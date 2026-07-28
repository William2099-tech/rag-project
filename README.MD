# RAG Project

Retrieval-Augmented Generation (RAG) project for the GenAI Secure Coding course. Built incrementally each week.

---

## What `/test-gemini` Does

A GET endpoint that sends a prompt to Gemini and returns the reply as JSON.

- URL: `http://127.0.0.1:8000/test-gemini`
- Success: `{"response": "..."}`
- Error: returns a clear message without exposing your API key

---

## Where the Gemini Call Lives

File: **`rag_app.py`** → function: **`test_gemini()`**

- API key loaded from `.env` at the top of the file
- Model created with `genai.GenerativeModel("gemini-flash-latest")`
- Prompt sent with `model.generate_content(prompt)`
- Text returned with `response.text`

---

## What I Learned from the Gemini Documentation

- Use `genai.configure(api_key=...)` before calling the API
- Create a model with `GenerativeModel("model-name")`
- Send prompts with `generate_content()`
- Get the reply from `response.text`
- Older models like `gemini-pro` may not work — use `gemini-flash-latest`
- Keep API keys in `.env`, never in code or Git

---

## Questions I Still Have

- Do we need to switch to the newer `google.genai` package?
- Which model name does the course expect for grading?
- How will document retrieval be added in later weeks?

---

## Notes

**Files:** `rag_app.py`, `requirements.txt`, `.gitignore`, `.env` (local only)

**Run the app:**
```powershell
cd c:\Users\LilWi\Documents\rag-project
.\venv\Scripts\Activate.ps1
uvicorn rag_app:app --reload
```

**Fixes applied:** added `genai` import, fixed indentation, switched to `gemini-flash-latest`, added error handling with `HTTPException`
