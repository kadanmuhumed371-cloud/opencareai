import gradio as gr
import torch
import numpy as np
import tempfile
import scipy.io.wavfile
from transformers import VitsModel, AutoTokenizer

# Load model and tokenizer
model = VitsModel.from_pretrained("jellecali8/somali_tts_model")
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-som")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device).eval()

# Load custom speaker embedding
try:
    speaker_embedding = torch.tensor(np.load("new_speaker_embedding.npy")).unsqueeze(0).to(device)
except Exception as e:
    speaker_embedding = None
    print(f"Embedding load error: {e}")

def tts_fn(text):
    try:
        inputs = tokenizer(text, return_tensors="pt").to(device)

        with torch.no_grad():
            output = model(**inputs, speaker_embeddings=speaker_embedding)

        # Check for empty waveform
        if output.waveform is None or output.waveform.shape[-1] == 0:
            return "❌ Model-ka ma soo saarin cod. Waxaa laga yaabaa in embedding uu cilad leeyahay."

        audio = output.waveform.squeeze().cpu().numpy()

        # Save audio to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            scipy.io.wavfile.write(f.name, rate=16000, data=(audio * 32767).astype(np.int16))
            return f.name
    except Exception as e:
        return f"Error during synthesis: {str(e)}"

gr.Interface(
    fn=tts_fn,
    inputs=gr.Textbox(label="Qor qoraalka Somali"),
    outputs=gr.Audio(label="Codka la clone gareeyey"),
    title="Cod Somali ah oo la clone gareeyay"
).launch()
