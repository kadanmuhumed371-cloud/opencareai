import re
from linguistic_engine.utils.json_loader import load_json_collection

class VocabularyProcessor:
    def __init__(self):
        self.rules = load_json_collection('custom_vocabulary.json')

    def process(self, text: str) -> str:
        for rule in self.rules:
            original = rule.get('original', '')
            tts_version = rule.get('tts_version', '')
            if original and tts_version:
                pattern = re.compile(rf'\b{re.escape(original)}\b', re.IGNORECASE)
                text = pattern.sub(tts_version, text)
        return text
