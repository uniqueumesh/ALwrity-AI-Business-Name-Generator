from typing import Mapping


def render_prompt(template: str, variables: Mapping[str, str]) -> str:
    # Simple brace-based formatting with safe defaults
    class _SafeDict(dict):
        def __missing__(self, key):
            return "{" + key + "}"

    return template.format_map(_SafeDict(**variables))
