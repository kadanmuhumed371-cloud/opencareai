import os
from google.cloud import texttospeech

# --- ADDED THIS TO FIX AUTHENTICATION ---
key_path = os.path.join(os.getcwd(), "service-account.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
# ----------------------------------------

# Initialize client
client = texttospeech.TextToSpeechClient()

# List voices
# Note: Somali (so-SO) is a low-resource language. If it returns nothing, we check all.
print("Listing all voices to find what works:")
voices = client.list_voices()

for voice in voices.voices:
    # Print Somali voices, or any voice to see if the connection is working
    if "so" in voice.language_codes[0]:
        print(f"FOUND SOMALI VOICE: {voice.name}, Language: {voice.language_codes[0]}")

print("\n(If no Somali voices printed, the system currently only supports standard global voices.)")