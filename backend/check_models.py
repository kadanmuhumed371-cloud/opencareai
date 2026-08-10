import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load your API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# List available models
print("Available models:")
for m in genai.list_models():
    print(f"Model Name: {m.name}")   