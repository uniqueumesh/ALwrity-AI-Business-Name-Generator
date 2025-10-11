import time
import os
import sys
import json
import warnings

# Suppress all warnings and Google library verbose output
warnings.filterwarnings('ignore')
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '3'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['GRPC_TRACE'] = ''
os.environ['GRPC_VERBOSITY'] = 'NONE'

# Redirect stderr temporarily to suppress C++ library warnings
import io as _io
_stderr = sys.stderr
sys.stderr = _io.StringIO()

import streamlit as st
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
from dotenv import load_dotenv

# Restore stderr after imports
sys.stderr = _stderr

# Load environment variables
load_dotenv()

# Additional suppression for absl logging (used by Google libraries)
try:
    import absl.logging
    absl.logging.set_verbosity('error')
    absl.logging.set_stderrthreshold('error')
except ImportError:
    pass


def main():
    # Set page configuration
    st.set_page_config(
        page_title="Alwrity - AI Business Name Generator",
        layout="wide",
    )
    
    # Custom CSS styling
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
        
        div.stButton > button:hover {
            background: #0D47A1;
        }
        </style>
    """, unsafe_allow_html=True)

    # Hide top header line
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    # Hide footer
    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)

    st.title("✨ Alwrity - AI Business Name Generator")
    
    st.markdown("""
        <p style="font-size: 1.1rem; color: #666;">
        Generate unique, brandable business names powered by AI research and creativity.
        </p>
    """, unsafe_allow_html=True)

    # Input section
    with st.expander("**PRO-TIP** - Follow the steps below for best results.", expanded=True):
        col1, col2 = st.columns([5, 5])

        with col1:
            input_business_keywords = st.text_input(
                '**🔑 Enter your business keywords**',
                placeholder="e.g., AI productivity, eco-friendly fashion, coffee shop",
                help="Describe your business in 2-4 words. Be specific about your industry or niche."
            )
            
            business_description = st.text_area(
                '**📝 Business Description (Optional)**',
                placeholder="e.g., A mobile app that helps freelancers track time and manage invoices...",
                help="Optional: Provide more details about your business for better name suggestions."
            )

        with col2:
            industry_options = [
                "General",
                "Technology/Software",
                "E-commerce/Retail",
                "Health & Wellness",
                "Food & Beverage",
                "Education",
                "Finance",
                "Creative/Agency",
                "Consulting",
                "Other"
            ]
            input_industry = st.selectbox(
                '🏢 Industry', 
                industry_options,
                index=0,
                help="Select your industry for more relevant name suggestions."
            )
            
            name_style_options = [
                "Modern & Brandable",
                "Professional & Corporate",
                "Creative & Unique",
                "Short & Catchy",
                "Descriptive & Clear"
            ]
            input_name_style = st.selectbox(
                '🎨 Name Style',
                name_style_options,
                index=0,
                help="Choose the style/tone for your business name."
            )
            
            input_target_audience = st.text_input(
                '🎯 Target Audience (Optional)',
                placeholder="e.g., millennials, small businesses, parents",
                help="Who is your primary customer? This helps tailor the name."
            )

        with col2:
            num_names = st.selectbox(
                '📊 Number of business names', 
                options=[5, 10, 15, 20],
                index=1,  # Default to 10
                help="Choose how many unique business names to generate."
            )

    # --- Exa Research Preview (Collapsible) ---
    exa_research_data = []
    exa_cache_key = f"exa_{input_business_keywords}"
    
    if input_business_keywords:
        if exa_cache_key in st.session_state:
            exa_research_data = st.session_state[exa_cache_key]
        else:
            with st.spinner("🔍 Researching similar businesses..."):
                exa_research_data = get_exa_research(input_business_keywords)
                st.session_state[exa_cache_key] = exa_research_data
        
        if exa_research_data == 'RATE_LIMIT':
            st.warning('⚠️ Exa API rate limit or quota exceeded. Please try again later or use a different API key.')
            exa_research_data = []
        elif exa_research_data and exa_research_data != 'ERROR':
            with st.expander(f"🔎 Similar Businesses Found ({len(exa_research_data)} businesses)", expanded=False):
                st.success(f"Found {len(exa_research_data)} similar businesses to inspire unique names.")
                st.caption("This data helps the AI create unique names that stand out from competitors.")
                
                for idx, item in enumerate(exa_research_data[:5], 1):
                    st.write(f"**{idx}. {item.get('title', 'N/A')}**")
                    st.write(f"*{item.get('url', 'N/A')}*")
                    if item.get('text'):
                        st.write(item['text'][:200] + "...")
                    st.divider()
        elif exa_research_data == 'ERROR':
            st.info('Could not fetch research data. Check your Exa API key or try different keywords.')
            exa_research_data = []

    # Generate Business Names button
    if st.button('**🚀 Generate Business Names**'):
        if not input_business_keywords:
            st.error('**🫣 Please provide business keywords to generate names!**')
        else:
            with st.spinner("✨ Generating unique business names..."):
                business_names = generate_business_names(
                    input_business_keywords,
                    business_description,
                    exa_research_data,
                    input_industry,
                    input_name_style,
                    input_target_audience,
                    num_names
                )
                
                if business_names and business_names != 'RATE_LIMIT':
                    st.session_state['business_names'] = business_names
                elif business_names == 'RATE_LIMIT':
                    st.error("💥 **Gemini API rate limit exceeded. Please try again later or use a different API key!**")
                else:
                    st.error("💥 **Failed to generate business names. Please try again!**")

    # Display results
    if 'business_names' in st.session_state and st.session_state['business_names']:
        st.markdown("---")
        st.markdown('<h2 style="color:#1565C0;">🎉 Generated Business Names</h2>', unsafe_allow_html=True)
        
        names_list = [n.strip().lstrip('0123456789. -*') for n in st.session_state['business_names'].split('\n') if n.strip()]
        
        # Display names in a clean card format
        for idx, name in enumerate(names_list, 1):
            st.markdown(f"### {idx}. {name}")


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_exa_research(keywords):
    """
    Fetch similar businesses using Exa API for research and context.
    """
    try:
        from exa_py import Exa
        
        api_key = os.getenv('EXA_API_KEY')
        if not api_key:
            st.error("EXA_API_KEY is missing. Please add it to your .env file.")
            return 'ERROR'
        
        exa = Exa(api_key=api_key)
        
        # Search query for similar businesses
        search_query = f"{keywords} business company startup brand"
        
        # Perform search
        search_results = exa.search_and_contents(
            query=search_query,
            type="neural",
            use_autoprompt=True,
            num_results=10,
            text=True
        )
        
        # Extract relevant data
        research_data = []
        for result in search_results.results:
            research_data.append({
                'title': result.title,
                'url': result.url,
                'text': result.text[:500] if result.text else ""
            })
        
        return research_data
        
    except Exception as err:
        error_msg = str(err).lower()
        if 'rate limit' in error_msg or 'quota' in error_msg or '429' in error_msg:
            return 'RATE_LIMIT'
        st.error(f"Exa API error: {err}")
        return 'ERROR'


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_business_names(keywords, description, exa_data, industry, name_style, target_audience, num_names=10):
    """
    Generate unique business names using Gemini 2.0 Flash LLM with Exa research context.
    """
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            st.error("GEMINI_API_KEY is missing. Please add it to your .env file.")
            return None
        
        genai.configure(api_key=api_key)
        
    except Exception as err:
        st.error(f"Failed to configure Gemini: {err}")
        return None
    
    # Build context from Exa research
    exa_context = ""
    competitor_names = []
    if exa_data and exa_data not in ['RATE_LIMIT', 'ERROR']:
        exa_context = "\n\n🚫 EXISTING COMPETITORS (AVOID these names and similar patterns):\n"
        for item in exa_data[:5]:
            name = item.get('title', 'N/A')
            competitor_names.append(name)
            exa_context += f"- {name}\n"
        exa_context += "\n⚠️ DO NOT create names that sound like, rhyme with, or follow the same pattern as these competitors.\n"
    
    # Build comprehensive prompt with stronger uniqueness emphasis
    prompt = f"""
You are an EXPERT brand naming consultant with 20 years of experience creating memorable, unique business names for Fortune 500 companies.

🎯 YOUR MISSION:
Create {num_names} HIGHLY UNIQUE, NEVER-BEFORE-USED business names that stand out in the market.

📋 BUSINESS CONTEXT:
- Core Keywords: {keywords}
- Industry: {industry}
- Brand Style: {name_style}
{f'- Business Description: {description}' if description else ''}
{f'- Target Audience: {target_audience}' if target_audience else ''}

{exa_context}

🔥 CRITICAL UNIQUENESS RULES:
1. ❌ NEVER use common business suffixes like: "Solutions", "Tech", "Labs", "Pro", "Hub", "Soft", "Ware", "Group", "Systems"
2. ❌ NEVER combine keywords directly (e.g., if keywords are "AI productivity", don't create "AIProductivity" or "ProductiveAI")
3. ❌ NEVER use generic industry terms (e.g., avoid "Cloud", "Data", "Smart", "Digital", "Cyber", "Net", "Web" unless disguised creatively)
4. ✅ CREATE names that sound COMPLETELY NEW and INVENTED
5. ✅ Each name must pass this test: "If I Google this, will I find ZERO existing businesses with this exact name?"

🎨 ADVANCED NAMING TECHNIQUES (Use these):

A) **Morpheme Fusion** - Blend meaningful word parts creatively:
   - Combine Latin/Greek roots: "Velo" (speed) + "rium" = Velorium
   - Mix languages: "Kai" (Japanese: change) + "zen" = Kaizen ❌ (already exists) → Try: Kaivos, Zenova
   
B) **Vowel Play** - Change vowels in familiar words:
   - "Stream" → Stryam, Straem, Strym
   - "Focus" → Fycus, Focys, Foqus
   
C) **Phonetic Invention** - Create pleasing sound combinations:
   - Strong consonants + soft vowels: Zephora, Kymera, Vexara
   - Rhythmic patterns: Lumino, Navigo, Vivaro
   
D) **Conceptual Metaphors** - Use unexpected concepts from nature, mythology, or science:
   - Space/Cosmos: Quasar, Nebula, Zenith (but make them unique: Quasro, Nebulyx, Zenithos)
   - Nature: Redwood, Summit (but make them unique: Redwyx, Summyt, Oakenly)
   
E) **Prefix/Suffix Invention** - Create new affixes:
   - Instead of "-ly" use "-io", "-ax", "-yn": Swiftio, Rapidax, Claryn
   - Instead of "Tech-" use "Zyn-", "Vex-", "Nyx-": Zynflow, Vexcore, Nyxsphere

🎯 NAME QUALITY CHECKLIST (Every name must pass):
✅ Pronounceable in under 3 seconds
✅ Memorable after hearing once
✅ No negative meanings in major languages
✅ .com domain likely available (short, unique)
✅ Sounds professional yet distinctive
✅ Works well as a logo/brand
✅ NOT similar to competitors listed above
✅ Passes the "Google test" - appears nowhere

💡 INDUSTRY-SPECIFIC GUIDELINES for {industry}:
- If Tech: Focus on speed, intelligence, innovation - but AVOID clichés
- If Health: Focus on care, vitality, trust - but avoid medical jargon
- If Finance: Focus on security, growth, clarity - but avoid banking terms
- If E-commerce: Focus on accessibility, value, experience - but avoid "shop/store/mart"
- If Creative: Focus on imagination, craft, vision - but avoid "studio/design/creative"

🎨 STYLE ADAPTATION for "{name_style}":
- Modern & Brandable: Clean, tech-forward, minimal (e.g., Vercel, Notion) → Create similar but unique
- Professional & Corporate: Strong, trustworthy, established → But with a twist
- Creative & Unique: Unexpected, artistic, memorable → Push boundaries further
- Short & Catchy: 1-2 syllables, punchy, fun → Like Stripe, Figma but different
- Descriptive & Clear: Hint at function, but do it cleverly → Not literally

🚀 CREATIVE CHALLENGES:
1. At least 30% of names should be COMPLETELY INVENTED words (like Xerox, Kodak, Etsy)
2. At least 30% should use unexpected word combinations (like Snapchat, Dropbox but more unique)
3. At least 30% should be metaphorical/abstract (like Apple, Amazon but more creative)
4. Remaining 10% can be modified real words (like Flickr, Tumblr but more distinct)

⚡ FINAL VERIFICATION:
Before outputting each name, mentally check:
- "Does this sound like it could already exist?" → If YES, make it MORE unique
- "Is this too generic or obvious?" → If YES, add creative twist
- "Would this stand out in a list of 100 companies?" → If NO, make it bolder

📤 OUTPUT FORMAT:
List exactly {num_names} business names, one per line.
NO numbering, NO explanations, NO domains, NO descriptions.
ONLY the pure business names.
Each name should be 1-3 words maximum.
"""
    
    generation_config = {
        "temperature": 1.0,  # Maximum creativity for truly unique names
        "top_p": 0.98,       # Allow more diverse token selection
        "top_k": 64,         # Wider selection pool for creativity
        "max_output_tokens": 2048
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config
    )
    
    try:
        response = model.generate_content(prompt)
        
        if hasattr(response, 'code') and response.code == 429:
            return 'RATE_LIMIT'
        
        if hasattr(response, 'text'):
            if 'rate limit' in response.text.lower() or 'quota' in response.text.lower():
                return 'RATE_LIMIT'
            return response.text
        
        return None
        
    except Exception as err:
        error_msg = str(err).lower()
        if 'quota' in error_msg or 'rate limit' in error_msg or '429' in error_msg:
            return 'RATE_LIMIT'
        st.error(f"Failed to get response from Gemini: {err}")
        return None


if __name__ == "__main__":
    main()

