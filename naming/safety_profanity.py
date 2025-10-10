PROFANITY = {"bad", "curse"}


def has_profanity(name: str) -> bool:
    n = name.lower()
    return any(p in n for p in PROFANITY)


