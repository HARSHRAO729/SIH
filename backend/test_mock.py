"""Checks the mock against CONTRACT.md. Run: python3 backend/test_mock.py"""
from mock_server import reply_for, validate

KEYS = {"answer", "sources", "confidence", "declined", "mode"}

for q in ["Can I patent my churna?", "medicinal plant research", "selling abroad", "what is the GST rate?"]:
    r = reply_for(q)
    assert set(r) == KEYS, r
    assert r["confidence"] in ("high", "med", "low")
    assert all(set(s) == {"id", "text", "source"} for s in r["sources"])
    assert r["declined"] == (not r["sources"])

assert reply_for("GST rate")["declined"] is True
assert validate({"question": "x", "jurisdiction": "india", "product_type": "classical"}) is None
assert validate({"question": " ", "jurisdiction": "india", "product_type": "classical"})
assert validate({"question": "x", "jurisdiction": "mars", "product_type": "classical"})
assert validate([])
print("ok")
