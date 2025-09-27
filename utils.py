"""
Utility functions for ALwrity AI Business Name Generator
"""
from config import PROBLEMATIC_WORDS, WORD_REPLACEMENTS


def sanitize_input(text):
    """Clean input text to avoid safety filter triggers with enhanced sanitization"""
    if not text:
        return ""
    
    # Convert to lowercase for checking
    text_lower = text.lower()
    
    # Enhanced word replacements for business terms
    enhanced_replacements = {
        'kill': 'eliminate',
        'death': 'end',
        'die': 'stop',
        'dead': 'inactive',
        'hate': 'dislike',
        'scam': 'service',
        'fake': 'alternative',
        'steal': 'acquire',
        'hack': 'optimize',
        'crack': 'access',
        'violence': 'action',
        'weapon': 'tool',
        'gun': 'device',
        'bomb': 'explosive',
        'murder': 'eliminate',
        'drug': 'medicine',
        'alcohol': 'beverage',
        'tobacco': 'product',
        'gambling': 'entertainment',
        'casino': 'venue',
        'betting': 'prediction',
        'lottery': 'game',
        'adult': 'mature',
        'porn': 'content',
        'sex': 'gender',
        'nude': 'bare',
        'explicit': 'clear',
        'mature': 'adult',
        'fraud': 'service',
        'deception': 'strategy',
        'trick': 'method',
        'cheat': 'advantage',
        'pirate': 'copy',
        'illegal': 'unauthorized',
        'unauthorized': 'unapproved',
        'stolen': 'acquired'
    }
    
    # Replace problematic words with safer alternatives
    cleaned_text = text
    for word, replacement in enhanced_replacements.items():
        if word in text_lower:
            cleaned_text = cleaned_text.replace(word, replacement)
            cleaned_text = cleaned_text.replace(word.title(), replacement.title())
            cleaned_text = cleaned_text.replace(word.upper(), replacement.upper())
    
    # Additional business-specific cleaning
    business_cleaners = {
        'eco-friendly': 'environmentally conscious',
        'sustainable': 'environmentally responsible',
        'green': 'environmental',
        'organic': 'natural',
        'natural': 'pure',
        'pure': 'clean',
        'clean': 'fresh',
        'fresh': 'new',
        'new': 'modern',
        'modern': 'contemporary',
        'contemporary': 'current',
        'current': 'present',
        'present': 'now',
        'now': 'today',
        'today': 'current'
    }
    
    for word, replacement in business_cleaners.items():
        if word in text_lower:
            cleaned_text = cleaned_text.replace(word, replacement)
            cleaned_text = cleaned_text.replace(word.title(), replacement.title())
            cleaned_text = cleaned_text.replace(word.upper(), replacement.upper())
    
    # Remove any remaining problematic words
    words = cleaned_text.split()
    safe_words = [word for word in words if word.lower() not in PROBLEMATIC_WORDS]
    
    return ' '.join(safe_words).strip()
