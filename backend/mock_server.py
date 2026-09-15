"""Mock backend for IP-SAKTI. Stdlib only: `python3 backend/mock_server.py`.

Returns hard-coded replies in the CONTRACT.md shape so the front-end can be built
before the real backend exists. Same server as server.py, with MODE=mock.
Keywords pick a hero reply; anything else returns the "declined" state.
"""
import time

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


def reply_for(question, delay=0):
    time.sleep(delay)
    q = question.lower()
    for key, reply in REPLIES.items():
        if key in q:
            return {**reply, "declined": False, "mode": "mock"}
    return {**DECLINED, "declined": True, "mode": "mock"}


if __name__ == "__main__":
    import server
    server.serve("mock")
