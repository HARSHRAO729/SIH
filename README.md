# IP-SAKTI — SIH26045 internal-round demo

Assistant that answers AYUSH IP/regulatory questions with cited legal sources. Prototype.

## Layout
- `NEXT_STEPS.md` — **what to do next and who does it. Start here.**
- `CONTRACT.md` — API + snippet JSON shape. **Read first.**
- `backend/mock_server.py` — mock backend (no installs)
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
