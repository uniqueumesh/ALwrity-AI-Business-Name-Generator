import time
import os
import json
import streamlit as st
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)


def main():
    # Set page configuration
    st.set_page_config(
        page_title="ALwrity AI Business Name Generator",
        layout="wide",
    )
    # Remove the extra spaces from margin top.
    st.markdown("""
        <style>
        ::-webkit-scrollbar-track {
        background: #e1ebf9;
        }

        ::-webkit-scrollbar-thumb {
            background-color: #90CAF9;
            border-radius: 10px;
            border: 3px solid #e1ebf9;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #64B5F6;
        }

        ::-webkit-scrollbar {
            width: 16px;
        }
        div.stButton > button:first-child {
            background: #1565C0;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 10px 2px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            font-weight: bold;
        }
        </style>
    """
    , unsafe_allow_html=True)

    # Hide top header line
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    # Hide footer
    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)

    st.title("🏢 ALwrity - AI Business Name Generator")

    # --- API Key Input Section (moved below title) ---
    with st.expander("API Configuration 🔑", expanded=False):
        st.markdown('''If the default Gemini API key is unavailable or exceeds its limits, you can provide your own API key below.<br>
        <a href="https://aistudio.google.com/app/apikey" target="_blank">Get Gemini API Key</a>
        ''', unsafe_allow_html=True)
        user_gemini_api_key = st.text_input("Gemini API Key", type="password", help="Paste your Gemini API Key here if you have one. Otherwise, the tool will use the default key if available.")

    # Input section
    with st.expander("**PRO-TIP** - Follow the steps below for best results.", expanded=True):
        col1, col2 = st.columns([5, 5])

        with col1:
            input_business_description = st.text_area(
                '**🏢 Describe your business!**',
                placeholder="e.g., An online subscription box for eco-friendly home products",
                help="Provide a short description of your business, what you do, and your target market."
            )
            input_include_keywords = st.text_input(
                '**🔑 Include Keywords (Optional)**',
                placeholder="e.g., eco, green, sustainable, home",
                help="Add specific words you want to include in the business names."
            )
            input_exclude_keywords = st.text_input(
                '**❌ Exclude Keywords (Optional)**',
                placeholder="e.g., tech, digital, online",
                help="Add words you want to avoid in the business names."
            )

        with col2:
            input_name_length = st.selectbox(
                '📏 Name Length', 
                ('Short (4-7 characters)', 'Medium (7-11 characters)', 'Long (11-16 characters)'),
                index=1
            )
            input_name_style = st.selectbox(
                '🎨 Name Style', 
                ('Professional', 'Modern', 'Creative', 'Funny', 'Custom'), 
                index=1
            )
            input_alliteration = st.checkbox(
                '🔤 Prefer Alliteration',
                help="Generate names where the first letters of words match (e.g., 'Blue Bird Bakery')"
            )
            input_target_audience = st.text_input(
                '🎯 Target Audience (Optional)',
                placeholder="e.g., Small businesses, Tech startups, Health enthusiasts",
                help="Specify your target audience for more tailored names."
            )

    # Add option for number of names
    st.markdown('<h3 style="margin-top:2rem;">How many business names do you want to generate?</h3>', unsafe_allow_html=True)
    num_names = st.slider('Number of business names', min_value=5, max_value=50, value=20, help="Choose how many business names to generate (5-50).")

    # Generate Business Names button
    if st.button('**Generate Business Names**'):
        with st.spinner("Generating business names..."):
            if not input_business_description:
                st.error('**🫣 Please provide a business description to generate names!**')
            else:
                business_names = generate_business_names(
                    input_business_description, 
                    input_name_length, 
                    input_name_style, 
                    input_include_keywords, 
                    input_exclude_keywords, 
                    input_alliteration, 
                    input_target_audience, 
                    user_gemini_api_key, 
                    num_names
                )
                if business_names:
                    st.session_state['business_names'] = business_names
                else:
                    st.error("💥 **Failed to generate business names. Please try again!**")
            
            if 'business_names' in st.session_state:
                st.markdown('<h4 style="margin-top:1.5rem; color:#1976D2;">🎯 Generated Business Names</h4>', unsafe_allow_html=True)
                st.markdown(st.session_state['business_names'])

    # Refinement section
    if 'business_names' in st.session_state and st.session_state['business_names']:
        st.markdown('<h4 style="margin-top:2rem; color:#1976D2;">🔄 Refine Your Suggestions</h4>', unsafe_allow_html=True)
        st.markdown("Don't like these names? Tell us what you like and what to change!")
        
        refinement_feedback = st.text_area(
            "Your feedback (optional)",
            placeholder="e.g., I like the tech feel but want shorter names. Avoid words ending in 'ly'. More creative combinations please.",
            help="Provide specific feedback about what you like or dislike about the generated names."
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("**Refine Suggestions**", type="secondary"):
                if refinement_feedback:
                    with st.spinner("Refining business names based on your feedback..."):
                        refined_names = generate_business_names(
                            f"{input_business_description}\n\nUser feedback: {refinement_feedback}", 
                            input_name_length, 
                            input_name_style, 
                            input_include_keywords, 
                            input_exclude_keywords, 
                            input_alliteration, 
                            input_target_audience, 
                            user_gemini_api_key, 
                            num_names
                        )
                        if refined_names:
                            st.session_state['business_names'] = refined_names
                            st.success("✅ Names refined based on your feedback!")
                            st.rerun()
                        else:
                            st.error("Failed to refine names. Please try again.")
                else:
                    st.warning("Please provide feedback to refine the suggestions.")
        with col2:
            if st.button("**Clear Feedback**", type="secondary"):
                st.rerun()


def sanitize_input(text):
    """Clean input text to avoid safety filter triggers"""
    if not text:
        return ""
    
    # Remove potentially problematic words/phrases
    problematic_words = [
        'kill', 'death', 'die', 'dead', 'murder', 'violence', 'weapon', 'gun', 'bomb',
        'hate', 'racist', 'discrimination', 'offensive', 'inappropriate', 'illegal',
        'drug', 'alcohol', 'tobacco', 'gambling', 'casino', 'betting', 'lottery',
        'adult', 'porn', 'sex', 'nude', 'explicit', 'mature', '18+',
        'scam', 'fraud', 'fake', 'deception', 'trick', 'cheat', 'steal',
        'hack', 'crack', 'pirate', 'illegal', 'unauthorized', 'stolen'
    ]
    
    # Convert to lowercase for checking
    text_lower = text.lower()
    
    # Replace problematic words with safer alternatives
    replacements = {
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
    
    cleaned_text = text
    for word, replacement in replacements.items():
        if word in text_lower:
            cleaned_text = cleaned_text.replace(word, replacement)
            cleaned_text = cleaned_text.replace(word.title(), replacement.title())
            cleaned_text = cleaned_text.replace(word.upper(), replacement.upper())
    
    # Remove any remaining problematic words
    words = cleaned_text.split()
    safe_words = [word for word in words if word.lower() not in problematic_words]
    
    return ' '.join(safe_words).strip()


def generate_business_names(business_description, name_length, name_style, include_keywords, exclude_keywords, alliteration, target_audience, user_gemini_api_key=None, num_names=20):
    """ Function to call upon LLM to get the work done. """
    
    # Map length options
    length_mapping = {
        'Short (4-7 characters)': 'short',
        'Medium (7-11 characters)': 'medium', 
        'Long (11-16 characters)': 'long'
    }
    length_instruction = length_mapping.get(name_length, 'medium')
    
    # Clean and sanitize inputs to avoid safety filters
    clean_description = sanitize_input(business_description)
    clean_include = sanitize_input(include_keywords) if include_keywords else 'None specified'
    clean_exclude = sanitize_input(exclude_keywords) if exclude_keywords else 'None specified'
    clean_audience = sanitize_input(target_audience) if target_audience else 'General audience'
    
    # Further refined prompt for best results
    seo_guidelines = f"""
Create {num_names} professional business names for a company.

Business Type: {clean_description}
Name Length: {length_instruction}
Style: {name_style.lower()}
Include Words: {clean_include}
Avoid Words: {clean_exclude}
Target Market: {clean_audience}
Alliteration: {alliteration}

Requirements:
- Generate {num_names} unique business names
- Each name should be {length_instruction} length
- Style should be {name_style.lower()}
- Names must be professional and brandable
- Easy to pronounce and remember
- Suitable for business registration
- Avoid generic or common terms
- Include relevant keywords when possible
- Consider target audience preferences

Output format: List each business name on a separate line, no numbering or explanations.
"""
    
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


def generate_local_names(business_description, name_length, name_style, include_keywords, exclude_keywords, alliteration, target_audience, num_names=20):
    """ Fallback local name generation when API fails """
    import random
    
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
    
    # Common business suffixes and prefixes
    suffixes = ['Labs', 'Works', 'Studio', 'Group', 'Co', 'Corp', 'Inc', 'LLC', 'Solutions', 'Services', 'Tech', 'Digital', 'Creative', 'Innovation', 'Hub', 'Space', 'Place', 'Center', 'Point', 'Edge', 'Flow', 'Wave', 'Spark', 'Bright', 'Sharp', 'Quick', 'Fast', 'Smart', 'Pro', 'Plus', 'Max', 'Prime', 'Elite', 'Gold', 'Silver', 'Blue', 'Green', 'Red', 'White', 'Black']
    
    prefixes = ['Pro', 'Ultra', 'Super', 'Mega', 'Micro', 'Mini', 'Max', 'Prime', 'Elite', 'Gold', 'Silver', 'Blue', 'Green', 'Red', 'White', 'Black', 'Bright', 'Sharp', 'Quick', 'Fast', 'Smart', 'New', 'Next', 'Future', 'Modern', 'Digital', 'Tech', 'Creative', 'Innovation', 'Advanced', 'Premium', 'Ultimate', 'Perfect', 'Best', 'Top', 'First', 'Leading', 'Master', 'Expert', 'Pro', 'Plus', 'Max', 'Prime', 'Elite']
    
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
            prefix = random.choice(prefixes)
            if alliteration and keyword[0] == prefix[0]:
                name = f"{prefix}{keyword.title()}"
            elif not alliteration:
                name = f"{prefix}{keyword.title()}"
            else:
                continue
                
        elif method == 'suffix' and keywords:
            # Add suffix to keyword
            keyword = random.choice(keywords)
            suffix = random.choice(suffixes)
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
        generic_names = ['InnovateCorp', 'SmartWorks', 'ProSolutions', 'EliteGroup', 'PrimeTech', 'BrightIdeas', 'QuickStart', 'FastTrack', 'SharpEdge', 'BlueWave', 'GreenSpace', 'RedPoint', 'WhiteCloud', 'BlackDiamond', 'GoldStandard', 'SilverLining', 'BlueOcean', 'GreenTech', 'RedBull', 'WhitePaper']
        name = random.choice(generic_names)
        if name not in names:
            names.append(name)
    
    return '\n'.join(names[:num_names])


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def gemini_text_response(prompt, user_gemini_api_key=None):
    import google.generativeai as genai
    import os
    try:
        api_key = user_gemini_api_key or os.getenv('GEMINI_API_KEY')
        if not api_key:
            st.error("GEMINI_API_KEY is missing. Please provide it in the API Configuration section or set it in the environment.")
            return None
        genai.configure(api_key=api_key)
    except Exception as err:
        st.error(f"Failed to configure Gemini: {err}")
        return None
    
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.8,
        "top_k": 40,
        "max_output_tokens": 2048
    }
    model = genai.GenerativeModel(model_name="gemini-2.5-flash", generation_config=generation_config)
    
    try:
        response = model.generate_content(prompt)
        
        # Check for rate limiting
        if hasattr(response, 'code') and response.code == 429:
            return 'RATE_LIMIT'
            
        # Check if response has valid content
        if not response or not hasattr(response, 'candidates'):
            st.warning("No response received from Gemini. Please try again.")
            return None
            
        if not response.candidates:
            st.warning("Empty response from Gemini. Please try again.")
            return None
            
        # Check finish reason
        candidate = response.candidates[0]
        if hasattr(candidate, 'finish_reason'):
            if candidate.finish_reason == 2:  # SAFETY
                st.warning("Content was blocked by safety filters. Please try with different inputs.")
                return None
            elif candidate.finish_reason == 3:  # RECITATION
                st.warning("Content was blocked due to recitation. Please try with different inputs.")
                return None
            elif candidate.finish_reason == 4:  # OTHER
                st.warning("Content generation was stopped. Please try again.")
                return None
        
        # Safely extract text content
        try:
            if hasattr(response, 'text') and response.text:
                text_content = response.text.strip()
                if text_content:
                    return text_content
                else:
                    st.warning("Empty text content received. Please try again.")
                    return None
            else:
                # Try alternative method to get text
                if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                    text_parts = []
                    for part in candidate.content.parts:
                        if hasattr(part, 'text') and part.text:
                            text_parts.append(part.text)
                    if text_parts:
                        return '\n'.join(text_parts).strip()
                
                st.warning("No valid text content in response. Please try again.")
                return None
                
        except Exception as text_err:
            st.warning(f"Error extracting text: {text_err}. Please try again.")
            return None
            
    except Exception as err:
        error_msg = str(err).lower()
        if 'quota' in error_msg or 'rate limit' in error_msg:
            return 'RATE_LIMIT'
        elif 'safety' in error_msg or 'blocked' in error_msg:
            st.warning("Content was blocked by safety filters. Please try with different inputs.")
            return None
        else:
            st.warning(f"API error: {err}. Retrying...")
            return None


if __name__ == "__main__":
    main()
