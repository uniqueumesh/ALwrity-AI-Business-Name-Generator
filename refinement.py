"""
Refinement module for ALwrity AI Business Name Generator
Handles user feedback and iterative name refinement
"""
import streamlit as st
from datetime import datetime
from generator import generate_business_names


def initialize_refinement_state():
    """Initialize session state for refinement functionality"""
    if 'name_sets' not in st.session_state:
        st.session_state['name_sets'] = []
    if 'refinement_count' not in st.session_state:
        st.session_state['refinement_count'] = 0
    if 'current_feedback' not in st.session_state:
        st.session_state['current_feedback'] = ""


def add_name_set(names, label, feedback=None):
    """Add a new name set to session state"""
    name_set = {
        'id': f"set_{len(st.session_state['name_sets'])}",
        'label': label,
        'names': names,
        'timestamp': datetime.now().strftime("%I:%M %p"),
        'feedback': feedback
    }
    st.session_state['name_sets'].append(name_set)
    return name_set


def get_original_parameters():
    """Get original generation parameters from session state"""
    if 'original_params' not in st.session_state:
        return None
    return st.session_state['original_params']


def store_original_parameters(business_description, name_length, name_style, 
                            include_keywords, exclude_keywords, alliteration, 
                            target_audience, api_key, num_names):
    """Store original generation parameters for refinement"""
    st.session_state['original_params'] = {
        'business_description': business_description,
        'name_length': name_length,
        'name_style': name_style,
        'include_keywords': include_keywords,
        'exclude_keywords': exclude_keywords,
        'alliteration': alliteration,
        'target_audience': target_audience,
        'api_key': api_key,
        'num_names': num_names
    }


def create_enhanced_prompt(original_description, feedback, previous_names):
    """Create enhanced prompt for refinement"""
    enhanced_description = f"{original_description}\n\nUser feedback: {feedback}"
    
    if previous_names:
        enhanced_description += f"\n\nPrevious names to avoid repeating: {', '.join(previous_names[:5])}"
    
    return enhanced_description


def process_refinement(feedback, original_params):
    """Process user feedback and generate refined names"""
    if not feedback.strip():
        return None, "Please provide feedback to refine the suggestions."
    
    if not original_params:
        return None, "No original parameters found. Please generate names first."
    
    try:
        # Create enhanced description
        previous_names = []
        for name_set in st.session_state['name_sets']:
            previous_names.extend(name_set['names'])
        
        enhanced_description = create_enhanced_prompt(
            original_params['business_description'], 
            feedback, 
            previous_names
        )
        
        # Generate refined names
        refined_names = generate_business_names(
            enhanced_description,
            original_params['name_length'],
            original_params['name_style'],
            original_params['include_keywords'],
            original_params['exclude_keywords'],
            original_params['alliteration'],
            original_params['target_audience'],
            original_params['api_key'],
            original_params['num_names']
        )
        
        if refined_names:
            # Split names into list
            names_list = [name.strip() for name in refined_names.split('\n') if name.strip()]
            
            # Add to name sets
            st.session_state['refinement_count'] += 1
            label = f"Refined Names #{st.session_state['refinement_count']}"
            add_name_set(names_list, label, feedback)
            
            return names_list, "✅ Names refined based on your feedback!"
        else:
            return None, "Failed to refine names. Please try again."
            
    except Exception as e:
        return None, f"Error during refinement: {str(e)}"


def render_refinement_section():
    """Render the refinement section UI"""
    if not st.session_state['name_sets']:
        return
    
    st.markdown('<h4 style="margin-top:2rem; color:#1976D2;">🔄 Refine Your Suggestions</h4>', unsafe_allow_html=True)
    st.markdown("Don't like these names? Tell us what you like and what to change!")
    
    # Feedback text area
    feedback = st.text_area(
        "Your feedback (optional)",
        value=st.session_state['current_feedback'],
        placeholder="e.g., I like the tech feel but want shorter names. Avoid words ending in 'ly'. More creative combinations please.",
        help="Provide specific feedback about what you like or dislike about the generated names.",
        key="refinement_input"
    )
    
    # Update current feedback in session state
    st.session_state['current_feedback'] = feedback
    
    # Buttons
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("**Refine Suggestions**", type="secondary"):
            original_params = get_original_parameters()
            refined_names, message = process_refinement(feedback, original_params)
            
            if refined_names:
                st.success(message)
                st.rerun()
            else:
                st.error(message)
    
    with col2:
        if st.button("**Clear Feedback**", type="secondary"):
            st.session_state['current_feedback'] = ""
            st.rerun()


def render_name_sets():
    """Render all name sets with proper labeling and copy functionality"""
    if not st.session_state['name_sets']:
        return
    
    st.markdown('<h4 style="margin-top:1.5rem; color:#1976D2;">🎯 Generated Business Names</h4>', unsafe_allow_html=True)
    st.info("💡 **Tip**: Click on any name to copy it, or use the code blocks on the right for easy selection!")
    
    # Render each name set
    for i, name_set in enumerate(st.session_state['name_sets']):
        # Set header with timestamp
        if name_set['label'] == 'Original Names':
            st.markdown(f'<h5 style="color:#1976D2; margin-top:1rem;">📋 {name_set["label"]} (Generated at {name_set["timestamp"]})</h5>', unsafe_allow_html=True)
        else:
            st.markdown(f'<h5 style="color:#2E7D32; margin-top:1rem;">🔄 {name_set["label"]} (Generated at {name_set["timestamp"]})</h5>', unsafe_allow_html=True)
        
        # Display names with copy functionality
        for j, name in enumerate(name_set['names']):
            col1, col2 = st.columns([4, 1])
            with col1:
                # Clickable name with copy functionality
                st.markdown(f"""
                <div style="padding: 8px; border: 1px solid #e0e0e0; border-radius: 5px; margin: 5px 0; cursor: pointer; background-color: #f8f9fa;" 
                     onclick="navigator.clipboard.writeText('{name}'); this.style.backgroundColor='#d4edda'; setTimeout(() => this.style.backgroundColor='#f8f9fa', 1000);">
                    <strong>{j+1}.</strong> {name}
                </div>
                """, unsafe_allow_html=True)
            with col2:
                # Code block for easy selection
                st.code(name, language=None)
        
        # Show feedback for refined sets
        if name_set.get('feedback'):
            with st.expander(f"💬 Feedback for {name_set['label']}", expanded=False):
                st.write(name_set['feedback'])
        
        # Add separator between sets
        if i < len(st.session_state['name_sets']) - 1:
            st.markdown("---")
    
    # Plain text section for bulk copying
    st.markdown("---")
    st.markdown("**Plain text (select all to copy):**")
    all_names = []
    for name_set in st.session_state['name_sets']:
        all_names.extend([f"{name_set['label']}: {name}" for name in name_set['names']])
    st.code('\n'.join(all_names), language=None)


def clear_all_refinements():
    """Clear all refinements and keep only original names"""
    if len(st.session_state['name_sets']) > 1:
        # Keep only the first (original) set
        original_set = st.session_state['name_sets'][0]
        st.session_state['name_sets'] = [original_set]
        st.session_state['refinement_count'] = 0
        st.session_state['current_feedback'] = ""
        st.success("✅ Cleared all refinements. Showing original names only.")
        st.rerun()


def add_clear_all_button():
    """Add clear all refinements button if there are multiple sets"""
    if len(st.session_state['name_sets']) > 1:
        st.markdown("---")
        if st.button("🗑️ **Clear All Refinements**", type="secondary"):
            clear_all_refinements()
