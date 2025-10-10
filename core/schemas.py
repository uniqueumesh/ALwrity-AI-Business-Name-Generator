from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Candidate:
    id: str
    territory: str
    text: str
    rationale: Optional[str] = None


@dataclass
class ScoreCard:
    distinctiveness: float
    pronounceability: float
    spellability: float
    cultural: float
    transliteration: float
    accessibility: float
    seo_uniqueness: float
    domain_handle: float
    narrative_fit: float
    confusion_risk: float


@dataclass
class NameCard:
    candidate: Candidate
    scores: ScoreCard
    pr_headline_notes: Optional[str] = None
    alternatives: Optional[List[str]] = None


@dataclass
class DomainEvidence:
    domain: str
    available: bool
    reason: Optional[str] = None


@dataclass
class HandleEvidence:
    network: str
    handle: str
    exists: bool


@dataclass
class Evidence:
    exa_urls: List[str]
    domain: DomainEvidence
    handles: List[HandleEvidence]



