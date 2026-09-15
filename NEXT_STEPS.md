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
1. Create `data/snippets.json` using the exact shape in `data/snippets.sample.json`.
2. ~15–20 **real, correctly cited** snippets: TK patent bar, prior-art library, GI basics, ABS/biodiversity, AYUSH licensing, labelling/advertising, PCT, Madrid.
3. Write the ideal sourced answer for each of the 3 hero questions → `data/hero_answers.md` (with Dhyani).
4. Keep a sources list for the references slide.

Hand-off: push `data/snippets.json` and tell Harsh.

### Harsh — Real backend
1. `backend/` real server, same contract as the mock.
2. Load `data/snippets.json`; filter by jurisdiction + product_type; keyword-match the question.
3. No matching snippet → `declined: true` (never call the LLM without sources).
4. Call Gemini with the snippets in the prompt; return the snippets as `sources`.
5. Scripted mode for the 3 hero questions + a switch `MODE=live|scripted|mock`.
6. API key in `.env` (never committed).

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
