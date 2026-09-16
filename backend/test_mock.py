"""Checks mock + engine against CONTRACT.md without calling Gemini. Run: python3 backend/test_mock.py"""
import json

import engine
from mock_server import reply_for
from server import validate

KEYS = {"answer", "sources", "confidence", "declined", "mode"}


def check_shape(r):
    assert set(r) == KEYS, r
    assert r["confidence"] in ("high", "med", "low")
    assert all(set(s) == {"id", "text", "source"} for s in r["sources"])
    assert r["declined"] == (not r["sources"]), r


def ask(q, j="india", pt="unknown"):
    return {"question": q, "jurisdiction": j, "product_type": pt, "language": "en"}


# mock
for q in ["Can I patent my churna?", "medicinal plant research", "selling abroad", "what is the GST rate?"]:
    check_shape(reply_for(q))
assert reply_for("GST rate")["declined"] is True

# validation
assert validate(ask("x")) is None
assert validate(ask(" "))
assert validate(ask("x", j="mars"))
assert validate(ask("x", pt="soap"))
assert validate([])

# retrieval: hero questions find the right snippet, jurisdiction lanes stay separate
HERO = [
    (ask("Can I patent and sell my classical churna?", pt="classical"), "tk-patent-bar"),
    (ask("Can I use a medicinal plant in my research?", pt="plant-research"), "abs-nba-approval"),
    (ask("How do I protect my product when selling abroad?", j="international", pt="export"), "intl-pct"),
]
for body, expected in HERO:
    ids = [s["id"] for s in engine.retrieve(body["question"], body["jurisdiction"], body["product_type"])]
    assert expected in ids, (body["question"], ids)
assert not engine.retrieve("Can I patent my churna?", "international", "unknown")
assert not engine.retrieve("What is the GST rate on soap?", "india", "unknown")

# scripted
for body, _ in HERO:
    r = engine.answer(body, "scripted")
    check_shape(r)
    assert not r["declined"] and r["mode"] == "scripted", body
assert engine.answer(ask("GST rate?"), "scripted")["declined"]


# live, with a fake LLM
def fake(reply):
    return lambda prompt: json.dumps(reply)


body = HERO[0][0]
r = engine.answer(body, "live", fake({"answer": "Not patentable.", "used_ids": ["tk-patent-bar"], "confidence": "high", "declined": False}))
check_shape(r)
assert r["mode"] == "live" and r["sources"][0]["id"] == "tk-patent-bar"

# citation gate: invented id → declined
r = engine.answer(body, "live", fake({"answer": "Trust me.", "used_ids": ["made-up"], "confidence": "high", "declined": False}))
assert r["declined"] and r["mode"] == "live"

# no snippet → declined, LLM never called
def boom_if_called(prompt):
    raise AssertionError("LLM called when it should not be")
assert engine.answer(ask("What is the GST rate on soap?"), "live", boom_if_called)["declined"]

# auto: hero questions answer from the script without touching the LLM
for body, _ in HERO:
    r = engine.answer(body, "auto", boom_if_called)
    check_shape(r)
    assert r["mode"] == "scripted", body

# auto: anything the script does not cover goes to the LLM
r = engine.answer(ask("traditional knowledge patent invention", pt="classical"), "auto",
                  fake({"answer": "Not an invention.", "used_ids": ["tk-patent-bar"], "confidence": "med", "declined": False}))
assert r["mode"] == "live" and not r["declined"], r

# LLM failure on a hero question → scripted fallback
def down(prompt):
    raise OSError("network down")
assert engine.answer(body, "live", down)["mode"] == "scripted"

# LLM failure on a non-hero question that has snippets → error surfaces (server returns 502)
try:
    engine.answer(ask("traditional knowledge patent invention", pt="classical"), "live", down)
    raise AssertionError("expected failure")
except OSError:
    pass

print("ok")
