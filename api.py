"""
API communication module for ALwrity AI Business Name Generator
"""
import os
import streamlit as st
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_random_exponential
from config import GEMINI_MODEL, GENERATION_CONFIG, MAX_RETRY_ATTEMPTS, RETRY_WAIT_MIN, RETRY_WAIT_MAX


@retry(wait=wait_random_exponential(min=RETRY_WAIT_MIN, max=RETRY_WAIT_MAX), stop=stop_after_attempt(MAX_RETRY_ATTEMPTS))
def gemini_text_response(prompt, user_gemini_api_key=None):
    """Handle Gemini API communication with robust error handling"""
    try:
        api_key = user_gemini_api_key or os.getenv('GEMINI_API_KEY')
        if not api_key:
            st.error("GEMINI_API_KEY is missing. Please provide it in the API Configuration section or set it in the environment.")
            return None
        genai.configure(api_key=api_key)
    except Exception as err:
        st.error(f"Failed to configure Gemini: {err}")
        return None
    
    model = genai.GenerativeModel(model_name=GEMINI_MODEL, generation_config=GENERATION_CONFIG)
    
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
