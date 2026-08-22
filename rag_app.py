import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import google.generativeai as genai
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("Gemini API key not found in .env file")
genai.configure(api_key=gemini_api_key)
app = FastAPI()
@app.get("/health")
def health():
    return {"message": "API is running"}
@app.get("/test-gemini")
def test_gemini():
    try:
        model = genai.GenerativeModel("gemini-flash-latest")
        topic = "the Python programming language"

        # Step 1: Generate a short outline (intermediate result)
        outline_prompt = (
            f"Create a short 3-point outline about {topic}. "
            "Use numbered points only."
        )
        outline_response = model.generate_content(outline_prompt)
        outline = outline_response.text
        print("Step 1 complete: outline generated.")

        # Step 2: Expand the outline into a full response
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