import os
from dotenv import load_dotenv
from fastapi import FastAPI
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("Gemini API key not found in .env file")

app = FastAPI()
@app.get("/health")
def health():
    return {"message": "API is running"}






