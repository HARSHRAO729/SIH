"""Mock backend for IP-SAKTI. Stdlib only: `python3 backend/mock_server.py`.

Returns hard-coded replies in the CONTRACT.md shape so the front-end can be built
before the real backend exists.
Keywords pick a hero reply; anything else returns the "declined" state.
"""
import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = 8000
DELAY = 0.8  # seconds, so the "typing..." state is visible

REPLIES = {
    "churna": {
        "answer": "A classical churna made from a formulation already described in authoritative AYUSH texts is not patentable in India, because it is traditional knowledge. You can still manufacture and sell it once you hold an AYUSH manufacturing licence for a classical (ASU) medicine.",
        "sources": [
            {"id": "tk-patent-bar", "text": "What are not inventions: an invention which in effect is traditional knowledge or which is an aggregation or duplication of known properties of traditionally known component or components.", "source": "Patents Act, 1970 — Section 3(p)"},
            {"id": "ayush-licence", "text": "No person shall manufacture for sale any Ayurvedic, Siddha or Unani drug except under a licence issued by the Licensing Authority.", "source": "Drugs and Cosmetics Rules, 1945 — Rule 153"},
        ],
        "confidence": "high",
    },
    "plant": {
        "answer": "Using an Indian medicinal plant for research or commercial use requires prior approval from the National Biodiversity Authority, and benefits may need to be shared with local communities.",
        "sources": [
            {"id": "abs-nba-approval", "text": "No person shall obtain any biological resource occurring in India or knowledge associated thereto for research or for commercial utilisation without previous approval of the National Biodiversity Authority.", "source": "Biological Diversity Act, 2002 — Section 3"},
        ],
        "confidence": "med",
    },
    "abroad": {
        "answer": "To protect your product in several countries, you can file one international patent application under the PCT, and register your brand in many countries at once through the Madrid System.",
        "sources": [
            {"id": "intl-pct", "text": "An international application filed under the PCT has the effect of a national application in each designated State.", "source": "Patent Cooperation Treaty — Article 11(3)"},
            {"id": "intl-madrid", "text": "A trademark can be protected in multiple member countries by filing a single international application.", "source": "Madrid Protocol (WIPO)"},
        ],
        "confidence": "med",
    },
}

DECLINED = {
    "answer": "I don't have a verified legal source for this question, so I won't guess. Please rephrase, or talk to a human IP expert.",
    "sources": [],
    "confidence": "low",
}


def reply_for(question):
    q = question.lower()
    for key, reply in REPLIES.items():
        if key in q:
            return {**reply, "declined": False, "mode": "mock"}
    return {**DECLINED, "declined": True, "mode": "mock"}


def validate(body):
    if not isinstance(body, dict):
        return "body must be a JSON object"
    if not str(body.get("question", "")).strip():
        return "question is required"
    if body.get("jurisdiction") not in ("india", "international"):
        return "jurisdiction must be india or international"
    if not body.get("product_type"):
        return "product_type is required"
    return None


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        raw = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Access-Control-Allow-Origin", "*")  # ponytail: open CORS, local demo only
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(raw)

    def do_OPTIONS(self):
        self.send_json(204, {})

    def do_GET(self):
        if self.path == "/api/health":
            return self.send_json(200, {"ok": True, "mode": "mock"})
        self.send_json(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/api/ask":
            return self.send_json(404, {"error": "not found"})
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"null")
        except json.JSONDecodeError:
            return self.send_json(400, {"error": "invalid JSON"})
        err = validate(body)
        if err:
            return self.send_json(400, {"error": err})
        time.sleep(DELAY)
        self.send_json(200, reply_for(body["question"]))


if __name__ == "__main__":
    print(f"Mock backend on http://localhost:{PORT}")
    ThreadingHTTPServer(("", PORT), Handler).serve_forever()
