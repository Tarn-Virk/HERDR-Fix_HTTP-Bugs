# HERDR-Fix_HTTP-Bugs
🐛 herdr-demo  A deliberately broken FastAPI contacts app, built as a hands-on demo for Herdr multi-agent orchestration. A tiny CRUD API — four endpoints, four route files, one in-memory data store. On the surface it looks fine. Underneath, it ships with two planted bugs and three missing features. The baseline test suite scores it 4 out of 9.
 

---

## 📋 Prerequisites

- Python 3.10+
- Git
- [Claude Code](https://claude.com/claude-code), installed and authenticated
- A terminal that handles tmux-style splits — WSL, macOS Terminal, any modern Linux terminal

---

## 🚀 Setup

### 1. Clone and enter the repo

git clone https://github.com/Tarn-Virk/HERDR-Fix_HTTP-Bugs


### 2. Create the virtual environment

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


### 3. Tag the baseline

Gives you a one-command rewind back to the broken state between runs:

git tag baseline-4of9

### 4. Install Herdr + the Claude integration

curl -fsSL https://herdr.dev/install.sh | sh
herdr integration install claude
herdr --help


## 🏃 Running the app

### Start the server (Terminal A — leave it running)

source .venv/bin/activate
uvicorn main:app --reload --port 8000

Open http://127.0.0.1:8000 in a browser. You should see four contacts: Alice, Bob, Charlie, Dana.

### Check the baseline score (Terminal B)

.venv/bin/python test_api.py

Expected output:

4/9 checks passed

If you see 4/9, you're ready to go. If not, something's drifted — `git reset --hard baseline-4of9` and try again.



## 👀 See the bugs for yourself (optional, but fun)

With the server running, open the app in a browser:

**Bug A — the invisible edit**
- Click **Edit** on Alice's row → type `Alicia` → OK
- Status line reports success ✅
- Table still shows **Alice** after refresh ❌

**Bug B — the shifting delete**
- Delete Bob (id 2) → correct, Bob disappears
- Delete Charlie (id 3) → wait, **Dana** disappears instead ❌

Both bugs confirmed. Now let the agents sort it out.

---

## 🤖 Running the Herdr orchestration

### 1. Launch Herdr (Terminal B)


cd ~/herdr-demo
herdr


### 2. Paste the lead agent prompt


You are the lead agent for a parallel bug-fix run on a FastAPI
contacts app at ~/herdr-demo.

The server is already running on port 8000 with --reload in a
separate terminal. Current test score is 4/9 (python test_api.py).

Spawn FOUR child agents in four new panes, one per route file.
Each child owns exactly one file and must not touch any other
file. main.py and store.py are OFF LIMITS to everyone.

Agent 1 — routes/get_contacts.py
  Add a ?search= query param. Case-insensitive match on name OR
  email. No arg = return all.

Agent 2 — routes/create_contact.py
  Add two checks before insert:
   - duplicate email → return 409
   - blank or whitespace-only name → return 400

Agent 3 — routes/update_contact.py
  Fix the mutation bug. The update returns a copy and never
  writes back. Look up by id, mutate in place.

Agent 4 — routes/delete_contact.py
  Fix the index bug. Code treats id as list position (id-1).
  After any delete, positions shift but ids don't. Look up by
  id, then remove.

Rules for every child:
 - Edit only your assigned file.
 - Do not restart the server — --reload handles it.
 - Do not probe the server mid-edit.
 - When done, print "DONE: <filename>" and stop.

Once all four print DONE, run:
  .venv/bin/python test_api.py
Report the final score back here.
```

### 3. Watch the panes spawn

- Four panes open across the Herdr session
- Each agent reads its assigned file, edits it, prints `DONE: <file>`
- Terminal A logs four reload lines as uvicorn picks up each change
- The lead collects all four DONEs, runs the test, reports **9/9** ✅

---

## ✅ Verify the fix

### Test suite

```bash
.venv/bin/python test_api.py
```

Expected: `9/9 checks passed`.

### Browser smoke test

- Edit Alice → "Alicia" → the table shows **Alicia** after refresh ✅
- Delete Bob + Charlie → only Alice/Alicia and Dana remain ✅
- Visit `http://127.0.0.1:8000/contacts?search=ali` → Alicia only ✅

---

## 🔄 Reset back to broken (for another run)

# Stop Herdr: Ctrl+D in the lead pane
# Stop uvicorn in Terminal A: Ctrl+C

pkill -f uvicorn            # kill orphans, if any
git reset --hard baseline-4of9
git clean -fd               # removes anything the agents created
git status                  # should say: working tree clean
```

Re-run the baseline check and you'll be back at 4/9, ready to go again.

---

## 🛠 Troubleshooting

**Score comes back as 8/9**
Usually the POST agent added one of the two checks (409 or 400) but not both. Re-prompt that agent: *"You missed the [409 duplicate / 400 blank-name] check. Add it."*

**A pane sits silent for over a minute**
The agent probably hit a tool approval prompt. Check each pane and approve.

**The final test errors instead of scoring**
Server might be mid-reload. The lead should retry once. If it keeps failing, check uvicorn in Terminal A is still alive: `lsof -i :8000`.

**An agent tries to edit `main.py` or `store.py`**
The prompt forbids this. Stop that agent, remind it of the rule, and re-run just that lane.

---

## 📁 Repo layout

```
herdr-demo/
├── main.py                    # FastAPI app + routers wired in (DO NOT EDIT)
├── store.py                   # In-memory data + helpers (DO NOT EDIT)
├── routes/
│   ├── get_contacts.py        # GET    /contacts        — Agent 1
│   ├── create_contact.py      # POST   /contacts        — Agent 2
│   ├── update_contact.py      # PUT    /contacts/{id}   — Agent 3
│   └── delete_contact.py      # DELETE /contacts/{id}   — Agent 4
├── static/
│   └── index.html             # The browser UI
├── test_api.py                # Supervisor test — 9 live checks
└── requirements.txt
```

Each endpoint lives in its own file so four agents can work in parallel without touching the same code. That split is the whole reason this demo works cleanly.

---

## 🙏 Credits

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Orchestrated with [Herdr](https://herdr.dev) + [Claude Code](https://claude.com/claude-code)
- Walkthrough video: *[link coming soon]*

---
