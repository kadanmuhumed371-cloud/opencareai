import re

def clean_ai_text(text: str) -> str:
    """
    Cleans up raw AI text output.
    Removes markdown formatting, excessive whitespaces, and standardizes punctuation.
    """
    if not text:
        return ""
        
    # Remove markdown bold/italic
    text = re.sub(r'[*_]{1,2}', '', text)
    
    # Standardize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
