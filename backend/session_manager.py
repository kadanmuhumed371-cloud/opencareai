from typing import Dict, Any, Optional

class OpenCareSessionState:
    def __init__(self, session_id: str, initial_lang: str = "Af-Soomaali"):
        self.session_id = session_id
        self.active_language = initial_lang
        self.current_service = "GENERAL_HEALTH"  # FIRST_AID, VISUAL_ASSISTANCE, MOTHER_CHILD, SYMPTOM_ASSESSMENT, REALTIME_TRANSLATION
        self.is_emergency = False
        
        # Clinical Context Memory
        self.patient_profile = {
            "demographic": None,  # man, woman, pregnant_mother, infant, child
            "age": None,
            "main_complaint": None,
            "symptoms": [],
            "duration": None,
            "medications_mentioned": [],
            "location": None
        }
        
        # Translation State Machine
        self.translation_state = {
            "is_active": False,
            "person_a": {"role": None, "language": None},
            "person_b": {"role": None, "language": None},
            "current_direction": None, # e.g. "somali_to_amharic"
            "history": []
        }
        
        # Visual OCR Cache
        self.last_visual_context: Optional[Dict[str, Any]] = None

    def update_language(self, new_lang: str):
        if new_lang in ["Af-Soomaali", "Afaan Oromoo", "Amharic", "English"]:
            self.active_language = new_lang

    def set_translation_session(self, person_a_role: str, person_a_lang: str, person_b_role: str, person_b_lang: str):
        self.translation_state["is_active"] = True
        self.translation_state["person_a"] = {"role": person_a_role, "language": person_a_lang}
        self.translation_state["person_b"] = {"role": person_b_role, "language": person_b_lang}
        self.current_service = "REALTIME_TRANSLATION"

    def record_visual_analysis(self, image_summary: str, mime_type: str):
        self.last_visual_context = {
            "summary": image_summary,
            "mime_type": mime_type
        }
