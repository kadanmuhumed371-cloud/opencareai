import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load your environment variables (like your .env file)
load_dotenv()

print("--- STARTING GEMINI PING TEST ---")

try:
    # Set up the API key
    api_key = os.getenv("GEMINI_API_KEY") # Make sure this matches your .env file variable name
    if not api_key:
        print("ERROR: API key is completely missing or .env file is not loading!")
        exit()

    genai.configure(api_key=api_key)
    
    # Initialize the model you are using
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Send a simple text request
    print("Sending request to Gemini 2.5 Flash...")
    response = model.generate_content("Respond with exactly these words: 'The Brain is online.'")
    
    print("\n✅ SUCCESS! Gemini responded:")
    print(f"[{response.text.strip()}]")

except Exception as e:
    print("\n❌ API FAILED. Here is the exact reason:")
    print(str(e))