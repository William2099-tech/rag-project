# RAG Project

Retrieval-Augmented Generation (RAG) project for the GenAI Secure Coding course. Built incrementally each week.

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

## Run the App

```cmd
cd c:\Users\LilWi\Documents\rag-project
venv\Scripts\activate.bat
uvicorn rag_app:app --host 127.0.0.1 --port 8000
```

Test:

- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/test-gemini`

---

## Where the Gemini Logic Lives

File: **`rag_app.py`** → function: **`test_gemini()`**

- API key loaded from `.env` at the top of the file
- Step 1: `outline = model.generate_content(outline_prompt).text`
- Step 2: `final_response = model.generate_content(expand_prompt).text`
- Return: `{"response": final_response.text}`
