"""
Business name generation module for ALwrity AI Business Name Generator
"""
import random
import streamlit as st
from api import gemini_text_response
from utils import sanitize_input
from config import (
    LENGTH_MAPPING, BUSINESS_SUFFIXES, BUSINESS_PREFIXES, 
    GENERIC_NAMES, DEFAULT_NUM_NAMES, STYLE_TEMPLATES
)


def create_enhanced_prompt(description, length, style, include_words, exclude_words, audience, alliteration, num_names):
    """Create style-specific enhanced prompts for better name generation with safety-filter-friendly language"""
    
    # Get style-specific template
    style_template = STYLE_TEMPLATES.get(style.lower(), STYLE_TEMPLATES['professional'])
    
    # Safety-filter-friendly prompt structure
    prompt = f"""Create {num_names} business names for a company.

Company Description: {description}
Target Market: {audience}
Name Length: {length}
Style: {style.lower()}
Keywords to Include: {include_words}
Keywords to Avoid: {exclude_words}
Alliteration: {alliteration}

{style_template}

Requirements:
- Generate {num_names} unique business names
- Each name should be {length} length
- Style should be {style.lower()}
- Names must be professional and brandable
- Easy to pronounce and remember
- Suitable for business registration
- Avoid generic or common terms
- Include relevant keywords when possible
- Consider target audience preferences

Output format: List each business name on a separate line, no numbering or explanations.

Examples of successful business names in this style:
{get_style_examples(style.lower())}

Generate {num_names} business names:"""
    
    return prompt


def get_style_examples(style):
    """Get style-specific examples for better AI understanding"""
    examples = {
        'professional': [
            "Accenture (Accent + Future)",
            "Microsoft (Micro + Soft)", 
            "Verizon (Veritas + Horizon)",
            "Oracle (Oracle of Delphi)"
        ],
        'modern': [
            "Spotify (Spot + Identify)",
            "Uber (German for 'above')",
            "Airbnb (Air + Bed + Breakfast)",
            "Tesla (Nikola Tesla)"
        ],
        'creative': [
            "Google (Googol - mathematical term)",
            "Amazon (Largest river)",
            "Apple (Simple, memorable)",
            "Nike (Greek goddess of victory)"
        ],
        'funny': [
            "Squatty Potty (Humor + Function)",
            "BarkBox (Dog + Subscription)",
            "DuckDuckGo (Privacy + Fun)",
            "MailChimp (Email + Monkey)"
        ]
    }
    
    example_list = examples.get(style, examples['professional'])
    return "\n".join([f"- {example}" for example in example_list])


def generate_business_names(business_description, name_length, name_style, include_keywords, exclude_keywords, alliteration, target_audience, user_gemini_api_key=None, num_names=DEFAULT_NUM_NAMES):
    """Main business name generation orchestrator"""
    
    # Map length options
    length_instruction = LENGTH_MAPPING.get(name_length, 'medium')
    
    # Clean and sanitize inputs to avoid safety filters
    clean_description = sanitize_input(business_description)
    clean_include = sanitize_input(include_keywords) if include_keywords else 'None specified'
    clean_exclude = sanitize_input(exclude_keywords) if exclude_keywords else 'None specified'
    clean_audience = sanitize_input(target_audience) if target_audience else 'General audience'
    
    # Create enhanced prompt for Gemini with style-specific templates
    seo_guidelines = create_enhanced_prompt(
        clean_description, length_instruction, name_style, 
        clean_include, clean_exclude, clean_audience, 
        alliteration, num_names
    )
    
    # Try Gemini first
    business_names = gemini_text_response(seo_guidelines, user_gemini_api_key)
    
    if business_names == 'RATE_LIMIT':
        st.warning('⚠️ Gemini API rate limit exceeded. Using local generation...')
        return generate_local_names(business_description, name_length, name_style, include_keywords, exclude_keywords, alliteration, target_audience, num_names)
    elif business_names is None:
        # Fallback to local generation
        st.info("🔄 Using local generation...")
        return generate_local_names(business_description, name_length, name_style, include_keywords, exclude_keywords, alliteration, target_audience, num_names)
    
    return business_names


def generate_local_names(business_description, name_length, name_style, include_keywords, exclude_keywords, alliteration, target_audience, num_names=DEFAULT_NUM_NAMES):
    """Fallback local name generation when API fails"""
    
    # Extract keywords from description
    words = business_description.lower().split()
    keywords = [w for w in words if len(w) > 3 and w.isalpha()]
    
    # Add include keywords
    if include_keywords:
        keywords.extend([w.strip() for w in include_keywords.split(',') if w.strip()])
    
    # Remove exclude keywords
    if exclude_keywords:
        exclude_list = [w.strip().lower() for w in exclude_keywords.split(',') if w.strip()]
        keywords = [w for w in keywords if w.lower() not in exclude_list]
    
    # Generate names
    names = []
    attempts = 0
    max_attempts = num_names * 3
    
    while len(names) < num_names and attempts < max_attempts:
        attempts += 1
        
        # Choose generation method
        method = random.choice(['compound', 'prefix', 'suffix', 'invented', 'alliteration'])
        
        if method == 'compound' and len(keywords) >= 2:
            # Combine two keywords
            word1, word2 = random.sample(keywords, 2)
            if alliteration and word1[0] == word2[0]:
                name = f"{word1.title()}{word2.title()}"
            elif not alliteration:
                name = f"{word1.title()}{word2.title()}"
            else:
                continue
                
        elif method == 'prefix' and keywords:
            # Add prefix to keyword
            keyword = random.choice(keywords)
            prefix = random.choice(BUSINESS_PREFIXES)
            if alliteration and keyword[0] == prefix[0]:
                name = f"{prefix}{keyword.title()}"
            elif not alliteration:
                name = f"{prefix}{keyword.title()}"
            else:
                continue
                
        elif method == 'suffix' and keywords:
            # Add suffix to keyword
            keyword = random.choice(keywords)
            suffix = random.choice(BUSINESS_SUFFIXES)
            if alliteration and keyword[0] == suffix[0]:
                name = f"{keyword.title()}{suffix}"
            elif not alliteration:
                name = f"{keyword.title()}{suffix}"
            else:
                continue
                
        elif method == 'invented':
            # Create invented name
            vowels = 'aeiou'
            consonants = 'bcdfghjklmnpqrstvwxyz'
            name_length_target = random.randint(4, 8)
            name = ''
            for i in range(name_length_target):
                if i % 2 == 0:
                    name += random.choice(consonants)
                else:
                    name += random.choice(vowels)
            name = name.title()
            
        elif method == 'alliteration' and len(keywords) >= 2:
            # Alliterative combination
            word1 = random.choice(keywords)
            word2 = random.choice([w for w in keywords if w[0] == word1[0]])
            if word2:
                name = f"{word1.title()}{word2.title()}"
            else:
                continue
        else:
            continue
        
        # Filter by length
        if name_length == 'Short (4-7 characters)' and len(name) > 7:
            continue
        elif name_length == 'Medium (7-11 characters)' and (len(name) < 7 or len(name) > 11):
            continue
        elif name_length == 'Long (11-16 characters)' and len(name) < 11:
            continue
        
        # Add to names if unique
        if name not in names and len(name) > 2:
            names.append(name)
    
    # If we don't have enough names, add some generic ones
    while len(names) < num_names:
        name = random.choice(GENERIC_NAMES)
        if name not in names:
            names.append(name)
    
    return '\n'.join(names[:num_names])
