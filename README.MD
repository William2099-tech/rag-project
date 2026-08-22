# RAG Project

Retrieval-Augmented Generation (RAG) project for the GenAI Secure Coding course. Built incrementally each week.

---

## Week 7 — Validation & Response Review

### What `/query` Does

A **POST** endpoint that accepts a user question, validates it, gets an AI answer, has a second AI call review that answer, and returns the final result.

- Docs UI: `http://127.0.0.1:8000/docs` → **POST /query** → Try it out
- Request body: `{"question": "What is retrieval augmented generation?"}`
- Success: `{"question": "...", "answer": "..."}`

### How It Connects to Earlier Weeks

| Week | What you built | How Week 7 uses it |
|------|----------------|-------------------|
| Week 5 | Single Gemini call in `/test-gemini` | Same SDK pattern, now with user input |
| Week 6 | Multi-step execution (outline → expand) | Same idea: multiple model calls in sequence |
| Week 7 | Validation + review | Adds guardrails before and after the AI calls |

### Why Input Validation Exists

Checks run **before** any AI call. Bad input (empty, too short, too long) is rejected with a **400** error. This saves API cost, prevents useless prompts, and is the first layer of secure GenAI design.

### Why Output Validation Exists

Checks run **after** the first model responds. If the AI returns empty or too-short text, the API returns a **500** error instead of sending bad data to the user.

### Why a Second AI Model Reviews the First Response

The first model answers the question. The second model reads that answer and improves it if needed. This **review/refine** pattern is common in production systems and connects to future weeks (RAG, guardrails, quality control).

### `/query` Flow (Step by Step)

1. User sends `{"question": "..."}`
2. `validate_user_input()` — reject bad questions early
3. First Gemini call — generate `raw_answer`
4. `validate_model_output()` — reject empty/short AI output
5. `review_model_output()` — second Gemini call improves the answer
6. Return `question` + final `answer` to the user

### Test Invalid Input (in `/docs`)

These should return clear errors **without** calling Gemini:

```json
{"question": ""}
```
```json
{"question": "hi"}
```

---

## Week 6 — Multi-Step Execution

### What `/test-gemini` Does

The endpoint runs **two Gemini calls in sequence** and returns only the final result.

- URL: `http://127.0.0.1:8000/test-gemini`
- Success: `{"response": "..."}`
- Errors return a safe message (no API key exposed)

### Multi-Step Flow

| Step | What it does | Returned to client? |
|------|----------------|---------------------|
| 1 | Ask Gemini for a short 3-point outline about Python | No (stored in `outline`) |
| 2 | Ask Gemini to expand that outline into a full explanation | Yes (`response`) |

### Why the steps are separated

Step 1 plans the answer. Step 2 uses that plan to produce a better, structured response. This matches how real AI systems chain logic instead of using one prompt.

### Challenges / open questions

- Two API calls take longer than one (browser may need 30–60 seconds)
- Still deciding when to migrate from `google-generativeai` to `google.genai`

---

## Where the Gemini Logic Lives

File: **`rag_app.py`** → function: **`test_gemini()`**

- API key loaded from `.env` at the top of the file
- Step 1: `outline = model.generate_content(outline_prompt).text`
- Step 2: `final_response = model.generate_content(expand_prompt).text`
- Return: `{"response": final_response.text}`

---

## Command Reference (Weeks 1–5)

All commands below were used before Week 6. Use **CMD** unless noted.

### Git — Clone & Sync

```cmd
git clone <your-repo-url>
```
Downloads the project from GitHub to your computer.

```cmd
cd c:\Users\LilWi\Documents\rag-project
```
Moves into the project folder. Run this first in any new terminal.

```cmd
git pull
```
Downloads the latest changes from GitHub before you start working.

```cmd
git status
```
Shows which files changed, which are staged, and which are untracked.

---

### Git — Save & Upload Changes

```cmd
git add rag_app.py requirements.txt .gitignore README.MD
```
Stages specific files for commit. **Never** add `.env`.

```cmd
git add .
```
Stages all changed files. Only use if you checked `git status` first and `.env` is not included.

```cmd
git commit -m "Your message here"
```
Saves staged changes locally with a description.

```cmd
git push
```
Uploads your commits to GitHub.

---

### Virtual Environment — Setup & Activate

```cmd
python -m venv venv
```
Creates a virtual environment folder (only needed once).

```cmd
venv\Scripts\activate.bat
```
Activates venv. Your prompt should show `(venv)`.

```cmd
deactivate
```
Turns off venv when you are done.

---

### Python Packages — Install Dependencies

```cmd
pip install -r requirements.txt
```
Installs all libraries listed in `requirements.txt` (`fastapi`, `uvicorn`, `python-dotenv`, `google-generativeai`).

---

### Environment File — API Key (`.env`)

Create or edit `.env` in the project root in Cursor (not Git cmd):

```
GEMINI_API_KEY=your_actual_key_here
```

- Loads your Gemini API key locally
- **Never commit this file** — it is listed in `.gitignore`

If `.env` shows as untracked in Git, add this line to `.gitignore`:

```
.env
```

Then:

```cmd
git add .gitignore
git commit -m "Ignore .env file"
git push
```

If you accidentally staged `.env`:

```cmd
git rm --cached .env
```

Removes `.env` from Git tracking without deleting the file on your computer.

---

### Run the Server

```cmd
cd c:\Users\LilWi\Documents\rag-project
venv\Scripts\activate.bat
uvicorn rag_app:app --host 127.0.0.1 --port 8000
```
Starts the FastAPI app. Leave this window open while testing.

```cmd
uvicorn rag_app:app --reload
```
Same as above, but auto-restarts when you save code changes (default port 8000).

---

### Test Endpoints

**In browser:**

- Health: `http://127.0.0.1:8000/health`
- Gemini: `http://127.0.0.1:8000/test-gemini`
- Query (Week 7): `http://127.0.0.1:8000/docs` → POST `/query`

**In CMD:**

```cmd
curl http://127.0.0.1:8000/health
```
Quick check that the server is running.

```cmd
curl http://127.0.0.1:8000/test-gemini
```
Calls Gemini. May take 30–60 seconds (longer in Week 6 with two steps).

---

### Troubleshooting

```cmd
netstat -ano | findstr :8000
```
Shows if anything is using port 8000.

```cmd
for /f "tokens=5" %a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do taskkill /F /PID %a
```
Kills stuck processes on port 8000 if the server hangs.

```cmd
uvicorn rag_app:app --host 127.0.0.1 --port 8001
```
Starts the server on a different port if 8000 is broken. Then use `:8001` in your URLs.

**Common fixes:**

| Problem | Likely cause | Fix |
|---------|--------------|-----|
| `ERR_CONNECTION_REFUSED` | Server not running or wrong port | Start uvicorn; match URL port to terminal |
| Blank page | Stuck server | Kill port 8000, restart uvicorn |
| `.env` in red (untracked) | Normal if ignored | Do not `git add .env` |
| `NameError: genai` | Missing import | Add `import google.generativeai as genai` at top of `rag_app.py` |

---

## Quick Start (Every Session)

```cmd
cd c:\Users\LilWi\Documents\rag-project
git pull
venv\Scripts\activate.bat
uvicorn rag_app:app --host 127.0.0.1 --port 8000
```
