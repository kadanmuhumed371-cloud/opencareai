import re
from linguistic_engine.utils.json_loader import load_json_collection

class PhoneticProcessor:
    def __init__(self):
        self.rules = load_json_collection('phonetic_rules.json')
        # Build a dictionary and a single regex pattern for simultaneous replacement
        # Sort by length descending so 'dh' matches before 'd'
        sorted_rules = sorted(self.rules, key=lambda x: len(x.get('pattern', '')), reverse=True)
        self.replacements = {r['pattern'].lower(): r['tts_pronunciation'] for r in sorted_rules if r.get('pattern') and r.get('tts_pronunciation')}
        
        if self.replacements:
            # Create a pattern that matches any of the keys
            escaped_keys = [re.escape(k) for k in self.replacements.keys()]
            self.pattern = re.compile(r'(' + '|'.join(escaped_keys) + r')', re.IGNORECASE)
        else:
            self.pattern = None

    def process(self, text: str) -> str:
        if not self.pattern:
            return text
            
        def match_func(match):
            word = match.group(0)
            # Find the replacement
            rep = self.replacements.get(word.lower(), word)
            # Preserve case loosely
            if word.isupper():
                return rep.upper()
            elif word.istitle():
                return rep.capitalize()
            return rep
            
        return self.pattern.sub(match_func, text)
