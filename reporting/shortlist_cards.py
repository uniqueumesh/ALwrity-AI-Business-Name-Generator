from typing import List
import streamlit as st
from core.schemas import NameCard


def render_name_cards(cards: List[NameCard]) -> None:
    if not cards:
        st.info("No names to display yet.")
        return
    for card in cards:
        with st.container(border=True):
            st.subheader(card.candidate.text)
            st.caption(f"Territory: {card.candidate.territory}")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Pronounceability", f"{card.scores.pronounceability:.2f}")
                st.metric("Spellability", f"{card.scores.spellability:.2f}")
            with col2:
                st.metric("Distinctiveness", f"{card.scores.distinctiveness:.2f}")
                st.metric("Uniqueness", f"{card.scores.seo_uniqueness:.2f}")
            with col3:
                st.metric("Availability", f"{card.scores.domain_handle:.2f}")
                st.metric("Confusion Risk", f"{card.scores.confusion_risk:.2f}")
            if card.pr_headline_notes:
                st.write(card.pr_headline_notes)
            # Evidence
            evidence = getattr(card, "evidence", None)
            if evidence:
                with st.expander("Evidence"):
                    st.write("EXA URLs:")
                    for url in evidence.exa_urls:
                        st.markdown(f"- [{url}]({url})")
                    st.write("Domain:")
                    st.write(f"{evidence.domain.domain} → {'available' if evidence.domain.available else 'taken'}")
                    st.write("Handles:")
                    for h in evidence.handles:
                        st.write(f"{h.network}: @{h.handle} → {'exists' if h.exists else 'free'}")


