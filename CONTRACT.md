# IP-SAKTI API Contract (v1)

The front-end and backend both follow this file. Changing it = tell the team first.

Base URL (local): `http://localhost:8000`
Mock and real backend serve the **same** shape. Switching mock → real is only the base URL.

## POST /api/ask

Request
```json
{
  "question": "Can I patent and sell my classical churna?",
  "jurisdiction": "india",
  "product_type": "classical",
  "language": "en"
}
```

| field | type | required | values |
|---|---|---|---|
| question | string | yes | non-empty |
| jurisdiction | string | yes | `india` \| `international` |
| product_type | string | yes | `classical` \| `new-drug` \| `plant-research` \| `export` \| `unknown` |
| language | string | no | `en` (default) \| `hi` |

Response `200`
```json
{
  "answer": "A classical churna made from a text-listed formulation is not patentable ...",
  "sources": [
    { "id": "tk-patent-bar", "text": "What are not inventions ...", "source": "Patents Act, 1970 — Section 3(p)" }
  ],
  "confidence": "high",
  "declined": false,
  "follow_ups": [
    { "text": "If I cannot patent it, how do I protect my brand name?", "jurisdiction": "india", "product_type": "classical" }
  ],
  "mode": "mock"
}
```

| field | type | notes |
|---|---|---|
| answer | string | plain text, may contain `\n` |
| sources | list of `{id, text, source}` | empty when `declined` is true |
| confidence | string | `high` \| `med` \| `low` |
| declined | bool | true = no source found, assistant refuses to guess. UI shows this state distinctly |
| follow_ups | list of `{text, jurisdiction, product_type}` | next questions to offer as clickable chips; empty for live/declined answers. Clicking one sets both toggles, then asks it |
| mode | string | where the answer came from: `scripted` (pre-written), `live` (Gemini), `mock` — badge/debugging only |

Response `400` (bad input) / `502` (answer engine unavailable — show "try again")
```json
{ "error": "question is required" }
```

## GET /api/health
```json
{ "ok": true, "mode": "auto" }
```
Server modes: `auto` (default — scripted answers first, Gemini for everything else), `live` (Gemini first, scripted on failure), `scripted` (offline only), `mock`.

## Snippet pack shape (Yashvi → Harsh)

`data/snippets.json` — a list of:
```json
{
  "id": "tk-patent-bar",
  "text": "Short quoted rule, 1–3 sentences.",
  "source": "Patents Act, 1970 — Section 3(p)",
  "jurisdiction": "india",
  "product_types": ["classical", "new-drug"],
  "keywords": ["patent", "churna", "formulation"]
}
```

`answer_hi` in `data/scripted_answers.json` (optional): the Hindi version of a scripted answer; English is used when it is missing.

`keywords` (optional but important): plain words a user would type that the legal quote doesn't contain.
Retrieval is keyword matching, so a snippet without them is hard to find (e.g. Section 3(p) never says "churna").
See `data/snippets.sample.json`.
