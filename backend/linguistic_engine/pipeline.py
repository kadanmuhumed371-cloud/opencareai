import re
from linguistic_engine.utils.text_cleaner import clean_ai_text
from linguistic_engine.processors.number_processor import NumberProcessor
from linguistic_engine.processors.medical_simplifier import MedicalSimplifier
from linguistic_engine.processors.vocabulary_processor import VocabularyProcessor
from linguistic_engine.processors.phonetic_processor import PhoneticProcessor
from linguistic_engine.processors.safety_filter import SafetyFilter
from linguistic_engine.processors.ssml_generator import SSMLGenerator

class SomaliLinguisticPipeline:
    def __init__(self):
        self.number_processor = NumberProcessor()
        self.medical_simplifier = MedicalSimplifier()
        self.vocabulary_processor = VocabularyProcessor()
        self.phonetic_processor = PhoneticProcessor()
        self.safety_filter = SafetyFilter()
        self.ssml_generator = SSMLGenerator()

    def process_somali_medical_response(self, text: str) -> str:
        """
        Main processing function to convert AI output to natural Somali TTS-ready SSML.
        """
        # 1. Clean text
        text = clean_ai_text(text)
        
        placeholders = {}
        counter = 0
        
        def protect(match):
            nonlocal counter
            word = match.group(0)
            token = f"__TOKEN_{counter}__"
            placeholders[token] = word
            counter += 1
            return token

        # 2. Number correction
        # We temporarily hijack the sub method to insert placeholders
        for rule in self.number_processor.rules:
            detected = rule.get('detected', '')
            replace_with = rule.get('replace_with', '')
            if detected and replace_with:
                pattern = re.compile(rf'\b{re.escape(detected)}\b', re.IGNORECASE)
                # protect the replaced string
                text = pattern.sub(lambda m, rw=replace_with: protect(re.match(r'.*', rw)), text)
        
        # 3. Medical simplification
        for rule in self.medical_simplifier.rules:
            term = rule.get('technical_term', '')
            simple = rule.get('simple_somali', '')
            if term and simple:
                pattern = re.compile(rf'\b{re.escape(term)}\b', re.IGNORECASE)
                text = pattern.sub(lambda m, sm=simple: protect(re.match(r'.*', sm)), text)
                
        # 5. Vocabulary replacement (User requested this order)
        for rule in self.vocabulary_processor.rules:
            original = rule.get('original', '')
            tts_version = rule.get('tts_version', '')
            if original and tts_version:
                pattern = re.compile(rf'\b{re.escape(original)}\b', re.IGNORECASE)
                text = pattern.sub(lambda m, tv=tts_version: protect(re.match(r'.*', tv)), text)

        # 4. Phonetic adaptation (Now it won't touch the replaced words)
        text = self.phonetic_processor.process(text)
        
        # Restore placeholders
        for token, word in placeholders.items():
            text = text.replace(token, word)
            
        # Add safety filter
        text = self.safety_filter.process(text)
        
        # 6. SSML enhancement
        final_ssml = self.ssml_generator.process(text)
        
        return final_ssml

def process_somali_medical_response(text: str) -> str:
    """Convenience function for the pipeline."""
    pipeline = SomaliLinguisticPipeline()
    return pipeline.process_somali_medical_response(text)
