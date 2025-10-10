import os
from typing import List

import streamlit as st

from core.config import load_configuration_or_fail
from core.orchestrator import Orchestrator
from reporting.shortlist_cards import render_name_cards
from ui_prompt_editor import render_prompt_editor


def _init_session_state() -> None:
    if "wizard_step" not in st.session_state:
        st.session_state["wizard_step"] = 0


def _steps() -> List[str]:
    return [
        "Brief",
        "Territories",
        "Generate",
        "Checks",
        "Shortlist",
        "Package",
    ]


def _render_stepper() -> None:
    steps = _steps()
    st.sidebar.header("Steps")
    st.session_state["wizard_step"] = st.sidebar.radio(
        label="Navigate",
        options=list(range(len(steps))),
        index=st.session_state["wizard_step"],
        format_func=lambda i: f"{i+1}. {steps[i]}",
    )


def _nav_buttons() -> None:
    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("Back", use_container_width=True, disabled=st.session_state["wizard_step"] == 0):
            st.session_state["wizard_step"] = max(0, st.session_state["wizard_step"] - 1)
            st.rerun()
    with col_next:
        if st.button(
            "Next",
            use_container_width=True,
            disabled=st.session_state["wizard_step"] >= len(_steps()) - 1,
        ):
            # Persist selections when advancing steps
            current_step = _steps()[st.session_state["wizard_step"]]
            if current_step == "Territories":
                st.session_state["territories_confirmed"] = st.session_state.get("territories_selected", []) or []
            st.session_state["wizard_step"] = min(len(_steps()) - 1, st.session_state["wizard_step"] + 1)
            st.rerun()


def _render_brief():
    st.subheader("Brief")
    st.text_input(
        "Business description",
        key="brief_description",
        placeholder="Example: AI bookkeeping app for freelancers; automates invoicing and tax estimates",
        help="Describe what the business does in 1–2 sentences."
    )
    st.text_area(
        "Audience/markets",
        key="brief_markets",
        placeholder="Example: Primary audience: US freelancers and small agencies. Markets: en-US (United States)",
        help="Who is this for and where will the name be used?"
    )
    st.text_input(
        "Tone (e.g., modern, warm)",
        key="brief_tone",
        placeholder="Example: warm, modern, trustworthy",
        help="Pick 2–4 tone words that fit your brand personality."
    )
    st.text_area(
        "Do/Don't words",
        key="brief_do_dont",
        placeholder="Example: Do: clear, simple, short. Don't: buzzwords, hard-to-spell, hyphens",
        help="List words or patterns you want to include or avoid."
    )
    st.text_area(
        "Competitors (comma-separated)",
        key="brief_competitors",
        placeholder="Example: QuickBooks, FreshBooks, Wave",
        help="Names of competitors or similar products (comma-separated)."
    )
    st.caption("Tip: You can refine prompts anytime via the Prompt Editor below.")


def _render_territories():
    st.subheader("Territories")
    st.multiselect(
        "Select 3–5 territories",
        ["Pioneer", "Sage", "Minimalist", "Nature-Tech", "Precision", "Human Warmth", "Futurist", "Craft"],
        key="territories_selected",
        help="Territories are creative lanes. Example: 'Minimalist' = clean and simple; 'Sage' = wise and trustworthy.",
    )


def _render_generate():
    st.subheader("Generate Candidates")
    st.info("Generation will use Gemini 2.5 Flash (prompts) plus morphology.")
    territories = (
        st.session_state.get("territories_confirmed")
        or st.session_state.get("territories_selected")
        or []
    )
    use_structured = st.checkbox("Use structured output (JSON)", value=True, help="Return names+rationales as JSON from Gemini.")
    if territories:
        st.caption(f"Selected territories: {', '.join(territories)}")
    else:
        st.warning("No territories selected. Please go back and choose 3–5 territories.")
    if st.button("Generate", key="btn_generate"):
        if not territories:
            st.warning("Please select territories first.")
            return
        orch = Orchestrator.from_env()
        # Gather prompt context from Brief step
        tone = st.session_state.get("brief_tone", "")
        do_dont = st.session_state.get("brief_do_dont", "")
        constraints = st.session_state.get("brief_description", "")
        with st.spinner("Generating names..."):
            st.session_state["generated_candidates"] = orch.generate_candidates(
                territories,
                per_territory=10,
                use_structured=use_structured,
            )
        cands = st.session_state.get("generated_candidates", []) or []
        st.success(f"Generated {len(cands)} candidates.")
        if cands:
            preview = [c.text for c in cands[:20]]
            st.write("Preview:")
            st.write(", ".join(preview))


def _render_checks():
    st.subheader("Run Checks")
    st.info("Will run EXA uniqueness, domains (GoDaddy/RDAP), handles, phonetics/safety. Placeholder for now.")
    if st.button("Run Checks", key="btn_checks"):
        candidates = st.session_state.get("generated_candidates", []) or []
        if not candidates:
            st.warning("No candidates generated yet.")
            return
        orch = Orchestrator.from_env()
        with st.spinner("Running checks (web uniqueness, domains, handles)..."):
            st.session_state["name_cards"] = orch.run_checks(candidates)
        cards = st.session_state.get("name_cards", []) or []
        st.success(f"Checks complete for {len(cards)} candidates.")


def _render_shortlist():
    st.subheader("Shortlist")
    cards = st.session_state.get("name_cards", []) or []
    render_name_cards(cards)


def _render_package():
    st.subheader("Package")
    st.write("Export CSV/JSON/PDF with rationale and evidence. CSV export available.")
    cards = st.session_state.get("name_cards", []) or []
    if cards:
        from reporting.export_csv import to_csv
        from reporting.export_json import to_json

        csv_bytes = to_csv(cards)
        st.download_button(
            label="Download CSV",
            data=csv_bytes,
            file_name="shortlist.csv",
            mime="text/csv",
        )
        json_bytes = to_json(cards)
        st.download_button(
            label="Download JSON",
            data=json_bytes,
            file_name="shortlist.json",
            mime="application/json",
        )


def main() -> None:
    st.set_page_config(page_title="ALwrity Name Generator", layout="wide")
    load_configuration_or_fail()
    _init_session_state()
    _render_stepper()

    step = _steps()[st.session_state["wizard_step"]]
    st.title(f"{step}")

    if step == "Brief":
        _render_brief()
    elif step == "Territories":
        _render_territories()
    elif step == "Generate":
        _render_generate()
    elif step == "Checks":
        _render_checks()
    elif step == "Shortlist":
        _render_shortlist()
    elif step == "Package":
        _render_package()

    st.divider()
    _nav_buttons()
    with st.expander("Prompt Editor"):
        render_prompt_editor()


if __name__ == "__main__":
    main()


