"""IP-SAKTI backend. Stdlib only.

    python3 backend/server.py            # MODE from .env, default auto
    MODE=scripted python3 backend/server.py
"""
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PORT = int(os.environ.get("PORT", "8000"))
JURISDICTIONS = ("india", "international")
PRODUCT_TYPES = ("classical", "new-drug", "plant-research", "export", "unknown")


def load_env():
    env = Path(__file__).resolve().parent.parent / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"'))


def validate(body):
    if not isinstance(body, dict):
        return "body must be a JSON object"
    if not isinstance(body.get("question"), str) or not body["question"].strip():
        return "question is required"
    if body.get("jurisdiction") not in JURISDICTIONS:
        return "jurisdiction must be india or international"
    if body.get("product_type") not in PRODUCT_TYPES:
        return "product_type must be one of " + ", ".join(PRODUCT_TYPES)
    if body.get("language", "en") not in ("en", "hi"):
        return "language must be en or hi"
    return None


def make_handler(mode):
    from engine import answer  # imported late so .env is loaded first

    class Handler(BaseHTTPRequestHandler):
        def send_json(self, status, data):
            raw = json.dumps(data, ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("Access-Control-Allow-Origin", "*")  # ponytail: open CORS, local demo only
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()
            self.wfile.write(raw)

        def do_OPTIONS(self):
            self.send_json(204, {})

        def do_GET(self):
            if self.path == "/api/health":
                return self.send_json(200, {"ok": True, "mode": mode})
            self.send_json(404, {"error": "not found"})

        def do_POST(self):
            if self.path != "/api/ask":
                return self.send_json(404, {"error": "not found"})
            try:
                body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"null")
            except (json.JSONDecodeError, ValueError):
                return self.send_json(400, {"error": "invalid JSON"})
            err = validate(body)
            if err:
                return self.send_json(400, {"error": err})
            try:
                self.send_json(200, answer(body, mode))
            except Exception as e:
                print(f"answer failed: {e!r}", file=sys.stderr)
                self.send_json(502, {"error": "answer engine unavailable"})

    return Handler


def serve(mode):
    if mode not in ("auto", "live", "scripted", "mock"):
        sys.exit("MODE must be auto, live, scripted or mock")
    print(f"IP-SAKTI backend ({mode}) on http://localhost:{PORT}")
    ThreadingHTTPServer(("", PORT), make_handler(mode)).serve_forever()


if __name__ == "__main__":
    load_env()
    serve(os.environ.get("MODE", "auto"))
