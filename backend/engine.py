"""Answer engine: snippet retrieval, Gemini call, citation gate, scripted fallback."""
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from mock_server import DECLINED, DELAY as MOCK_DELAY, reply_for as mock_reply

DATA = Path(__file__).resolve().parent.parent / "data"
MIN_SCORE = int(os.environ.get("MIN_SCORE", "2"))  # tuning knob: keyword hits needed before a snippet counts
TOP_K = 4
STOPWORDS = set("""a an and are as at be by can do does for from how i if in is it its my of on or
our so that the this to under we what when where which who will with without you your
""".split())


def load_json(name, fallback=None):
    path = DATA / name
    if not path.exists() and fallback:
        path = DATA / fallback
    return json.loads(path.read_text(encoding="utf-8"))


SNIPPETS = load_json("snippets.json", fallback="snippets.sample.json")
SCRIPTED = load_json("scripted_answers.json")
BY_ID = {s["id"]: s for s in SNIPPETS}


def tokens(text):
    # the Devanagari range is explicit: \w drops the vowel marks and shatters Hindi words
    words = (t for t in re.findall(r"[\w\u0900-\u097F]+", text.lower()) if len(t) > 2 and t not in STOPWORDS)
    return {t[:-1] if len(t) > 4 and t.endswith("s") else t for t in words}  # ponytail: plural strip, not a stemmer


def retrieve(question, jurisdiction, product_type):
    # ponytail: keyword overlap is the demo stand-in for embeddings + re-ranking; fine for ~20 snippets
    q = tokens(question)
    scored = []
    for s in SNIPPETS:
        if s["jurisdiction"] != jurisdiction:
            continue
        if product_type != "unknown" and product_type not in s["product_types"]:
            continue
        haystack = " ".join([s["text"], s["source"], s["id"].replace("-", " "), *s.get("keywords", [])])
        score = len(q & tokens(haystack))
        if score >= MIN_SCORE:
            scored.append((score, s))
    scored.sort(key=lambda x: -x[0])
    return [s for _, s in scored[:TOP_K]]


def cite(snippet):
    return {"id": snippet["id"], "text": snippet["text"], "source": snippet["source"]}


def declined(mode):
    return {**DECLINED, "declined": True, "mode": mode}


def scripted(question, jurisdiction, language="en"):
    q = question.lower()
    for s in SCRIPTED:
        if s["jurisdiction"] == jurisdiction and any(k in q for k in s["keywords"]):
            sources = [cite(BY_ID[i]) for i in s["source_ids"] if i in BY_ID]
            if sources:
                # optional answer_hi: the Hindi fallback, else English
                text = s.get(f"answer_{language}", s["answer"])
                return {"answer": text, "sources": sources, "confidence": s["confidence"],
                        "declined": False, "mode": "scripted"}
    return None


PROMPT = """You are IP-SAKTI, an assistant on intellectual property and regulation for AYUSH products.
Answer ONLY from the legal snippets below. Do not use outside knowledge.
If the snippets do not answer the question, set "declined" to true.
Write the answer in {language}, in 2-4 plain sentences, for a non-lawyer.

Snippets:
{snippets}

Question: {question}

Reply with JSON only:
{{"answer": string, "used_ids": [snippet ids you relied on], "confidence": "high"|"med"|"low", "declined": bool}}"""

LANGUAGES = {"en": "English", "hi": "Hindi"}


def call_gemini(prompt):
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY not set")
    model = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        data=json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"},
        }).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
    )
    # python.org builds on macOS ship without CA certs; the system bundle covers it
    ctx = ssl.create_default_context(cafile="/etc/ssl/cert.pem") if Path("/etc/ssl/cert.pem").exists() else None
    # Gemini throws the odd 503; one retry saves a fallback on stage
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
                data = json.load(r)
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except urllib.error.HTTPError as e:
            if e.code < 500 or attempt:
                raise
            print(f"gemini {e.code}, retrying", file=sys.stderr)
        except (urllib.error.URLError, TimeoutError):
            if attempt:
                raise
            print("gemini unreachable, retrying", file=sys.stderr)
        time.sleep(1.5)


def live(body, llm):
    found = retrieve(body["question"], body["jurisdiction"], body["product_type"])
    if not found:
        return declined("live")  # no source → never ask the LLM
    prompt = PROMPT.format(
        language=LANGUAGES.get(body.get("language", "en"), "English"),
        snippets="\n".join(f"[{s['id']}] ({s['source']}) {s['text']}" for s in found),
        question=body["question"],
    )
    out = json.loads(llm(prompt))
    # citation gate: keep only ids we actually supplied; no valid citation → decline
    allowed = {s["id"]: s for s in found}
    sources = [cite(allowed[i]) for i in out.get("used_ids", []) if i in allowed]
    if out.get("declined") or not sources or not str(out.get("answer", "")).strip():
        return declined("live")
    confidence = out.get("confidence") if out.get("confidence") in ("high", "med", "low") else "low"
    return {"answer": out["answer"], "sources": sources, "confidence": confidence, "declined": False, "mode": "live"}


def answer(body, mode, llm=call_gemini):
    if mode == "mock":
        return mock_reply(body["question"], MOCK_DELAY)
    if mode == "scripted":
        return scripted(body["question"], body["jurisdiction"], body.get("language", "en")) or declined("scripted")
    try:
        return live(body, llm)
    except Exception as e:
        # API/network/bad JSON → hero questions still answer from the script
        print(f"live failed, trying scripted: {e!r}", file=sys.stderr)
        fallback = scripted(body["question"], body["jurisdiction"], body.get("language", "en"))
        if fallback:
            return fallback
        raise
