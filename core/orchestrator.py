from __future__ import annotations

from dataclasses import dataclass
from typing import List

from core.config import load_configuration_or_fail
from core.schemas import Candidate, NameCard, ScoreCard, Evidence, DomainEvidence, HandleEvidence
from providers.exa_client import ExaClient
from providers.domains_godaddy import GoDaddyClient
from providers.handles import check_handle
from naming.generate_morphology import generate_morphological_names
from naming.score_phonetics import score_pronounceability
from naming.safety_profanity import has_profanity
from providers.llm_gemini import GeminiClient
import json
from prompts.prompt_registry import get_prompt
from prompts.prompt_runtime import render_prompt


@dataclass
class Orchestrator:
    exa: ExaClient
    godaddy: GoDaddyClient
    gemini: GeminiClient

    @classmethod
    def from_env(cls) -> "Orchestrator":
        cfg = load_configuration_or_fail()
        return cls(
            exa=ExaClient(api_key=cfg.exa_api_key),
            godaddy=GoDaddyClient(key=cfg.godaddy_key, secret=cfg.godaddy_secret),
            gemini=GeminiClient(api_key=cfg.gemini_api_key),
        )

    def generate_candidates(self, territories: List[str], per_territory: int = 10, use_structured: bool = False) -> List[Candidate]:
        candidates: List[Candidate] = []
        for t in territories:
            if use_structured:
                schema = {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "name": {"type": "STRING"},
                            "rationale": {"type": "STRING"},
                            "territory": {"type": "STRING"},
                        },
                        "propertyOrdering": ["name", "rationale", "territory"],
                    },
                }
                template = get_prompt("generation")
                # Pull context from environment/session later; for now neutral tone/constraints
                prompt = render_prompt(template, {
                    "territory": t,
                    "tone": "",
                    "do_dont": "",
                    "constraints": "",
                })
                # Higher temperature for more originality as per prompting strategies guidance
                raw = self.gemini.generate_structured(prompt=prompt, response_schema=schema, temperature=0.8)
                try:
                    items = json.loads(raw) if raw else []
                except Exception:
                    items = []
                if items:
                    for i, item in enumerate(items[:per_territory]):
                        name = (item.get("name") or "").strip()
                        if not name:
                            continue
                        candidates.append(Candidate(id=f"{t}-{i}", territory=t, text=name, rationale=item.get("rationale")))
                    continue
            # Fallback morphology
            names = generate_morphological_names(territory=t, tone="", count=per_territory)
            for i, n in enumerate(names):
                candidates.append(Candidate(id=f"{t}-{i}", territory=t, text=n))
        return candidates

    # Prompt-driven helpers
    def draft_strategy_brief(self, *, business: str, markets: str, tone: str, do_dont: str, competitors: str) -> str:
        template = get_prompt("strategy_brief")
        prompt = render_prompt(template, {
            "business": business,
            "markets": markets,
            "tone": tone,
            "do_dont": do_dont,
            "competitors": competitors,
        })
        return self.gemini.generate(prompt, max_tokens=512, temperature=0.3)

    def suggest_territories(self, *, purpose: str, pillars: str, tone: str, constraints: str) -> str:
        template = get_prompt("territories")
        prompt = render_prompt(template, {
            "purpose": purpose,
            "pillars": pillars,
            "tone": tone,
            "constraints": constraints,
        })
        return self.gemini.generate(prompt, max_tokens=256, temperature=0.4)

    def run_checks(self, candidates: List[Candidate]) -> List[NameCard]:
        cards: List[NameCard] = []
        for cand in candidates:
            domain = f"{cand.text.lower()}.com"
            # Placeholders for now
            availability = self.godaddy.check_availability(domain)
            exa_results = self.exa.search(query=cand.text, top_k=5)
            exa_hits = len(exa_results)
            handles = [
                check_handle("x", cand.text.lower()),
                check_handle("instagram", cand.text.lower()),
                check_handle("youtube", cand.text.lower()),
            ]

            scores = ScoreCard(
                distinctiveness=max(0.0, 1.0 - exa_hits * 0.1),
                pronounceability=score_pronounceability(cand.text),
                spellability=0.8,
                cultural=0.0 if has_profanity(cand.text) else 0.8,
                transliteration=0.7,
                accessibility=0.8,
                seo_uniqueness=max(0.0, 1.0 - exa_hits * 0.1),
                domain_handle=1.0 if availability.available else 0.3,
                narrative_fit=0.7,
                confusion_risk=0.2,
            )
            evidence = Evidence(
                exa_urls=[r.url for r in exa_results],
                domain=DomainEvidence(domain=domain, available=availability.available, reason=availability.reason),
                handles=[HandleEvidence(h.network, h.handle, h.exists) for h in handles],
            )
            card = NameCard(candidate=cand, scores=scores)
            # Attach evidence dynamically for UI (without altering dataclass signature now)
            card.evidence = evidence  # type: ignore[attr-defined]
            cards.append(card)
        return cards


