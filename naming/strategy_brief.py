from dataclasses import dataclass
from typing import List


@dataclass
class StrategyBrief:
    purpose: str
    pillars: List[str]
    tone: str
    constraints: str
    success_criteria: str


def draft_strategy_brief(*, business: str, markets: str, tone: str, do_dont: str, competitors: str) -> StrategyBrief:
    # Placeholder implementation; will integrate prompts + LLM later
    return StrategyBrief(
        purpose=f"Purpose aligned with {business}",
        pillars=["Clarity", "Trust", "Distinctiveness"],
        tone=tone or "modern",
        constraints=do_dont or "",
        success_criteria="Memorable, pronounceable, available",
    )


