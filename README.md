# IP-SAKTI — SIH26045 internal-round demo

Assistant that answers AYUSH IP/regulatory questions with cited legal sources. Prototype.

## Layout
- `NEXT_STEPS.md` — **what to do next and who does it. Start here.**
- `CONTRACT.md` — API + snippet JSON shape. **Read first.**
- `backend/server.py` — real backend (no installs), `MODE=live|scripted|mock`
- `backend/mock_server.py` — mock backend for the front-end
- `frontend/` — Ritik + Naitri
- `data/` — knowledge pack (Yashvi)

## Front-end team: run the mock
```bash
python3 backend/mock_server.py
```
Then `POST http://localhost:8000/api/ask`. Questions containing `churna`, `plant` or `abroad` return hero answers; anything else returns the `declined` state.

```bash
curl -X POST localhost:8000/api/ask -H 'Content-Type: application/json' -d '{"question":"Can I patent my churna?","jurisdiction":"india","product_type":"classical"}'
```

Keep the base URL in one config value — switching to the real backend is changing only that.

## Real backend (Harsh)
```bash
cp .env.example .env        # add GEMINI_API_KEY
python3 backend/server.py   # auto: scripted answers first, Gemini for the rest
python3 backend/test_mock.py
```
- `auto` (default): a hero question is answered instantly from `data/scripted_answers.json` — no API call, works offline. Anything else goes to Gemini.
- Gemini path: matching snippets → Gemini → keeps only the citations it was given. No snippet or no valid citation → `declined`.
- `MODE=scripted` for a fully offline demo, `MODE=live` to force Gemini, `MODE=mock` for front-end work.
- Uses `data/snippets.json` if present, else `data/snippets.sample.json`.
