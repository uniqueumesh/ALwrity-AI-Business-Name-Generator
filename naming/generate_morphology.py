from typing import List


PREFIXES = ["neo", "meta", "ver", "clar", "tru", "lum", "terra", "vital"]
SUFFIXES = ["ly", "io", "ify", "ity", "ora", "ium", "wave", "grid"]
CORES = ["trust", "pay", "fund", "leaf", "grid", "craft", "spark", "bridge", "clear", "mint"]


def _camel(word: str) -> str:
    return word[:1].upper() + word[1:]


def generate_morphological_names(territory: str, tone: str, count: int = 10) -> List[str]:
    results: List[str] = []
    # Simple blends/compounds to bootstrap
    i = 0
    while len(results) < count and i < 10_000:
        p = PREFIXES[i % len(PREFIXES)]
        c = CORES[(i // len(PREFIXES)) % len(CORES)]
        s = SUFFIXES[(i // (len(PREFIXES) * len(CORES))) % len(SUFFIXES)]
        name1 = _camel(p + c)
        name2 = _camel(c + s)
        for n in (name1, name2):
            if len(results) < count and 4 <= len(n) <= 12:
                results.append(n)
        i += 1
    # De-duplicate while preserving order
    seen = set()
    unique: List[str] = []
    for n in results:
        if n.lower() not in seen:
            seen.add(n.lower())
            unique.append(n)
    return unique[:count]


