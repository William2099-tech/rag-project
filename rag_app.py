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
        # Step 5: Create a Gemini model
        model = genai.GenerativeModel("gemini-flash-latest")

        # Send your prompt
        prompt = "explain what the python programming language is and how it works"
        response = model.generate_content(prompt)

        # Return the response text as JSON
        return {"response": response.text}

    except Exception:
        # Clear error for the user — no API key or other secrets exposed
        raise HTTPException(
            status_code=500,
            detail="Failed to get a response from Gemini. Check your API key and try again.",
        )