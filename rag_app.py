import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("Gemini API key not found in .env file")
genai.configure(api_key=gemini_api_key)

app = FastAPI()

MODEL_NAME = "gemini-flash-latest"


class QueryRequest(BaseModel):
    question: str


def validate_user_input(text: str):
    if text is None or text.strip() == "":
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    if len(text) < 5:
        raise HTTPException(status_code=400, detail="Question is too short")

    if len(text) > 500:
        raise HTTPException(status_code=400, detail="Question is too long")


def validate_model_output(text: str):
    if text is None or text.strip() == "":
        raise HTTPException(status_code=500, detail="AI returned an empty response")

    if len(text) < 10:
        raise HTTPException(status_code=500, detail="AI response is too short")


def review_model_output(original_answer: str):
    review_prompt = f"""
You are reviewing an AI-generated response.

Your job:
- If the response is unclear, incomplete, or poorly written, improve it.
- If the response is already good, return it unchanged.

AI response to review:
{original_answer}
"""

    review_model = genai.GenerativeModel(MODEL_NAME)
    review_response = review_model.generate_content(review_prompt)

    return review_response.text


@app.get("/health")
def health():
    return {"message": "API is running"}


@app.get("/test-gemini")
def test_gemini():
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        topic = "the Python programming language"

        outline_prompt = (
            f"Create a short 3-point outline about {topic}. "
            "Use numbered points only."
        )
        outline_response = model.generate_content(outline_prompt)
        outline = outline_response.text
        print("Step 1 complete: outline generated.")

        expand_prompt = (
            f"Using this outline:\n{outline}\n\n"
            f"Write a clear explanation of {topic}."
        )
        final_response = model.generate_content(expand_prompt)

        return {"response": final_response.text}

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to get a response from Gemini. Check your API key and try again.",
        )


@app.post("/query")
def query_ai(request: QueryRequest):
    validate_user_input(request.question)

    primary_model = genai.GenerativeModel(MODEL_NAME)
    primary_response = primary_model.generate_content(request.question)

    raw_answer = primary_response.text

    validate_model_output(raw_answer)

    reviewed_answer = review_model_output(raw_answer)

    return {
        "question": request.question,
        "answer": reviewed_answer,
    }
