# ALwrity AI Business Name Generator — System Architecture (No-Code Plan)

## 1) Purpose and Scope
- Goal: Automate the full human naming workflow in minutes within a transparent, open-source Python + Streamlit Cloud app.
- Out of scope (for now): Attorney-led comprehensive trademark searches/filings and premium domain brokerage. We provide heuristic risk signals only.
- Non-goals: Storing user data by default; providing legal advice; heavy SEO research beyond uniqueness signals.

## 2) High-Level Architecture
- Client/UI: Streamlit multi-step app guiding users from Brief → Territories → Candidates → Checks → Shortlist → Package.
- Core Orchestrator: Python services coordinating generation, scoring, and checks with parallelism and deterministic seeding.
- Subsystems (pluggable):
  - Strategy & Territories
  - Creative Generation
  - Scoring & Reranking (distinctiveness, phonetics, spellability, narrative fit)
  - Linguistic/Cultural Safety (multilingual/profanity/ambiguity)
  - Transliteration & Accessibility (screen reader/voice assistants)
  - TTS/ASR Confusion Checks (optional)
  - Domain/Handle Availability
  - SEO/SERP Uniqueness Signals
  - Consumer Validation (optional microtests)
- Data Layer: Ephemeral in-memory objects, optional in-memory vector index (FAISS/annlite). Opt-in cached lookups with TTL.
- Integrations (optional via user-provided keys): Embeddings/LLM, domain registrars/APIs, social handles, web research (EXA), TTS/ASR.

## 3) Key Constraints and Design Tenets
- Python-only; deployable on Streamlit Cloud.
- Open-source, modular, testable; deterministic runs via seeds.
- Privacy-first: no persistence by default; explicit consent for saved artifacts.
- All external calls toggleable; graceful degradation without keys.
- Backend-first execution: all planning, generation, and checks run server-side; UI performs no heavy computation.
- Human-in-the-Loop gates: human confirms Brief/Territories, reviews Shortlist, and makes Final Selection.
- Cost policy: free-only by default. No paid services; enhanced checks run only if user supplies keys to free-tier providers.
 - Startup validation: required env keys must be present; the app fails fast if any are missing.

## 4) User Flows (Top-Level)
1) Input Brief or URL/deck → auto-draft Strategy Brief.
2) Confirm territories → generate bulk candidates per territory.
3) Parallel checks → score/rerank → shortlist with rationale.
4) Optional deeper checks (TM API, TTS/ASR, SEO, consumer microtests).
5) Package export (CSV/JSON + PDF report) and asset prompts.
Notes:
- All processing is initiated by the UI but executed in the backend; the UI displays status, progress, and results.
- Decision gates (HITL) occur at step 2 (territories), step 3/5 (shortlist and final selection).

## 5) Module Breakdown (Python Packages)
- ui/ (Streamlit pages)
  - pages/01_brief.py: inputs, competitor list, constraints, seeds.
  - pages/02_territories.py: territory selection and tone sliders.
  - pages/03_generate.py: run sprints, show candidates per lane.
  - pages/04_checks.py: run batch checks and scores.
  - pages/05_shortlist.py: compare, filter, annotate rationale.
  - pages/06_package.py: export report and bundle assets.
- core/ (Orchestration)
  - orchestrator.py: pipelines, concurrency, retry/backoff, seeds.
  - schemas.py: dataclasses/typed models for inputs/outputs.
  - cache.py: memoization, TTL caches, request dedupe.
  - config.py: feature flags, provider selection, timeouts.
- providers/ (Adapters) — one feature per file
  - llm_gemini.py (Gemini LLM adapter)
  - embeddings_local.py (sentence-transformers adapter)
  - exa_client.py (EXA/Metaphor web research)
  - domains_godaddy.py (GoDaddy availability)
  - whois_rdap.py (RDAP/WHOIS lookups)
  - tts_vosk.py (optional)
  - asr_vosk.py (optional)
- naming/ (Domain Logic)
  - strategy_brief.py (brief drafting)
  - territory_definitions.py (lane definitions)
  - generate_morphology.py (morphological engines)
  - generate_llm_assist.py (LLM assist)
  - score_distinctiveness.py
  - score_phonetics.py
  - score_spellability.py
  - score_narrative_fit.py
  - safety_profanity.py
  - safety_cultural.py
  - safety_transliteration.py
  - safety_accessibility.py
  - availability_domains.py
  - availability_handles.py
  - seo_uniqueness.py
  - validation_microtests.py (optional)
- prompts/
  - prompt_strategy_brief.txt (default template)
  - prompt_territories.txt
  - prompt_generation.txt
  - prompt_rationale.txt
  - prompt_registry.py (maps features to templates)
  - prompt_runtime.py (variable injection, versioning)
- reporting/
  - shortlist_cards.py (name cards)
  - export_csv.py
  - export_json.py
  - export_pdf.py
- infra/
  - logging_setup.py
  - metrics_minimal.py
  - rate_limit.py
- tests/ (unit/integration/e2e specs)
  - One test module per feature file; fixtures per provider.

Note: Map to current files gradually (e.g., app.py, generator.py, utils.py become entrypoints/wrappers around the above modules).

## 6) Data Contracts (Typed Schemas)
- StrategyBrief: purpose, pillars, tone, markets/languages, constraints, criteria weights.
- Territory: id, name, essence, tone sliders, on/off lexicon, examples.
- Candidate: id, territory_id, text, rationale, generation_method, variants.
- ScoreCard: distinctiveness, pronounceability, spellability, cultural, transliteration, accessibility, seo_uniqueness, domain_handle, narrative_fit, confusion_risk; per-dimension notes.
- NameCard: candidate + ScoreCard + PR-headline notes, alternatives.
- Report: shortlist, metadata (seeds, providers, versions), disclaimers.

## 7) Pipelines and Concurrency
- P1 Brief: URL/deck ingest → extract signals → draft StrategyBrief (LLM optional) → human confirm.
- P2 Territories: propose 6–8 lanes → user picks 3–5.
- P3 Generation: for each lane, run hybrid generators (morphology + LLM) to produce 100–300 names; dedupe via embeddings; daily-like cull heuristics.
- P4 Checks (parallel fan-out/fan-in):
  - Distinctiveness vs competitors/category via vector distances.
  - Phonetics (g2p/phonemizer), spellability heuristics.
  - Safety: profanity/cultural lists, transliteration, accessibility.
  - Availability: domains/handles.
  - SEO uniqueness: n‑gram rarity; optional EXA-based novelty heuristics.
  - TTS/ASR confusion loop (optional): synthesize → transcribe → distance.
- P5 Rerank: weighted scoring → diversity enforcement → shortlist.
- P6 Package: rationale, story, taglines, export.
- Concurrency: asyncio tasks with bounded semaphores; retries with jitter; provider circuit breakers; per-provider rate limits.

## 8) Determinism and Reproducibility
- Global random seed + per-stage seeds recorded in Report.
- Temperature discipline for LLM; stable reranking; cache key includes prompts, versions, seeds.

## 9) Non-Functional Requirements
- Performance: Express run (2–5 min) on Streamlit Cloud baseline; Pro run (10–30 min) with optional checks.
- Reliability: Retries with exponential backoff; degraded modes when providers fail.
- Security: No secrets in logs; Streamlit secrets.toml; outbound-only calls; domain allowlists for fetchers.
- Privacy: No default persistence; opt-in project saves; data minimization; redaction of PII in cached keys.
- Accessibility: Clear read-aloud, keyboard navigation; pronunciation audio; high-contrast themes.
- Internationalization: Locale-aware checks and transliteration modules.
- Observability: Structured logs, minimal metrics (latency, error rates, hit/miss cache), optional OpenTelemetry hooks.

## 10) Configuration and Feature Flags
- Provider selection: EMBEDDINGS_PROVIDER, LLM_PROVIDER, TTS_PROVIDER, ASR_PROVIDER.
- Feature toggles: ENABLE_TTS_ASR, ENABLE_SERP, ENABLE_CONSUMER_TESTS, ENABLE_GEMINI, ENABLE_EXA.
- Timeouts and budgets per stage; concurrency limits.
- Cache TTLs per integration; opt-in persistent cache (if enabled by user).

### Environment Configuration (.env and Streamlit secrets)
- Local development: store API keys in a `.env` file (not committed). Load via `python-dotenv`.
  - Required keys (mandatory): `GEMINI_API_KEY`, `EXA_API_KEY`, `GODADDY_KEY`, `GODADDY_SECRET`. Optional: `GITHUB_TOKEN`.
  - Behavior: if any required key is missing, the app fails fast at startup with a clear error.
- Streamlit Cloud: use `secrets.toml` (Cloud UI) with the same key names. The app checks `st.secrets` first, then `.env`.
- Security: never print secrets; redact in logs; validate presence at startup and surface non-blocking warnings.

### Prompt Configuration and Runtime Editing
- Default prompts live under `prompts/` as plaintext/Jinja-like templates; no code change needed to tweak.
- A Prompt Editor UI allows per-step editing (brief, territories, generation, rationale) with preview and reset-to-default.
- Prompt variables: `{tone}`, `{markets}`, `{territories}`, `{constraints}`, `{competitors}`, `{seed}`.
- Versioning: save user-edited prompts with timestamp/label; select active version at runtime.
- Safety: sanitize injected variables; show token/length counters; warn on risky instructions.

## Providers & API Keys (Free-Only Defaults)
- LLM/Generation: Gemini 2.5 Flash via Google AI Studio (free tier where available) — requires GEMINI_API_KEY. Fallback: local morphological generators (no API). Optional: Hugging Face Inference (free tier) if token provided.
- Embeddings: sentence-transformers (e.g., all-MiniLM-L6-v2) running locally; FAISS for in-memory vector search (no API).
- Phonetics: phonemizer, CMUdict local resources (no API).
- Transliteration: Unidecode/epitran (local, no API).
- Profanity/Cultural safety: curated multilingual lists (local), no external API.
- Domains/WHOIS: DNS queries and python-whois where feasible (no paid API). Optional registrar APIs if user provides free keys.
 - Domains/WHOIS: DNS queries and python-whois where feasible (no paid API). Optional registrar APIs if user provides free keys (e.g., GoDaddy Domains API: availability endpoints; respect rate limits/ToS).
- Social handles: direct HTTP checks to profile URLs (no API) respecting rate limits; optional official APIs only if user provides keys.
- SEO uniqueness: offline n-gram rarity and corpus checks (no API). Optional EXA (Metaphor) web research API (EXA_API_KEY, free tier where available).
- TTS/ASR (optional): disabled by default. Prefer offline Vosk/Coqui when enabled (resource-permitting); cloud providers only with user keys.
- Translation (optional): disabled by default; can use DeepL/Google only if user keys and free tier allow.
- Reporting: CSV/JSON native; PDF via WeasyPrint or ReportLab (no API).

Defaults
- All ENABLE_* feature flags default to disabled; free/offline paths are used.
- If a provided key exceeds free tier or is missing, the system gracefully falls back to offline heuristics.

Network & Compliance
- Respect robots.txt and site terms for any public endpoint checks; throttle requests.
- Do not scrape or store personal data; minimize outbound calls.

## 11) Error Handling and Guardrails
- Input sanitation: strip risky content; avoid prompt injection/over-broad URLs.
- Safety filters: profanity/cultural blocklists on outputs.
- Legal disclaimer injected into reports and UI; tool excludes trademark checks.
- Graceful UI fallbacks when integrations are disabled or quota-limited.

## 12) Deployment (Streamlit Cloud)
- Single repo application entry app.py coordinating page router.
- Secrets via Streamlit Cloud `secrets.toml` (keys per provider). Local dev uses `.env` with `python-dotenv`.
- Resource constraints: limit concurrency and batch sizes; progressive disclosure (run heavy checks only on shortlist).
- Build cache: pre-download small models (phonemizer dictionaries) if allowed.
- CDN or cached endpoints for static assets (icons, CSS).
 - Prompts can be bundled in repo or overridden via `st.secrets`/`.env` paths (optional).

## 13) Testing Strategy
- Unit tests: morphology generators, scoring heuristics, profanity/transliteration, similarity metrics.
- Golden tests: seed-based generation snapshots for stability across refactors.
- Integration tests: pipeline with fake providers/mocks; concurrency/rate-limit tests.
- Contract tests: provider adapters conform to interfaces.
- E2E smoke: Streamlit session with headless runner (basic navigation + Express run).
- Static checks: ruff/flake8, black, mypy (where practical).
- Security: secrets scan, dependency audit (pip-audit/safety).

## 14) Documentation and OSS Hygiene
- README with quickstart, feature flags, and disclaimers.
- docs/ with user guide and admin guide.
- CONTRIBUTING, CODE_OF_CONDUCT, issue templates.
- Architecture diagram (mermaid) and dataflow charts.

## 20) Online Verification Baseline (Mandatory)
- Web uniqueness: EXA (Metaphor) queries for exact/fuzzy matches; record top-N collisions and URLs.
- Domains: GoDaddy API (if keys) or RDAP/WHOIS + DNS A/NS lookup.
- Social handles: HEAD/GET to canonical profile URLs to detect taken/exists.

## 21) Evidence Ledger (Per Name)
- Store: timestamps, sources, counts (EXA hits), domain/handle status, flags.
- Display: evidence badges on cards + expandable table with links.
- Score: Uniqueness score derived from evidence (not model claims) with thresholds.
 - Privacy: store only URLs and timestamps; do not retain page contents.

- Env vars: GEMINI_API_KEY, EXA_API_KEY, GODADDY_KEY, GODADDY_SECRET, optional GITHUB_TOKEN.
- Rate limits: document per provider; apply backoff (e.g., 429 → exponential retry).
- Cache TTLs: EXA (15–60 min), domain checks (15 min), handles (60 min). Display last-checked timestamps.

## 15) Roadmap (Architecture Milestones)
- M0 Express: brief → territories → generation → dedupe → phonetics/safety → domain/handles → shortlist/export.
- M1 Pro: transliteration/accessibility, SEO signals, TTS/ASR.
- M2 Validation: optional consumer microtests; improved reranking; caching/telemetry refinements.
- M3 Extensibility: multi-provider registry; plugin API; persisted projects (opt-in).

## 16) Risks and Mitigations
- API rate/latency: batch, cache, fallback to heuristics; user toggles.
- Cultural pitfalls: conservative blocklists; surface flags prominently.
- Model drift: golden tests + version pinning; report includes model versions.

## 17) Acceptance Criteria for Architecture
- Clear module boundaries and provider adapters.
- Deterministic, cacheable pipelines with documented seeds.
- Toggleable integrations and graceful degradation.
- Documented deployment and testing paths compatible with Streamlit Cloud.
 - Required env keys configured (`GEMINI_API_KEY`, `EXA_API_KEY`, `GODADDY_KEY`, `GODADDY_SECRET`) and validated at startup.

## 19) Code Organization Policy (One Feature per File)
- Each feature resides in its own Python file; do not mix multiple features in a single file.
- UI pages follow one page per file; helpers/utilities remain small and single-purpose.
- Providers: one adapter per file (e.g., `domains_godaddy.py`, `exa_client.py`).
- Scoring/safety/availability/seo: one metric/check per file (`score_phonetics.py`, `safety_profanity.py`, etc.).
- Extractions that grow > ~300–400 LOC should be decomposed into smaller feature files rather than accumulating utilities.

---

## 18) UI/UX Principles (Wizard, Minimal Scrolling)
- Wizard flow with discrete steps: Brief → Territories → Generate → Checks → Shortlist → Package. Use a stepper with clear progress.
- Minimal scrolling: group inputs into concise sections; use accordions/tabs for advanced options; avoid long single-page forms.
- Sticky actions: persistent top/bottom bar for primary actions (Run, Next, Back, Export) and key filters.
- Progressive disclosure: advanced settings collapsed by default; show tooltips/help on demand.
- Results ergonomics: paginated or tabbed lists; filter/sort controls; comparison “basket” to pin candidates; no infinite scrolling.
- Accessibility: keyboard navigation, focus states, ARIA labels, high contrast, readable sizes; screen-reader-friendly labels.
- Responsiveness: layouts that adapt to common breakpoints; avoid horizontal scroll; maintain readable line lengths.
- Feedback: skeletons/placeholders, progress indicators, non-blocking toasts for background tasks; retry affordances.
- Error handling: clear, actionable messages; graceful fallbacks when integrations are disabled or rate-limited.
- HITL UI: gated confirmation dialogs with scoring rubrics at key decisions (territories, shortlist, final lock).
- Export/share: one-click CSV/JSON/PDF export; copy-to-clipboard for selected names; seed/version shown for reproducibility.
 - Prompt Editor: compact tab/accordion to tweak prompts per step; supports save-as-version and revert-to-default.


This document defines the system plan without code, ensuring we can implement iteratively while maintaining quality, privacy, and performance.
