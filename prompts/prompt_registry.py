from pathlib import Path
from typing import Dict

_PROMPTS: Dict[str, str] = {}

_BASE = Path(__file__).parent
_OVERRIDES = _BASE / ".overrides"


def _load_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _maybe_override(filename: str, default_text: str) -> str:
    override_path = _OVERRIDES / filename
    if override_path.exists():
        return _load_file(override_path)
    return default_text


def load_prompts() -> None:
    _OVERRIDES.mkdir(parents=True, exist_ok=True)
    _PROMPTS["strategy_brief"] = _maybe_override(
        "prompt_strategy_brief.txt",
        _load_file(_BASE / "prompt_strategy_brief.txt"),
    )
    _PROMPTS["territories"] = _maybe_override(
        "prompt_territories.txt",
        _load_file(_BASE / "prompt_territories.txt"),
    )
    _PROMPTS["generation"] = _maybe_override(
        "prompt_generation.txt",
        _load_file(_BASE / "prompt_generation.txt"),
    )
    _PROMPTS["rationale"] = _maybe_override(
        "prompt_rationale.txt",
        _load_file(_BASE / "prompt_rationale.txt"),
    )


def get_prompt(key: str) -> str:
    if not _PROMPTS:
        load_prompts()
    return _PROMPTS[key]


def save_override(key: str, content: str) -> None:
    filename_map = {
        "strategy_brief": "prompt_strategy_brief.txt",
        "territories": "prompt_territories.txt",
        "generation": "prompt_generation.txt",
        "rationale": "prompt_rationale.txt",
    }
    _OVERRIDES.mkdir(parents=True, exist_ok=True)
    filename = filename_map[key]
    path = _OVERRIDES / filename
    path.write_text(content, encoding="utf-8")
    # Refresh cache
    _PROMPTS.clear()
    load_prompts()
