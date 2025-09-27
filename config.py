# Configuration settings for ALwrity AI Business Name Generator

# API Configuration
GEMINI_MODEL = "gemini-2.5-flash"
GENERATION_CONFIG = {
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 2048
}

# Retry Configuration
MAX_RETRY_ATTEMPTS = 6
RETRY_WAIT_MIN = 1
RETRY_WAIT_MAX = 60

# Name Generation Settings
DEFAULT_NUM_NAMES = 20
MIN_NAMES = 5
MAX_NAMES = 50

# Length Mappings
LENGTH_MAPPING = {
    'Short (4-7 characters)': 'short',
    'Medium (7-11 characters)': 'medium', 
    'Long (11-16 characters)': 'long'
}

# Business Name Components
BUSINESS_SUFFIXES = [
    'Labs', 'Works', 'Studio', 'Group', 'Co', 'Corp', 'Inc', 'LLC', 
    'Solutions', 'Services', 'Tech', 'Digital', 'Creative', 'Innovation', 
    'Hub', 'Space', 'Place', 'Center', 'Point', 'Edge', 'Flow', 'Wave', 
    'Spark', 'Bright', 'Sharp', 'Quick', 'Fast', 'Smart', 'Pro', 'Plus', 
    'Max', 'Prime', 'Elite', 'Gold', 'Silver', 'Blue', 'Green', 'Red', 
    'White', 'Black'
]

BUSINESS_PREFIXES = [
    'Pro', 'Ultra', 'Super', 'Mega', 'Micro', 'Mini', 'Max', 'Prime', 
    'Elite', 'Gold', 'Silver', 'Blue', 'Green', 'Red', 'White', 'Black', 
    'Bright', 'Sharp', 'Quick', 'Fast', 'Smart', 'New', 'Next', 'Future', 
    'Modern', 'Digital', 'Tech', 'Creative', 'Innovation', 'Advanced', 
    'Premium', 'Ultimate', 'Perfect', 'Best', 'Top', 'First', 'Leading', 
    'Master', 'Expert', 'Pro', 'Plus', 'Max', 'Prime', 'Elite'
]

# Generic Fallback Names
GENERIC_NAMES = [
    'InnovateCorp', 'SmartWorks', 'ProSolutions', 'EliteGroup', 'PrimeTech', 
    'BrightIdeas', 'QuickStart', 'FastTrack', 'SharpEdge', 'BlueWave', 
    'GreenSpace', 'RedPoint', 'WhiteCloud', 'BlackDiamond', 'GoldStandard', 
    'SilverLining', 'BlueOcean', 'GreenTech', 'RedBull', 'WhitePaper'
]

# Problematic words for safety filtering
PROBLEMATIC_WORDS = [
    'kill', 'death', 'die', 'dead', 'murder', 'violence', 'weapon', 'gun', 'bomb',
    'hate', 'racist', 'discrimination', 'offensive', 'inappropriate', 'illegal',
    'drug', 'alcohol', 'tobacco', 'gambling', 'casino', 'betting', 'lottery',
    'adult', 'porn', 'sex', 'nude', 'explicit', 'mature', '18+',
    'scam', 'fraud', 'fake', 'deception', 'trick', 'cheat', 'steal',
    'hack', 'crack', 'pirate', 'illegal', 'unauthorized', 'stolen'
]

# Word replacements for safety
WORD_REPLACEMENTS = {
    'kill': 'eliminate',
    'death': 'end',
    'die': 'stop',
    'dead': 'inactive',
    'hate': 'dislike',
    'scam': 'service',
    'fake': 'alternative',
    'steal': 'acquire',
    'hack': 'optimize',
    'crack': 'access'
}

# Style-specific prompt templates for enhanced name generation
STYLE_TEMPLATES = {
    'professional': """
STYLE: PROFESSIONAL
Focus on trust, reliability, and corporate appeal. Names should convey:
- Authority and expertise
- Trustworthiness and stability
- Corporate professionalism
- Industry leadership
- Sophisticated and polished tone
- Suitable for B2B and enterprise markets
""",
    'modern': """
STYLE: MODERN
Focus on innovation, technology, and contemporary appeal. Names should convey:
- Cutting-edge technology
- Innovation and progress
- Digital-first approach
- Contemporary and trendy
- Tech-savvy and forward-thinking
- Appeal to younger demographics
""",
    'creative': """
STYLE: CREATIVE
Focus on imagination, uniqueness, and artistic appeal. Names should convey:
- Creative and artistic flair
- Unique and memorable
- Innovative thinking
- Artistic and expressive
- Stand out from competition
- Appeal to creative industries
""",
    'funny': """
STYLE: FUNNY
Focus on humor, playfulness, and memorable quirkiness. Names should convey:
- Humor and personality
- Memorable and fun
- Approachable and friendly
- Stand out with humor
- Appeal to casual markets
- Create positive associations
""",
    'custom': """
STYLE: CUSTOM
Focus on unique requirements and specific brand personality. Names should convey:
- Unique brand identity
- Specific market positioning
- Customized approach
- Distinctive character
- Tailored to specific needs
- Stand out in the market
"""
}
