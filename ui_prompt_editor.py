import streamlit as st
from prompts.prompt_registry import get_prompt, save_override


def render_prompt_editor() -> None:
    st.subheader("Prompt Editor (Preview)")
    key = st.selectbox(
        "Select prompt",
        options=["strategy_brief", "territories", "generation", "rationale"],
        index=0,
    )
    template = get_prompt(key)
    content_key = f"prompt_{key}"
    st.text_area("Template", value=template, height=200, key=content_key)
    if st.button("Save override", key=f"save_{key}"):
        save_override(key, st.session_state[content_key])
        st.success("Saved. Overrides take effect immediately.")


