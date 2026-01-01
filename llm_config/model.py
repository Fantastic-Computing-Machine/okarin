import os

from dotenv import load_dotenv
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is required to start the application.")

model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
client = ChatGoogleGenerativeAI(model=model_name, api_key=api_key)
