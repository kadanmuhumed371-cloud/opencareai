import re
from linguistic_engine.utils.json_loader import load_json_collection

class MedicalSimplifier:
    def __init__(self):
        self.rules = load_json_collection('medical_simplification.json')

    def process(self, text: str) -> str:
        for rule in self.rules:
            term = rule.get('technical_term', '')
            simple = rule.get('simple_somali', '')
            if term and simple:
                pattern = re.compile(rf'\b{re.escape(term)}\b', re.IGNORECASE)
                text = pattern.sub(simple, text)
        return text
