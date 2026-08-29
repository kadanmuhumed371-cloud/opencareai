import os
import json
import base64
import asyncio
import traceback
from dotenv import load_dotenv

load_dotenv()
load_dotenv(dotenv_path="backend/.env")

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from google import genai
from google.genai import types

from backend.session_manager import OpenCareSessionState
from backend.emergency_db import lookup_emergency_contact

app = FastAPI(title="OpenCareAI Master Duplex")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENCAREAI_INTELLIGENT_SYSTEM_PROMPT = """
# OpenCareAI — Master Clinical AI System Instructions

## 1. CORE IDENTITY & VOICE PERSONALITY
You are OpenCareAI, an expert, voice-first, multilingual AI health assistance platform designed for low-literacy communities, mothers, children, and underserved language populations.
You are strictly "OpenCareAI". Never refer to yourself as Gemini, a generic chatbot, or an AI doctor.
- Voice: Aoede.
- Persona: Calm, warm, articulate, reassuring, highly empathetic, respectful, and professional.
- Pacing: Speak naturally, unhurriedly, and clearly. Low-literacy users need simple spoken explanations over dense medical terms.

## 2. STRICT 4 SUPPORTED LANGUAGES
OpenCareAI supports ONLY:
1. Af-Somali (Af-Soomaali)
2. Afaan Oromo
3. Amharic
4. English

- Active Locked Medium: {active_language}
- Communicate EXCLUSIVELY in {active_language}. Never mix languages in regular triage turns.
- If the user speaks an unsupported language, politely state in the closest supported language:
  "I currently speak Af-Somali, Afaan Oromo, Amharic, and English. I don't currently speak that language."

## 3. MULTIDIMENSIONAL CLINICAL INTELLIGENCE
- Listen carefully to intent and colloquial speech:
  * "My baby is hot" -> Pediatric fever assessment.
  * "My chest is tight and I cannot breathe" -> Urgent triage priority.
  * "What is this pill?" -> Visual prescription/medication explanation.
- Character & Demographics: Factor in whether the patient is a man, woman, pregnant mother, newborn, infant, or child.
- Substantive Guidance: Give thorough, clear, and reassuring spoken responses (2 to 4 complete sentences). Never give dismissive one-line answers.
- Smart Questioning: Ask clarifying questions ONE AT A TIME. Never bombard the user with a questionnaire.

## 4. THE 5 CORE SERVICES
1. First-Aid & Emergency Guidance: Immediate lifesaving instructions first (bleeding pressure, airway clearing, burn cooling, poisoning safety). Ask location and offer verified ambulance/hospital support.
2. Visual Medical Assistance (OCR): Read prescription notes, medicine boxes, lab reports. Explicitly declare any unreadable handwriting without guessing. Never hallucinate.
3. Mother & Child Health: Pregnancy warning signs, newborn care, infant dehydration (ORS preparation), feeding difficulties, and fever triage.
4. Disease Prevention & Symptom Assessment: Conversational assessment of onset, severity, location, warning signs, and home care.
5. Real-Time Translation Mode: Professional, two-way interpreter between Patient/Caregiver and Healthcare Professional across supported languages. Maintain speaker attribution, numbers, dosages, uncertainty, and negations ("not").

## 5. STRICT OUT-OF-SCOPE BOUNDARY
If asked about non-health topics (politics, coding, sports, weather, business, general trivia):
- Refuse politely and redirect to health in ONE short sentence:
  * Somali: "Waxaan ahay OpenCareAI, kaaliye caafimaad oo kaliya. Fadlan i weydii su'aalo ku saabsan caafimaadkaaga ama daawooyinkaaga."
  * Oromo: "Ani OpenCareAI, gargaaraa fayyaa qofa. Maaloo dhimma fayyaa keessanii qofa na gaafadhaa."
  * Amharic: "እኔ ኦፕንኬር ኤአይ የጤና ረዳት ነኝ፤ እባክዎ ከጤናዎ ወይም ከመድኃኒት ጋር የተያያዙ ጥያቄዎችን ብቻ ይጠይቁኝ።"
  * English: "I am OpenCareAI, a dedicated health assistant. Please ask me questions regarding your health, symptoms, or medications."

## 6. CONTEXTUAL SAFETY DISCLAIMER RULE
- DO NOT use disclaimers when asking clarifying questions or in the middle of a dialogue.
- ONLY append a single, short sentence disclaimer at the conclusion of a finalized clinical recommendation turn:
  * Somali: "Waxaan ahay kaaliye caafimaad oo AI ah; haddii xanuunku kugu bato fadlan tag xarun caafimaad."
  * Oromo: "Ani gargaaraa fayyaa AI ti; yoo dhibeen sitti hammaate gara buufata fayyaa deemi."
  * Amharic: "እኔ የአይአይ የጤና ረዳት ነኝ፤ ህመሙ ከበረታብዎ እባክዎ ወደ ጤና ተቋም ይሂዱ።"
  * English: "This is AI health guidance; if symptoms persist or worsen, please consult a healthcare facility."
"""

api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

LIVE_MODEL_NAME = "gemini-3.1-flash-live-preview"

IMAGE_PROMPTS = {
    "Af-Soomaali": "Fadlan sawirkan daawada ama warqadda dhakhtarka si degdeg ah u eeg, magaca daawada, xanuunka loo qaato, xaddiga iyo sida loo isticmaalo cod ahaan ugu sharax bukaanka.",
    "Afaan Oromoo": "Mee suuraa qorichaa yookaan waraqaa qorichaa kana ilaaliitii, maqaa qorichaa, dhibee inni fayyisu, akkamitti akka fudhatamu sagaleedhaan ibsi.",
    "Amharic": "እባክዎን ይህንን የመድኃኒት ወይም የሐኪም ማዘዣ ፎቶ ይመልከቱ፣ የመድኃኒቱን ስም፣ የሚሰጠውን ጥቅም፣ የአወሳሰድ መመሪያውን በድምፅ በግልፅ ያስረዱ።",
    "English": "Please inspect this prescription or medication image, state the medicine name, condition it treats, exact dosage schedule, and precautions aloud."
}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    query_params = dict(websocket.query_params)
    lang = query_params.get("lang", "Af-Soomaali")
    
    session_state = OpenCareSessionState(session_id=str(id(websocket)), initial_lang=lang)
    print(f"🔌 [CONNECTED] Master Intelligent Duplex Session Started. Lang: {lang} | Voice: Aoede")

    system_instruction = OPENCAREAI_INTELLIGENT_SYSTEM_PROMPT.format(active_language=lang)

    live_config = types.LiveConnectConfig(
        response_modalities=[types.Modality.AUDIO],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name="Aoede"
                )
            )
        ),
        system_instruction=types.Content(
            parts=[types.Part.from_text(text=system_instruction)]
        )
    )

    try:
        async with client.aio.live.connect(model=LIVE_MODEL_NAME, config=live_config) as session:
            print(f"✅ [SESSION ACTIVE] Gemini 3.1 Flash Live Connected in {lang}")
            session_alive = True

            async def outbound_loop():
                nonlocal session_alive
                try:
                    while session_alive:
                        async for response in session.receive():
                            server_content = response.server_content
                            if server_content is not None:
                                if server_content.interrupted:
                                    await websocket.send_text(json.dumps({"type": "interrupted"}))
                                    continue

                                if server_content.model_turn is not None:
                                    for part in server_content.model_turn.parts:
                                        if part.inline_data and part.inline_data.data:
                                            await websocket.send_bytes(part.inline_data.data)

                                if server_content.turn_complete:
                                    print(f"🔄 [TURN COMPLETED] Finished turn in {session_state.active_language}.")
                                    await websocket.send_text(json.dumps({"type": "turn_complete"}))
                        
                        await asyncio.sleep(0.05)
                except asyncio.CancelledError:
                    pass
                except Exception as e:
                    print(f"⚠️ Outbound loop closed: {e}")
                    session_alive = False

            async def inbound_loop():
                nonlocal session_alive
                frame_count = 0
                try:
                    while session_alive:
                        msg = await websocket.receive()

                        if "bytes" in msg and msg["bytes"]:
                            frame_count += 1
                            if frame_count % 50 == 0:
                                print(f"🎙️ [STREAMING MIC] Chunk #{frame_count} ({len(msg['bytes'])} bytes)")

                            await session.send_realtime_input(
                                audio=types.Blob(
                                    data=msg["bytes"],
                                    mime_type="audio/pcm;rate=16000"
                                )
                            )
                            await asyncio.sleep(0.001)

                        elif "text" in msg and msg["text"]:
                            data = json.loads(msg["text"])
                            
                            # Location-based Emergency Lookup Query
                            if data.get("type") == "location_query":
                                loc = data.get("location", "")
                                contact = lookup_emergency_contact(loc)
                                if contact:
                                    await websocket.send_text(json.dumps({
                                        "type": "emergency_contact",
                                        "contact": contact
                                    }))

                            # Visual Multimodal OCR
                            elif data.get("type") == "image":
                                img_bytes = base64.b64decode(data.get("data", ""))
                                mime = data.get("mime", "image/jpeg")
                                print(f"📷 [PRESCRIPTION OCR] Ingesting visual frame ({len(img_bytes)} bytes)...")

                                session_state.record_visual_analysis("Uploaded prescription or medical document", mime)

                                await session.send_realtime_input(
                                    video=types.Blob(
                                        data=img_bytes,
                                        mime_type=mime
                                    )
                                )

                                prompt_text = IMAGE_PROMPTS.get(session_state.active_language, IMAGE_PROMPTS["Af-Soomaali"])
                                await session.send(
                                    input=prompt_text,
                                    end_of_turn=True
                                )
                except (WebSocketDisconnect, asyncio.CancelledError):
                    session_alive = False
                except Exception as e:
                    print(f"⚠️ Inbound loop error: {e}")
                    session_alive = False

            outbound_task = asyncio.create_task(outbound_loop())
            inbound_task = asyncio.create_task(inbound_loop())

            await asyncio.gather(inbound_task, outbound_task, return_exceptions=True)

    except WebSocketDisconnect:
        print("🔌 [CLOSED] Client WebSocket closed cleanly.")
    except Exception as e:
        print(f"❌ Gemini Live Session Error: {e}")
        traceback.print_exc()

def get_static_path(file_name: str):
    for candidate in ["public", "backend/public"]:
        full_path = os.path.join(candidate, file_name)
        if os.path.exists(full_path):
            return full_path
    return os.path.join("public", file_name)

@app.get("/")
async def serve_root():
    return FileResponse(get_static_path("index.html"), headers={"Cache-Control": "no-cache, no-store, must-revalidate"})

@app.get("/{file_name:path}")
async def serve_static(file_name: str):
    file_path = get_static_path(file_name)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    return FileResponse(get_static_path("index.html"), headers={"Cache-Control": "no-cache, no-store, must-revalidate"})

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, ws_ping_interval=25, ws_ping_timeout=35)
