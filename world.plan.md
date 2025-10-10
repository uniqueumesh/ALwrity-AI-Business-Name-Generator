<!-- 5fc92fc7-6f15-4ca5-9ce4-8e434d04cec5 bf6bfab2-9932-4e9c-aed1-26fde1fdfb39 -->
# World-Class Naming Agency Manual (Lexicon/Catchword-Grade)

## Purpose and Principles

- **Objective**: Deliver distinctive, defensible, memorable names aligned to strategy, culture, and markets.
- **Principles**: Strategy-first, territory diversity, rigorous vetting, global sensitivity, legal prudence, transparent rationale, reproducibility.
- **Outcomes**: 2–3 finalist names with rationale, risks, and activation assets; decision made with confidence.

## Roles and Responsibilities

- **Client Stakeholders**: Decision makers, SMEs, legal liaison; provide inputs, attend gates, own final decision.
- **Lead Strategist**: Owns brief, territories, scoring model, and decision gates.
- **Creative Lead + Namers**: Generate, curate, narrate candidates; maintain freshness and breadth.
- **Linguist**: Phonetics, multilingual/cultural screening, red-flag lexicon.
- **Legal Scout**: Preliminary TM/availability signals; interfaces with counsel.
- **Project Manager**: Timeline, workshops, artifact hygiene, approvals.

## Timeline and Decision Gates (3–6 weeks typical)

- Week 0–1: Discovery → **Gate A**: Strategy Brief sign-off
- Week 1–2: Territories + Generation → **Gate B**: Focus territories agreed
- Week 2–3: Screening + Shortlist v1 → **Gate C**: Proceed to diligence
- Week 3–4: Client Round 1 + Iteration → **Gate D**: Down-select 2–3
- Week 4–6: Counsel clearance + Final → **Gate E**: Name lock

---

## Phase 1 — Discovery and Strategy Intake

- **Inputs**: Brief, deck/URL, roadmap, competitor list, geographies/languages, Nice classes, do/don’t words, risk tolerance, domain budget.
- **Activities**:
- Stakeholder interviews (leadership, product, marketing, legal, regional)
- Category language audit; competitor name map and cliché inventory
- Audience/usage contexts; internal naming constraints; phonetic preferences
- Risks: regulatory, cultural, political; domain/SEO expectations
- Brand architecture mapping (masterbrand vs sub-brand, extensions; verbability/pluralization)
- **Deliverables**: Strategy Brief v1 (purpose, promise, pillars, tone, constraints, success criteria) + Brand Architecture Note.
- **Acceptance (Gate A)**: Stakeholders sign brief; criteria weighting confirmed; prohibited/required terms logged; initial markets/languages agreed; early TM screening depth agreed; brand architecture alignment confirmed.
- **Checklist**: Stakeholders, competitors, markets, Nice classes, constraints, success KPIs captured; brand architecture documented.

## Phase 2 — Creative Territories and Naming Brief

- **Objectives**: Define distinct conceptual lanes to avoid convergence.
- **Activities**:
- Draft 6–8 territories (e.g., Pioneer, Sage, Minimalist, Nature-Tech, Precision, Human Warmth, Futurist, Craft)
- Set tone sliders; lexicon on/off lists; preferred name forms; phonetic guidance
- Provide 3–5 reference exemplars per territory (not for imitation)
- Align territories with brand architecture scenarios (future line extensions, category breadth)
- **Deliverables**: Territory Map + Naming Brief (criteria, tones, examples, must/avoid list).
- **Acceptance (Gate B)**: 3–5 focus territories prioritized; exclusions agreed; demonstrated diversity vs category clichés; architecture fit validated.

## Phase 3 — Generative Naming Sprints

- **Goal**: 800–1500 raw candidates across lanes with rationale notes.
- **Techniques**:
- Lexical: compounds, blends/portmanteau, affixation (prefix/suffix), clipping, reduplication
- Semantic: metaphor/metonymy, archetypes, domain metaphors, symbol systems
- Linguistic: Latin/Greek roots, transliteration, alliteration, rhyme, stress play
- Structural: real words, invented, evocative, descriptive, associative
- **Cadence**: 3–4 sprints with daily culls, peer critique, freshness protection (no repeating stems across lanes).
- **Quality Rules**: Speakable, spellable, stress-friendly, non-generic, strategy-aligned; avoid category clichés.
- **Artifacts**: Raw name log with territory tag, generation notes, intended meaning, optional variants.

Implementation Notes (tools)
- Text generation support: Gemini 2.5 Flash LLM (when key provided); otherwise offline morphological generation.
- Web uniqueness research (optional): EXA (Metaphor) API for result clustering and novelty signals (when key provided); fallback to offline n‑gram rarity checks.

Prerequisites (mandatory for tool operation)
- The following environment keys must be set before running the tool:
  - `GEMINI_API_KEY` (generation quality)
  - `EXA_API_KEY` (web uniqueness baseline)
  - `GODADDY_KEY` and `GODADDY_SECRET` (domain availability)
- The application will fail fast at startup if any required key is missing.

## Phase 4 — First-Pass Hygiene and Culling

- **Screens**: Duplicates; tongue-twisters; unintended slang; length > 12–14 chars (contextual); numerical/ambiguous punctuation; category clichés; homely sound clusters.
- **Deliverable**: Reduced set ≈200–300 for prioritized territories with quick rationale per survivor.

## Phase 5 — Linguistic and Cultural Screening

- **Checks**:
- Multilingual profanity/ambiguity across target locales; homophones/homographs; mis-segmentation risks
- Phonetics: pronounceability, sonority profile, stress pattern, syllable count; ease across key accents
- Acoustic confusion: read-aloud mishear risks in core markets (where relevant)
- Transliteration/script testing for non-Latin markets (e.g., ZH/JA/KO/AR/HI); IDN domain feasibility
- Accessibility and voice: screen reader pronunciation; voice assistant recognition; call-center clarity
- **Risk Tags**: Green (clear), Yellow (manageable with variant/spelling), Red (reject or pivot).
- **Deliverable**: Screening notes and flags appended to each candidate.

## Phase 6 — Preliminary Availability Signals

- **Common law & registries**: Company registries/state DBs and common-law usage scans (where available).
- **Marketplace scans**: App stores, major e‑commerce, GitHub, npm/PyPI (as relevant) for collisions/associations.
- **Availability**: Domain checks (primary/creative alternatives), social handle scans.
- **Deliverables**: Per-name availability heatmap (domains/handles, common law/marketplace signals).
- **Acceptance (Gate C)**: Shortlist-ready candidates show acceptable availability posture; transliteration/accessibility concerns addressed or mitigated; common law/marketplace scans reviewed.

## Phase 7 — Shortlist Creation v1

- **Curation**: 20–40 strongest names across 3–5 territories with rationale and scores.
- **Name Card** includes: territory, meaning/story, “why it works”, pronunciation (IPA/simple), stress, syllables, linguistic/cultural notes, domain/handle signals, common law/marketplace notes, differentiation vs competitors, PR headline/ambiguity stress-test notes, variants/pivots.
- **Artifact**: Deck/PDF with rubric and territory sections.

## Phase 8 — Internal Validation and Memory Testing

- **Methods**: 10-second distraction recall; spell-back; say-back; confusion vs competitor/confusables set; distinctiveness review.
- **Optional target-user microtests (pre‑Gate D)**: Remote preference/recall/say-back tests with target audience segments; capture insights and deltas.
- **Output**: Score sheets; adjustments to shortlist with rationale.

## Phase 9 — Client Workshop (Round 1 Presentation)

- **Agenda** (60–90 min):
- Frame strategy and territories; read-aloud demos; guided scoring; live cull; identify learning goals
- **Capture**: Criteria re-weighting, likes/dislikes, redlines, pivot directives; summary of any consumer validation results.
- **Acceptance (Gate D)**: Down-select 2–3 finalists + 3 alternates; consumer validation (if run) considered; PR headline test passed for finalists.

## Phase 10 — Iteration Rounds

- **Focus**: Address feedback; expand/pivot lanes; produce variants informed by risks.
- **Deliverable**: Refined shortlist with updated screenings and availability.

## Phase 11 — Deep Diligence and Legal Coordination

- **Support**: Provide nearest conflicts, goods/services, usage intents; coordinate with counsel’s comprehensive search.
- **Domain Strategy & Legal Posture**: Primary/acquirable options; defensive registration matrix (core + typo/ccTLD set); UDRP/cybersquatting risk posture and mitigation.

## Phase 12 — Final Selection and Lock

- **Tie-Breakers**: Strategy fit, differentiation, global safety, legal posture, scalability, narrative power.
- **Artifacts**: Decision memo, approval log, risk register snapshot.
- **Acceptance (Gate E)**: Executive sign-off; counsel does not object; domain legal posture reviewed; enforcement plan drafted.

## Phase 13 — Narrative and Brand Enablement

- **Outputs**: Brand story paragraph; reason-to-believe bullets; 3–5 tagline options; voice/tone guardrails; pronunciation guide; do/don’t examples; visual direction prompts (orientation only); quick wordmark/type legibility feasibility probe.
- **Deliverable**: Naming Package (slides/PDF + CSV/JSON metadata).

## Phase 14 — Implementation and Launch Support

- **Checklist**: Domain registration/redirects; social handle claims; filings initiation; internal/external comms; SEO/meta updates; analytics annotation; monitoring and escalation paths; enforcement readiness plan.

---

## Decision Rubrics and Scoring

- **Dimensions**: Distinctiveness, pronounceability, memorability, cultural safety, domain viability, narrative fit, scalability.
- **Scale**: 1–5 with rationale notes; traffic-light risk tags; agreed weightings per brief.
- **Usage**: Score independently; discuss deltas; adjust weights only at gates.

## Quality Bars (Per Phase)

- **Brief**: Clear promise, pillars, tone, constraints; consensus documented; architecture alignment confirmed; markets/languages and screening depth agreed.
- **Territories**: 6–8 distinct lanes; 3–5 prioritized; examples illustrate difference; architecture fit validated.
- **Generation**: ≥800 unique candidates; coverage across forms; rationale logged.
- **Screening**: Linguistic/global checks complete (incl. transliteration & accessibility); risk tags applied; conflicts and marketplace/common-law signals listed.
- **Shortlist**: 20–40 names; balanced across lanes; fully documented cards incl. PR headline notes.
- **Finalists**: 2–3 with acceptable risk posture and strong narrative fit; consumer validation (if run) aligns.

## Taxonomy of Name Forms (Pros/Cons)

- **Real Word**: Pros clarity; cons scarcity/conflicts.
- **Evocative**: Pros emotional; cons interpretive ambiguity.
- **Invented**: Pros ownable; cons education required.
- **Descriptive**: Pros instant comprehension; cons commodity feel.
- **Associative/Metaphor**: Pros rich story; cons cultural nuance.
- **Compound/Blend/Affixed/Clipped/Reduplicated**: Pros flexibility; cons craft risk.

## Red-Flag Lexicon & Cultural Considerations

- Maintain lists per market for profanity, taboo, negative connotations, sensitive political/historical references, unintended segmentations.

## Workshop Facilitation (Script Highlights)

- Frame strategy; calibrate on criteria; read-aloud practice; individual scoring; group discussion; down-select; confirm pivots.

## Governance and Records

- Versioned logs of candidates, culls, rationales.
- Decision histories and risk registers retained.
- Disclaimers: preliminary legal checks are not legal advice.

---

## Appendices — Templates

### A. Strategy Brief Template

- Purpose/Promise; Audience & Use Cases; Positioning Pillars; Brand Personality/Tone; Markets/Languages; Competitors & Category Language; Constraints (Regulatory/Linguistic/Domain/SEO); Do/Don’t Words; Success Criteria & Weights; Brand Architecture Notes.

### B. Territory Map Template

- Territory Name; Essence; Tonal Words; Sample Lexicon; Off-Limits Notes; Example Names (adjacent categories); Generation Prompts.

### C. Name Card Template

- Name; Territory; Meaning/Story; Why It Works vs Strategy; Pronunciation (IPA/Simple); Syllables/Stress; Linguistic/Cultural Notes; Domain/Handle Options; Common Law/Marketplace Notes; Differentiation vs Competitors; PR Headline Risks; Variants/Pivots; Recommendation.

### D. Screening Checklist

- Duplicates; Length/Clarity; Tongue-Twister; Negative/Slang; Profanity/Ambiguity (Locales); Homophones/Homographs; Pronounceability; Stress & Sonority; Acoustic Confusion; Transliteration/Script; Accessibility/Voice; Common Law/Registries; Marketplace Scans; Domain/Handles; Cliché Avoidance.

### E. Workshop Agenda & Scoring Sheet

- Agenda blocks (Intro, Territories, Read-Aloud, Individual Scoring, Discussion, Down-Select, Next Steps); Scoring grid with dimensions and weights; Notes.

### F. Final Decision Memo Template

- Finalists Compared; Scores & Weights; Counsel Feedback Summary; Risks & Mitigations; Domain Strategy; Enforcement/Watch Plan; Decision & Rationale; Approvals.

### G. User Validation & PR Headline Test Templates

- Lightweight user test guide (recall, say-back, preference); sample prompts and scoring grid.
- PR headline/ambiguity stress-test checklist with examples.

### To-dos

- [ ] Conduct discovery and draft Strategy Brief v1
- [ ] Document brand architecture alignment and constraints
- [ ] Define creative territories and Naming Brief
- [ ] Run naming sprints to produce raw candidates
- [ ] Perform first-pass hygiene culling
- [ ] Run linguistic and cultural screening (incl. transliteration & accessibility)
- [ ] Perform common law, registries, and marketplace scans
- Note: For implementation specifics (Online Verification Baseline via EXA, domain/handle checks, Evidence Ledger, env keys, and Prompt Editor), see `ARCHITECTURE.md`.
- [ ] Check domain/handle availability and creative alternatives
- [ ] Assemble Shortlist v1 with name cards (incl. PR headline notes)
- [ ] (Optional) Run target-user microtests (recall, say-back, preference)
- [ ] Facilitate client workshop and down-select
- [ ] Iterate with focused sprints and refinements
- [ ] Coordinate counsel for comprehensive legal clearance
- [ ] Define domain legal posture and defensive registration matrix
- [ ] Run final selection decision process and approvals
- [ ] Develop brand story, taglines, voice guardrails, and visual feasibility probe
- [ ] Support implementation: domains, handles, filings, SEO, monitoring, enforcement plan


