"""
Main application module for ALwrity AI Business Name Generator
"""
import streamlit as st
from generator import generate_business_names
from refinement import (
    initialize_refinement_state, 
    store_original_parameters, 
    add_name_set, 
    render_name_sets, 
    render_refinement_section,
    add_clear_all_button
)


def main():
    """Main application entry point"""
    # Set page configuration
    st.set_page_config(
        page_title="ALwrity AI Business Name Generator",
        layout="wide",
    )
    
    # Initialize refinement state
    initialize_refinement_state()
    
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
        </style>
    """, unsafe_allow_html=True)

    # Hide top header line
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    # Hide footer
    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)

    st.title("🏢 ALwrity - AI Business Name Generator")

    # --- API Key Input Section ---
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
                # Store original parameters for refinement
                store_original_parameters(
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
                    # Split names into list
                    names_list = [name.strip() for name in business_names.split('\n') if name.strip()]
                    
                    # Clear existing name sets and add new original set
                    st.session_state['name_sets'] = []
                    st.session_state['refinement_count'] = 0
                    add_name_set(names_list, "Original Names")
                    
                    st.success("✅ Business names generated successfully!")
                else:
                    st.error("💥 **Failed to generate business names. Please try again!**")
    
    # Render name sets (original + refinements)
    render_name_sets()
    
    # Render refinement section
    render_refinement_section()
    
    # Add clear all button if there are refinements
    add_clear_all_button()



if __name__ == "__main__":
    main()
