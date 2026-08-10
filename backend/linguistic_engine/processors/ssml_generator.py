class SSMLGenerator:
    def process(self, text: str) -> str:
        """
        Wraps text in SSML tags and adds pauses for emergency pacing.
        """
        # Split text into sentences for pacing
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        ssml_parts = ["<speak>"]
        
        for sentence in sentences:
            if "Fiiro Gaar Ah:" in sentence:
                # Add emphasis and longer pause for disclaimer
                ssml_parts.append(f"{sentence}.")
                ssml_parts.append('<break time="600ms"/>')
            elif "marka koowaad" in sentence.lower() or "marka labaad" in sentence.lower():
                # Add pause after steps
                ssml_parts.append(f"{sentence},")
                ssml_parts.append('<break time="400ms"/>')
            else:
                ssml_parts.append(f"{sentence}.")
                ssml_parts.append('<break time="300ms"/>')
                
        ssml_parts.append("</speak>")
        return "\n".join(ssml_parts)
