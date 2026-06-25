# Learning Companion: v1 Spec

**Version:** v1 (Module 1 deliverable)
**Status:** Spec, not yet built
**Public repo:** _TBD on first commit_

---

## Purpose

A multi-agent build-to-learn companion for self-directed adult professional technical learning. Captures and probes the user's actual build decisions, runs spaced-repetition BS-checks on claimed learnings, and grows in capability module-by-module alongside the user's learning plan.

v1 is single-user: each instance is operated by the person doing the learning. Multi-user / hosted operation is explicitly out of scope for v1. See the reference instance at `../instance/` for an applied example.

---

## Differentiation (from existing prior art)

| Prior art | Approach | Where v1 differs |
|---|---|---|
| Mia Kiraki's "AI tutor that won't let you fake understanding" (Feb 2026) | Single-agent Claude Project + file-based knowledge base + spaced repetition | Multi-agent architecture; integrated with active build workflows (decision logs from real builds, not curriculum tracking); calibrated LLM-as-judge as a first-class documented component |
| agent-tutor-skill (Bhala-Srinivash, GitHub) | Claude Code skill with FSRS spaced repetition + zero-hint quizzes | Adult professional technical audience (not student/course); decision-capture during builds; multi-agent rather than single-skill |
| DeepTutor (HKUDS) | Agent-native open-source personalized tutoring | Adult professional self-directed; build-to-learn loop; not academic course material |
| Commercial (Khanmigo, Coursera Coach, 360Learning) | K-12 / consumer / corporate LMS | Out of category: different audience, different use case |

**One-line differentiation:** Other AI tutors check whether you understood *what you read*. This one checks whether you understood *what you built*.

---

## v1 components

Three agents + orchestration + state + retrieval + eval.

```
                  ┌─────────────────────┐
                  │     Orchestrator    │
                  │  (router + session  │
                  │     state mgmt)     │
                  └──────────┬──────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
            ▼                ▼                ▼
   ┌────────────────┐  ┌──────────┐  ┌─────────────────┐
   │ Decision-Log   │  │   RAG    │  │   BS-Checker    │
   │     Agent      │◄─┤  layer   ├─►│     Agent       │
   │ (ingest +      │  │(embed +  │  │ (gen Q + judge  │
   │ structure)     │  │ retrieve)│  │  w/ calibration)│
   └────────┬───────┘  └────┬─────┘  └────────┬────────┘
            │               │                 │
            └───────────────┴─────────────────┘
                            │
                            ▼
                  ┌─────────────────────┐
                  │  Persistent state   │
                  │ (SQLite + filesystem│
                  │  for v1)            │
                  └─────────────────────┘
```

### Orchestrator
- Top-level multi-agent coordinator.
- Owns session state and routing.
- Surfaces queued BS-checks at session start (spaced repetition trigger).
- Single entrypoint for user interaction.

### Decision-Log Agent
- Ingests build decisions during/after a session.
- Structures into: `decision`, `alternatives_considered`, `rationale`, `expected_tradeoffs`, `tags`, `linked_artifact`.
- Indexes into the corpus (filesystem markdown + SQLite metadata).
- Supports query by tag, date, topic, or semantic search via the RAG layer.

### RAG layer
- Embedding-based retrieval over the decision-log corpus and any external instrumental reading I've ingested.
- v1 stack: chosen embedding model (Week 4 decision), simple chunk strategy, top-k retrieval with optional re-ranking.
- Documented eval against hand-crafted query set.

### BS-Checker Agent
- Generates probing questions from logged decisions/claims.
- Presents to me, accepts answer, judges via calibrated LLM-as-judge.
- Flags hand-waving, partial understanding, drift over time.
- Records results into corpus so future questions can target weak areas.
- **Multi-tier scheduling.** Each claim is checked at multiple intervals: spot (same session), short (Day 2-3), medium (Week 1-2), long (Month 1-3). FSRS-style: successful passes extend the next interval; failure resets to a shorter one. The long-interval pass is the interview-defensibility check.
- **Calibration is a documented first-class step.**

#### BS-Checker v0 architecture (as built, Module 1 Week 3)

The Week 3 build implemented the BS-Checker with explicit deferrals for components that depend on a calibrated judge. The v0 architecture has four design pillars:

**Three-level content model.** Every answer is evaluated against three tiers of content:
- **Core reasoning**: the architectural understanding the claim is about. Always required for credit.
- **Key supporting details**: substantive specifics that ground the reasoning. Required at higher tiers.
- **Lookup minutiae**: exact API names, version numbers, syntax. Never penalized.

This maps directly to the *Vocabulary calibration* methodology: probes target architecture rationale rather than lookup-able facts.

**Rising rigor by tier (standard rises, pass line stays fixed).** A vague-but-right answer passes spot but must supply key supporting details before durable. The bar climbs underneath the claim as it climbs the spaced-repetition ladder:
- **Spot**: explain your reasoning at a high level
- **Short**: reasoning + a key supporting detail
- **Medium**: reasoning + multiple key supporting details
- **Long**: interview-cold defense, full content tier

**Teach-on-every-check (foil-after-recall at system level).** The judge outputs a "complete answer / what you missed" field after scoring, non-penalizing. This is the foil-after-recall pattern from methodology *Session-output docs: trap or tool* applied as a system primitive: recall-first, comparison-after, gap captured.

**UNCALIBRATED labeling until Week 4.** The judge produces convincing scores. That is precisely the danger. Reading rationales only shows internal coherence, not agreement with the user. The system declares **UNCALIBRATED** in its output until Week 4 calibration measures judge-vs-user agreement to ≥80% exact or κ ≥ 0.6. Until then, judge output is *suggestion, not measurement.*

**Deferred per build-right-vs-defer (Week 6):**
- **Follow-up question loop**: one extra probe when an answer is partial/uncertain. Depends on a trustworthy judge (can't stack interactive branches on an unverified foundation).
- **Stateful gap-memory**: re-probe the *exact* detail you skated past before durable. Pairs with the follow-up loop. v0 uses stateless escalating rigor instead.

**Components built:**
- `companion/app/scheduler.py`: deterministic spaced-repetition ladder
- `companion/app/bschecker.py`: tier-aware question generator + uncalibrated tier-aware judge (structured output)
- `companion/app/session.py`: interactive review loop
- `companion/app/store.py`: `claims` and `bs_checks` tables; review-queue + audit history
- `companion/app/main.py`: `check` command runs the interactive session

---

## Data model (v1)

### Decision log entry
```yaml
id: dl-YYYYMMDD-NNN
date: 2026-MM-DD
session: session-id
decision: <one sentence>
alternatives_considered:
  - <alternative 1>
  - <alternative 2>
rationale: <2-5 sentences>
expected_tradeoffs:
  - <tradeoff 1>
  - <tradeoff 2>
tags: [agentic, evals, rag, ...]
linked_artifact: <path or url>
claimed_learnings:
  - <claim 1>
  - <claim 2>
```

### BS-check record
```yaml
id: bsc-YYYYMMDD-NNN
date: 2026-MM-DD
target_claim: <ref to claim>
tier: spot | short | medium | long
question: <generated question>
answer: <my answer>
judge_score: 1-5
judge_rationale: <judge's reasoning>
self_score: 1-5 (optional, after seeing judge)
outcome: pass | fail
next_review: <date, computed by FSRS-style rules below>
notes: <any meta>
```

**Tier scheduling rules (v1):**
- `spot`: within same session as claim is logged. Required for every claim.
- `short`: first scheduled at +2 days after a spot pass.
- `medium`: first scheduled at +10 days after a short pass.
- `long`: first scheduled at +30 days after a medium pass. *(Tuned down from the methodology's default of +45 for this instance, Module 1 Week 3.)*
- **On pass:** advance to next tier (or extend long-interval review by ~2.5×).
- **On fail:** reset to previous tier or to short, whichever is shorter. Update notes with what was missed.
- **At long-tier success:** claim is flagged as durable. Reviews continue at long intervals indefinitely but with lower priority.

### Calibration set entry
```yaml
id: cal-NNN
question: <Q>
answer: <my answer>
my_label: 1-5
judge_label: 1-5
notes: <where they disagreed and why>
```

---

## Eval discipline

The companion is a system I trust to assess my own learning. If the judge is wrong, the system is worse than nothing: it tells me I understood things I didn't.

**Mandatory calibration before v1 ships:**

1. Hand-label 20-30 Q/A pairs covering the rubric's full score range.
2. Include deliberate **seed pairs** where I pretend to understand things I don't. Verify the judge catches them.
3. Compute agreement: % exact + Cohen's κ.
4. Iterate prompt until: ≥80% exact agreement OR κ ≥ 0.6, *and* all seed pairs caught.
5. Document failure modes: kinds of answers the judge still misses.

**Re-calibration trigger:** every model swap, prompt change, or rubric change. Don't trust unchecked judge changes.

---

## Framework choice (TBD, Week 1 of Module 1)

Comparison axis:

| Axis | LangGraph | CrewAI | OpenAI Assistants | Pydantic AI |
|---|---|---|---|---|
| Multi-agent primitives | | | | |
| State management | | | | |
| Persistence | | | | |
| Eval integration | | | | |
| Vendor lock-in | | | | |
| Maturity / docs | | | | |
| Personal ergonomics | | | | |

Run the same minimal workflow in each (orchestrator → two stub agents → state read/write) before deciding. Fill the table empirically. Output: `framework-choice.md`.

---

## Public / private / license

- **Repo visibility:** private through Module 1. Goes public at v1 ship (end of Module 1, Week 8) with a controlled launch post. Public from Module 2 forward, with every subsequent component built in the open.
- **Operational state:** decision logs, BS-check results, calibration hand-labels are local-only or gitignored. Never public, even after the code is. The operational data is mine; only the code is the world's.
- **License:** MIT, applied at first public commit.
- **Redaction policy:** code-side, sensitive content (specific dollar figures, identifying details, anything embarrassing) gets redacted to `[redacted]` before commit. Real names of people only with permission.
- **Naming:** TBD. Needs to be readable, not "Ben's Tutor." Decide before going public at v1 ship.

### Launch checklist (Module 1 Week 8)

Before flipping repo to public:
- README polished and scannable in 60 seconds
- Architecture writeup readable end-to-end
- Framework-choice writeup readable end-to-end
- Calibration writeup with documented agreement metric
- Working demo or at least demo-able state (script that runs)
- Gitignore covers all operational state
- LinkedIn / blog post drafted and ready to publish same day as repo flip

---

## Out of scope for v1

Explicitly not built. Listed so the v1 boundary is clear.

| Component | Note |
|---|---|
| Knowledge Cartographer (topic coverage map) | Originally planned as a later component; trajectory redirected. See Roadmap. |
| External-resource Curator (targeted reading recommendations) | Originally planned as a later component; trajectory redirected. |
| Retrospective Agent (cross-build pattern surfacing) | Originally planned as a later component; trajectory redirected. |
| Production governance layer (kill switches, shadow eval, audit log, monitoring) | Originally planned as a later component; trajectory redirected. |
| Improved eval discipline / fine-tuned judge | Originally planned as a later component; trajectory redirected. |
| Web UI | Not committed; CLI / terminal is fine for v1+ |
| Multi-user / authentication | Not committed; single-user for indefinite future |

---

## Roadmap

v1 is the substantial build. Subsequent versions are smaller, targeted iterations driven by real use rather than a pre-scheduled component-per-module trajectory.

| Version | Status | Adds |
|---|---|---|
| v1 | Shipped | Orchestrator, Decision-Log, BS-Checker, RAG, calibrated judge, log-time cross-claim consistency, single follow-up loop |
| v1.1 | Planned | `ingest` command: extracts claim-shaped statements from external transcripts (session exports, conversation logs) and registers them into the existing claims queue. Lets the BS-Checker probe curriculum learning the same way it probes build decisions, without manual logging per module. |
| Beyond v1.1 | Real-use driven | No pre-scheduled component additions. New capabilities only when real use of the tool surfaces a real need. |

The original v2-v6 trajectory (Knowledge Cartographer, Curator, Retrospective Agent, production governance harness, eval sophistication) was redirected after Module 1 in favor of curriculum modules that produce operator-shaped deliverables (audits, playbooks, frameworks, vendor maps) rather than additional companion components. The companion remains the verification substrate throughout the curriculum via v1.1's ingest path; it does not need to grow per module to play that role.

Each shipped version's spec lives in `spec-vN.md` in this directory.
