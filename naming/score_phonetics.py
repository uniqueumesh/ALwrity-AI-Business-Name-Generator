def score_pronounceability(name: str) -> float:
    # Heuristic: penalize long clusters; reward vowel balance
    vowels = sum(1 for ch in name.lower() if ch in "aeiou")
    consonants = sum(1 for ch in name.lower() if ch.isalpha() and ch not in "aeiou")
    length = len(name)
    if length == 0:
        return 0.0
    ratio = vowels / max(1, consonants)
    base = 0.6 + min(0.3, max(0.0, ratio - 0.3))
    if length > 12:
        base -= 0.1
    return max(0.0, min(1.0, base))


