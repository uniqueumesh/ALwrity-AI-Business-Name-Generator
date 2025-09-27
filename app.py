"""
Main application module for ALwrity AI Business Name Generator
"""
import streamlit as st
from generator import generate_business_names


def main():
    """Main application entry point"""
    # Set page configuration
    st.set_page_config(
        page_title="ALwrity AI Business Name Generator",
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
                
                # Split names and display in vertical format
                names_list = [name.strip() for name in st.session_state['business_names'].split('\n') if name.strip()]
                
                # Create a clean vertical list with copy buttons
                for i, name in enumerate(names_list):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"**{i+1}.** {name}")
                    with col2:
                        if st.button("📋", key=f"copy_{i}", help="Copy to clipboard"):
                            st.write("Copied!")
                
                # Also show as plain text for easy selection
                st.markdown("---")
                st.markdown("**Plain text (select all to copy):**")
                st.code('\n'.join(names_list), language=None)

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


if __name__ == "__main__":
    main()
