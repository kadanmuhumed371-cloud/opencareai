import re
from linguistic_engine.utils.json_loader import load_json_collection

class NumberProcessor:
    def __init__(self):
        self.rules = load_json_collection('number_corrections.json')

    def process(self, text: str) -> str:
        for rule in self.rules:
            detected = rule.get('detected', '')
            replace_with = rule.get('replace_with', '')
            if detected and replace_with:
                # Use word boundaries and ignore case for robust replacement
                pattern = re.compile(rf'\b{re.escape(detected)}\b', re.IGNORECASE)
                text = pattern.sub(replace_with, text)
        return text
