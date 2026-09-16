# Demo script — the three hero conversations

Every question below is answered **from the script**: instant, offline, no API call, same words every time.
Set the toggles before each conversation, then type the questions in order. Hit "New case" between conversations.

Badge check: the header reads **SCRIPTED** for these. If it reads **LIVE**, you typed something off-script — still fine, just slower.

---

## A. Classical churna — "not patentable, but sellable"
Toggles: **India** · category **Classical AYUSH**

| # | Type this | Answer cites | Say while it loads |
|---|---|---|---|
| 1 | Can I patent and sell a classical churna in India? | Patents Act s.3(p) + D&C Rules r.153 | "The first thing a founder asks — and the answer is two different laws." |
| 2 | If I cannot patent it, how do I protect my brand name? | Trade Marks Act ss.18, 28 | "So we move them from the wrong protection to the right one." |
| 3 | What do I need before I can sell it in the market? | D&C Rules r.153 + r.161 | "Licence and label — the part that actually blocks launch." |

Point at: the citation panel changing with each answer.

## B. Medicinal plant — "a different regime, cleanly cited"
Toggles: **India** · category **Plant research**

| # | Type this | Answer cites | Say while it loads |
|---|---|---|---|
| 1 | What obligations apply if I use a medicinal plant for research in India? | Biological Diversity Act s.3 | "Same assistant, completely different body of law." |
| 2 | Do I have to share benefits with local communities? | Biological Diversity Act s.21 | "This is the obligation most startups don't know exists." |
| 3 | Can someone else patent this traditional use? | TKDL + Patents Act s.3(p) | "And this is India's defensive shield — the TKDL." |

## C. Selling abroad — "the jurisdiction switch"
Toggles: **Global** · category **Export / international**

| # | Type this | Answer cites | Say while it loads |
|---|---|---|---|
| 1 | What should I consider if I want to sell my product abroad? | PCT Art. 11(3) + Madrid Protocol | "Flip one switch and the legal lane changes." |
| 2 | How do I protect the brand in multiple countries? | Madrid Protocol | "One filing, many countries." |
| 3 | Does an Indian patent protect me outside India? | Paris Convention 4bis + PCT | "The most expensive misconception in the room." |

---

## The closer — refusing to guess
Ask anything outside the pack, e.g. **What is the GST rate on soap?**
The assistant declines instead of inventing law. Line to use:

> "It says *less* rather than making something up. That is the whole point — every sentence is tied to a source, and when there is no source, there is no answer."

## Hindi
Switch the language to **हि** and ask hero question 1 of conversation A (the suggested card is already in Hindi).
Hindi is covered for the **first** question of each conversation; the follow-ups are English only.

## If something breaks
- Badge says SERVER OFFLINE → the backend stopped. `python3 backend/server.py`
- An answer is slow → it went to Gemini. Stay on the scripted questions above.
- Everything fails → play the backup screencast (Divakaran).
