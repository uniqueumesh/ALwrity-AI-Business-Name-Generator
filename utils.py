"""
Utility functions for ALwrity AI Business Name Generator
"""
from config import PROBLEMATIC_WORDS, WORD_REPLACEMENTS


def sanitize_input(text):
    """Clean input text to avoid safety filter triggers"""
    if not text:
        return ""
    
    # Convert to lowercase for checking
    text_lower = text.lower()
    
    # Replace problematic words with safer alternatives
    cleaned_text = text
    for word, replacement in WORD_REPLACEMENTS.items():
        if word in text_lower:
            cleaned_text = cleaned_text.replace(word, replacement)
            cleaned_text = cleaned_text.replace(word.title(), replacement.title())
            cleaned_text = cleaned_text.replace(word.upper(), replacement.upper())
    
    # Remove any remaining problematic words
    words = cleaned_text.split()
    safe_words = [word for word in words if word.lower() not in PROBLEMATIC_WORDS]
    
    return ' '.join(safe_words).strip()
