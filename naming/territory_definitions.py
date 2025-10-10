from dataclasses import dataclass
from typing import List


@dataclass
class Territory:
    name: str
    essence: str
    tonal_words: List[str]


DEFAULT_TERRITORIES = [
    Territory("Pioneer", "Bold, first-mover energy", ["bold", "forward", "venture"]),
    Territory("Sage", "Wisdom and trust", ["calm", "seasoned", "clarity"]),
    Territory("Minimalist", "Clean, modern utility", ["clean", "spare", "direct"]),
    Territory("Nature-Tech", "Organic meets engineered", ["green", "balanced", "earth"]),
    Territory("Precision", "Exacting, engineered", ["sharp", "precise", "refined"]),
]


