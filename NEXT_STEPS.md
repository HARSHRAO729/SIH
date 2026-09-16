# What's done, what's next, who does it

## Done — Phase 0 kickoff (Harsh)
- API contract → `CONTRACT.md`
- Mock backend → `backend/mock_server.py` (run `python3 backend/mock_server.py`, no installs)
- Snippet JSON shape → `data/snippets.sample.json`

Nobody is blocked now. Everyone starts Phase 1 in parallel.

> ⚠️ The mock's answers/quotes are placeholders, not verified law. Do not use them in the deck or final demo.

## Phase 1 — Parallel build (start now)

### Ritik — Front-end lead
1. Read `CONTRACT.md`. Run the mock.
2. Create the app in `frontend/` (React or plain HTML/CSS/JS).
3. Put the backend URL in **one** config value (e.g. `API_BASE = "http://localhost:8000"`).
4. Build: chat screen (thread, input, typing indicator), India/International toggle, language selector.
5. Build the answer card + citation panel (answer, sources, confidence badge).
6. Build the **declined** state (`declined: true` → "won't guess" message + escalate button) and the error state (network / 400).
7. Disclaimer "Information, not legal advice" + "Talk to a human" button.

Test with: `churna` (India), `plant` (India), `abroad` (International), anything else (declined).

### Naitri — Front-end support + design
1. Landing/intro screen with a Start button.
2. Classifier flow: 2–3 guided questions → sets `product_type` (`classical` | `new-drug` | `plant-research` | `export` | `unknown`) → opens chat.
3. "How it works" screen (real architecture).
4. Colours, fonts, icons — shared with Ritik and matching the deck.
5. Architecture graphic + screenshots → Dhyani.

Work in `frontend/` with Ritik; agree folder split before starting.

### Yashvi — Knowledge pack
1. Create `data/snippets.json` using the exact shape in `data/snippets.sample.json` — **including `keywords`** (words a user would type, e.g. "churna", "sell abroad"). Without them the backend can't find the snippet.
2. ~15–20 **real, correctly cited** snippets: TK patent bar, prior-art library, GI basics, ABS/biodiversity, AYUSH licensing, labelling/advertising, PCT, Madrid.
3. Write the ideal sourced answer for each of the 3 hero questions → `data/hero_answers.md` (with Dhyani).
4. Keep a sources list for the references slide.

Hand-off: push `data/snippets.json` and tell Harsh.

### Harsh — Real backend
- [x] `backend/server.py`, same contract as the mock, `MODE=live|scripted|mock`
- [x] Snippet retrieval (jurisdiction + product_type filter, keyword match)
- [x] No snippet / invalid citation → `declined` (LLM never called without sources)
- [x] Gemini call + citation gate; scripted fallback if Gemini fails on a hero question
- [ ] Add `GEMINI_API_KEY` to `.env` and test live answers for real
- [ ] Swap to Yashvi's `data/snippets.json`; tune `MIN_SCORE` if answers decline too often
- [ ] Replace `data/scripted_answers.json` text with Yashvi's verified ideal answers

### Dhyani — Pitch + deck
1. Outline the story: problem → solution → live demo → real architecture.
2. Finalise the 6-slide deck against the template.
3. Q&A sheet (technical answers with Harsh, e.g. "is this real RAG?").
4. Every slide claim must match what the demo shows.

### Divakaran — QA + demo script
1. Write test cases from `CONTRACT.md` (hero questions, declined, toggle, bad input).
2. Test Ritik's front-end against the mock as soon as screens exist; log bugs as GitHub Issues.
3. Draft the run-of-show (click-by-click, who says what).

## Phase 2 — Integration (Harsh + Ritik)
When the real backend is ready, Ritik changes `API_BASE` from mock to real. Test all 3 hero questions + declined, in live and scripted mode.

## Phase 3–6
Polish (Naitri, Yashvi, Dhyani) → Harden + backup screencast (Divakaran) → two full dry-runs (all) → export deck to PDF and upload (Divakaran).

## Git rules
- Don't push directly to `main`. Branch (`ritik/chat-screen`), push, open a PR.
- Only touch your own folder unless you've agreed otherwise: `frontend/` (Ritik, Naitri), `backend/` (Harsh), `data/` (Yashvi).
- Changing `CONTRACT.md` = tell Harsh and Ritik first.

---

## ✅ Update — HARSH's part is done (backend ready)

The real backend is in `main`. It follows the same `CONTRACT.md` as the mock, so nothing changes for the front-end except the base URL.

```bash
python3 backend/server.py                  # live (needs GEMINI_API_KEY in .env)
MODE=scripted python3 backend/server.py    # no internet needed, hero answers only
python3 backend/mock_server.py             # mock, for front-end work
```

Left on Harsh's side (small, waiting on others): test live with the real API key, swap in Yashvi's `data/snippets.json`, replace scripted answers with her verified ones.

## Next step — who does what now

### Ritik — connect the front-end (top priority)
1. Keep building against the mock until the chat screen + citation panel work.
2. Then run `python3 backend/server.py` and point `API_BASE` at it. Test: churna (India), plant (India), abroad (International), and one random question → must show the **declined** state.
3. Handle `502` → show "Something went wrong, try again".
4. Tell Harsh when screens are ready → joint integration test (Phase 2).

### Naitri — unchanged
Landing, classifier flow, "How it works" screen, styling. The classifier must send one of: `classical` | `new-drug` | `plant-research` | `export` | `unknown`.

### Yashvi — knowledge pack (now blocking the real answers)
1. Push `data/snippets.json` (~15–20 real snippets). **Every snippet needs `keywords`** — words a user would type. Copy the shape from `data/snippets.sample.json`.
2. Write verified ideal answers for the 3 hero questions → `data/hero_answers.md`.
3. Tell Harsh → he updates `data/scripted_answers.json` and checks that each hero question finds its snippet.

### Dhyani — deck + Q&A
Use this for "is this real RAG?": *"The demo retrieves from a curated pack by keyword and makes the model cite only snippets it was given; if there's no source, it refuses. The full version replaces keyword matching with semantic search over the full legal corpus."*

### Divakaran — start testing the backend now
1. Run `python3 backend/test_mock.py` → must print `ok`.
2. Run the server in `scripted` mode and hit it with the test cases (hero questions, random question, bad input → `400`).
3. Log failures as GitHub Issues, tag Harsh.

### Harsh — after Yashvi's hand-off
1. Add `GEMINI_API_KEY` to `.env`, test live answers.
2. Load Yashvi's snippets; if good questions come back declined, lower `MIN_SCORE` to `1` in `.env` or ask her for more keywords.
3. Integration test with Ritik → then Phase 3 (polish).

---

## ✅ Update — front-end connected to the backend

Ritik's repo is cloned into `frontend/` (still his own repo — it is git-ignored here, push front-end changes from inside that folder).

Run both:
```bash
MODE=scripted python3 backend/server.py    # terminal 1
cd frontend && npm install && npm run dev  # terminal 2 → http://localhost:5173
```

Tested end to end against the scripted backend: all 3 hero questions answer with sources, an unsupported question shows the declined card, the server-down error + **Try Again** works, and the header shows the backend mode (LIVE / SCRIPTED / MOCK / SERVER OFFLINE).

Backend changes that came out of it: retrieval now understands Hindi words, export keywords added, and `answer_hi` in `data/scripted_answers.json` is used for Hindi scripted answers (falls back to English).

### Still open
- **Yashvi:** Hindi scripted answers (`answer_hi`) + Hindi `keywords` on each snippet, or the Hindi demo answers in English.
- **Harsh:** live mode still untested (no `GEMINI_API_KEY` yet).
- **Ritik:** front-end fixes were made in the clone — review and merge them into your repo.

---

## ✅ Update — live mode verified (Gemini working)

Live answers work end to end: retrieval → Gemini → citation gate, in English and Hindi, with real sources attached.

- Model is now **`gemini-3.6-flash`** (`gemini-2.5-flash` is retired for new API keys). Set it in `.env` with `GEMINI_MODEL`.
- Typical live answer takes 4–7 seconds; Hindi can take ~15s.
- Gemini occasionally returns 503, so the backend retries once, then falls back to the scripted answer. Rapid repeated questions can hit a 429 rate limit on the free tier — don't spam questions during the demo.
- If the header badge says SCRIPTED during the demo, the API failed and the fallback saved it.
