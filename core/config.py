import os
from dataclasses import dataclass
from typing import Optional, Dict

try:
    # Load local .env if present (no-op if missing)
    from dotenv import load_dotenv  # type: ignore

    load_dotenv()
except Exception:
    # dotenv is optional; absence should not crash
    pass

try:
    import streamlit as st
except Exception:  # pragma: no cover
    st = None  # type: ignore


REQUIRED_KEYS = ("GEMINI_API_KEY", "EXA_API_KEY", "GODADDY_KEY", "GODADDY_SECRET")


@dataclass(frozen=True)
class AppConfig:
    gemini_api_key: str
    exa_api_key: str
    godaddy_key: str
    godaddy_secret: str


def _get_secret(name: str) -> Optional[str]:
    # Streamlit secrets take precedence when available
    if st is not None:
        try:
            if hasattr(st, "secrets") and name in st.secrets:
                value = str(st.secrets[name])
                if value:
                    return value
        except Exception:
            pass
    # Fallback to environment variables
    value = os.getenv(name)
    return value if value else None


def load_configuration_or_fail() -> AppConfig:
    missing = [k for k in REQUIRED_KEYS if not _get_secret(k)]
    if missing:
        message = (
            "Missing required environment keys: " + ", ".join(missing) +
            ". Configure these in .env (local) or Streamlit secrets (Cloud)."
        )
        if st is not None:
            st.error(message)
            st.stop()
        raise RuntimeError(message)

    cfg = AppConfig(
        gemini_api_key=_get_secret("GEMINI_API_KEY") or "",
        exa_api_key=_get_secret("EXA_API_KEY") or "",
        godaddy_key=_get_secret("GODADDY_KEY") or "",
        godaddy_secret=_get_secret("GODADDY_SECRET") or "",
    )
    return cfg


