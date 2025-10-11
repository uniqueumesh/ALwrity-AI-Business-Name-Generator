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
import pandas as pd
import io
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

    # Number of names to generate
    st.markdown('<h3 style="margin-top:2rem;">How many business names do you want to generate?</h3>', unsafe_allow_html=True)
    num_names = st.slider(
        'Number of business names', 
        min_value=5, 
        max_value=20, 
        value=10,
        help="Choose how many unique business names to generate (5-20)."
    )

    # --- Exa Research Preview ---
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
            st.markdown('<h4 style="margin-top:1.5rem; color:#1976D2;">🔎 Similar Businesses Found</h4>', unsafe_allow_html=True)
            st.success(f"Found {len(exa_research_data)} similar businesses to inspire unique names.")
            
            with st.expander("View Research Data"):
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
        
        # Export functionality
        st.markdown("---")
        st.markdown('<h3>📥 Export Your Names</h3>', unsafe_allow_html=True)
        
        col_exp1, col_exp2 = st.columns(2)
        
        # Create export dataframe
        export_df = pd.DataFrame({'Business Name': names_list})
        
        excel_buffer = io.BytesIO()
        export_df.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0)
        
        col_exp1.download_button(
            label="📊 Download as Excel",
            data=excel_buffer,
            file_name="business_names.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # CSV export
        csv_buffer = io.StringIO()
        export_df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        
        col_exp2.download_button(
            label="📄 Download as CSV",
            data=csv_data,
            file_name="business_names.csv",
            mime="text/csv"
        )


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
    if exa_data and exa_data not in ['RATE_LIMIT', 'ERROR']:
        exa_context = "\n\nSimilar businesses for inspiration (DO NOT COPY these names):\n"
        for item in exa_data[:5]:
            exa_context += f"- {item.get('title', 'N/A')}\n"
    
    # Build comprehensive prompt
    prompt = f"""
You are a creative brand naming expert. Generate {num_names} unique, memorable business names.

Business Information:
- Keywords: {keywords}
- Industry: {industry}
- Style Preference: {name_style}
{f'- Description: {description}' if description else ''}
{f'- Target Audience: {target_audience}' if target_audience else ''}

{exa_context}

Requirements:
1. Each name must be COMPLETELY UNIQUE - not used by any existing business
2. Names should be memorable, brandable, and easy to pronounce
3. Keep names between 1-3 words
4. Avoid generic or overly descriptive names
5. Consider these style preferences: {name_style}
6. Make names appropriate for the {industry} industry
7. Names should resonate with the target audience
8. Prefer names that could have available .com domains
9. Mix different naming strategies:
   - Invented/coined words (e.g., Spotify, Xerox)
   - Compound words (e.g., Facebook, Netflix)
   - Modified real words (e.g., Flickr, Tumblr)
   - Metaphorical names (e.g., Amazon, Apple)
10. DO NOT copy or closely imitate the similar business names listed above

Output Format:
List exactly {num_names} business names, one per line.
Do not include numbering, explanations, or any other text.
Just the names.
"""
    
    generation_config = {
        "temperature": 0.9,  # Higher creativity for unique names
        "top_p": 0.95,
        "top_k": 40,
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

