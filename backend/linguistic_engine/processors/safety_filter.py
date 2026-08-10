from linguistic_engine.utils.json_loader import load_json_collection

class SafetyFilter:
    def __init__(self):
        self.messages = load_json_collection('safety_messages.json')

    def process(self, text: str) -> str:
        disclaimer = ""
        for msg in self.messages:
            if msg.get('key') == 'disclaimer' and msg.get('enabled', True):
                disclaimer = msg.get('text', '')
                break
                
        if disclaimer:
            # Prepend the disclaimer
            return f"{disclaimer}\n\n{text}"
        return text
