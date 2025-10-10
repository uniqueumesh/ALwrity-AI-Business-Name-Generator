import json
from typing import List

from core.schemas import NameCard


def to_json(cards: List[NameCard]) -> bytes:
    payload = [
        {
            "name": c.candidate.text,
            "territory": c.candidate.territory,
            "scores": {
                "distinctiveness": c.scores.distinctiveness,
                "pronounceability": c.scores.pronounceability,
                "spellability": c.scores.spellability,
                "uniqueness": c.scores.seo_uniqueness,
                "availability": c.scores.domain_handle,
                "confusion_risk": c.scores.confusion_risk,
            },
            "pr_headline_notes": c.pr_headline_notes,
            "alternatives": c.alternatives,
        }
        for c in cards
    ]
    return json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")


