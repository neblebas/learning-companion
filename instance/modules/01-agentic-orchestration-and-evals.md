# Module 1: Agentic Orchestration + Evals

**Status:** Active. Weeks 1–6 complete; Week 7 (writeup and public ship) next.
**Start date:** _set when work begins_
**Target ship:** ~8 weeks from start (60-80 hours)
**Artifact:** Learning Companion v1. See `../../companion/spec-v1.md`.

### Progress

- ✅ Week 1. Framework comparison closed at two-framework depth (CrewAI and LangGraph implemented; Anthropic SDK and Pydantic AI evaluated via docs and named but not implemented, per the friction-is-signal discipline). LangGraph selected. See `../../companion/framework-choice.md`.
- ✅ Week 2. Companion v0 part 1: orchestrator (LangGraph, rule-based router), corpus store (SQLite index plus markdown documents), AI decision-logger (structured output, no-invent rule), retrieve path, and CLI. Logs and queries run through the orchestrator and persist across runs. Graph session-state kept transient; checkpointer deferred to Week 3 against a real reader. Code in `../../companion/app/`. **Time: 3.5 hrs** (budget 10–13; under).
- ✅ Week 3. Companion v0 part 2: the BS-Checker (uncalibrated). Claims-as-checkable-items, FSRS scheduler (spot/short/medium/long, long tuned to +30d), tier-aware question generator, tier-aware-rigor LLM-judge (verdict plus teaching field, flags ambiguous questions), and an interactive session loop wired to `check`. End-to-end BS-check flow works; **judge UNCALIBRATED until Week 4.** New code: `scheduler.py`, `bschecker.py`, `session.py`. **Time: ~2.5–3 hrs** (about 4 hrs elapsed with a ~1 hr break; budget 8–12, well under).
- ✅ Week 4. Judge calibration (the critical week). A 22-pair calibration set (8 genuine cold answers, 7 crafted, 7 seeds), blind-labeled on the 3-way verdict; the harness computes % exact, Cohen's κ, and seeds-caught. **Result: 82% / κ0.73 all, 88% / κ0.81 genuine, 7/7 seeds, gate met.** Key finding: the judge was non-deterministic at default temperature (the same rubric swung 88% to 75% across runs), fixed with **temperature=0** (byte-identical reruns). A "sharpen the rubric" iteration was tried and reverted, since its apparent effect was within run noise. New code: `calibrate.py`, `app/calibration/`. Deliverable: `../../companion/judge-calibration.md`. **Time: ~3 hrs** (budget 8–12; well under).
- ✅ Week 5. RAG and semantic retrieval. Local sentence-transformers embeddings (no API key, data stays local); compared MiniLM, bge-small, and bge-base on a hand-crafted query set, all tied (P@1 7/8, Recall@3 8/8; eval **saturated** at 8 entries), so chose **all-MiniLM-L6-v2** on size and simplicity, with no lock-in (re-embedding is cheap). Whole-entry chunking; brute-force exact cosine (numpy). Wired in as `query --find`, **closing the Week-2 exact-tag gap**. Security: dropped gte-base (`trust_remote_code`) for clean models. New code: `rag.py`, `rag_eval.py`. Deliverable: `../../companion/rag-notes.md`. **Time: ~2.5 hrs** (budget 8–12; well under).
- ✅ Week 6. Re-integration with RAG. At **log time**, each new decision's claims are cross-referenced against history (per-claim retrieval) through a **conservative tension-detector** (rigorous and additive-only; *related is not in-tension*, validated including a subtle false-positive case). A genuine tension is surfaced **immediately** and **spawned as its own tracked claim** (dedup via sorted-pair id; it climbs the tiers and is probed at review like any claim). *Firing point corrected from review-time to log-time, to catch the contradiction as it is introduced (the spot-check principle).* Added **retry/backoff** to all LLM clients after a sustained API 529 (deeper resilience goes to Module 5). Honest note: the compressed timeline meant no four-weeks-of-real-use feedback, so deferred-feature integration was substituted. Also built the **single follow-up loop** (deferred from Week 3): a `partial` answer gets one targeted follow-up at the specific gap, then the same calibrated judge re-scores the combined response (verified: partial to solid on supplying the missing piece). New: `rag.related_claims`, `bschecker.detect_tension`, `bschecker.followup_question`, `store.spawn_tension_claim`. Deliverable: `../../companion/v1-integration-notes.md`. **Carried forward:** my own first live cross-referenced `check` (the DoD real-use session). **Time: ~1.5 hrs** (budget 6–10; well under).
- ⬜ Weeks 7-8. See the weekly cadence below.

---

## Objective

Build the v1 of the multi-agent learning companion. By the end of this module, I will have:

1. **A deployed, in-use multi-agent system** with three agents (Orchestrator, Decision-Log, BS-Checker) coordinating over a persistent state and a small RAG corpus.
2. **A calibrated LLM-as-judge** powering the BS-Checker, with a documented agreement metric against my hand-labeled ground truth.
3. **A public GitHub repo** with code, architecture writeup, and framework-choice rationale.
4. **A published writeup** (LinkedIn long-form or blog) framing the companion as a multi-agent build-to-learn system, set apart from the existing single-agent prior art.

---

## Skills targeted

| Skill | Depth target | How it gets exercised |
|---|---|---|
| Multi-agent orchestration in a real framework (LangGraph / CrewAI / similar) | Hands-on, can build from scratch | Building the Orchestrator and agent routing |
| State persistence across agent interactions | Hands-on | Decision-Log corpus and session state |
| RAG basics (embedding choice, chunking, retrieval) | Hands-on, defensible choices | Decision-Log retrieval for the BS-Checker |
| LLM-as-judge design and calibration | Hands-on, can describe methodology | BS-Checker eval loop |
| Framework selection and comparison | Defensible writeup | Week 1 framework comparison |

**Explicitly not targeted in this module:** transformer internals, fine-tuning, multi-agent coordination at scale, production-grade ops. Those are later modules.

---

## Time budget

| Phase | Hours | Weeks |
|---|---|---|
| Framework comparison + scope lock | 6-10 | 1 |
| Companion v0 part 1 (orchestrator + state + decision-log) | 10-13 | 2 |
| Companion v0 part 2 (BS-Checker uncalibrated + review queue) | 8-12 | 3 |
| Use it daily + judge calibration | 8-12 | 4 |
| RAG component | 8-12 | 5 |
| Re-integration with RAG + iteration | 6-10 | 6 |
| Writeup + public ship | 8-12 | 7 |
| Buffer / docs polish | 4-8 | 8 |
| **Total** | **58-89** | **8** |

At ~7 hrs/wk average this is tight; at 10 hrs/wk it is comfortable. If a week slips, the slip eats into the buffer (Week 8), not into the calibration week. Calibration is non-negotiable.

**Cadence pivot rationale (from the spec-design conversation):** the original sequence built infrastructure linearly and reached a working v1 only at Week 7. The pivot builds a minimal v0 by the end of Week 3, then uses it daily from Week 4 forward to track real learning while iterating. Trade-offs accepted: Weeks 2-3 are bigger, and the system is uncalibrated for about one week of real use (Week 4, before calibration completes). Benefits: the tool earns its keep weeks earlier, the recursion ("AI to learn AI") becomes felt, and RAG in Week 5 has a real three-week corpus to retrieve over instead of synthetic data.

---

## Weekly cadence

### Week 1: Framework comparison + scope lock
- Compare LangGraph, CrewAI, OpenAI Assistants API, and Pydantic AI on the v1 scope (3 agents, persistent state, RAG, LLM-as-judge).
- Run the same minimal "hello multi-agent" workflow in each (or as many as time allows).
- Pick one. Document the rationale.
- **Deliverable:** `../../companion/framework-choice.md`, a 1-2 page writeup, public-quality from the start.
- **Why this matters in interview:** "I evaluated four frameworks before committing" is a strong answer to "why did you pick X?"

### Week 2: Companion v0 part 1 (orchestrator + state + decision-log)
- Set up the chosen framework. Get the orchestrator running with routing scaffolding.
- Decide state persistence: probably SQLite plus filesystem for v0 simplicity. Document the choice.
- Build the Decision-Log Agent: an ingest interface for build decisions and learning claims, structured into a queryable corpus.
- Simple retrieval (exact match, filter, tag) for now; RAG comes later in Week 5.
- Stub the BS-Checker route (don't build it yet; that is Week 3).
- **Deliverable:** can log decisions and claims via the orchestrator, and query them back. State persists across runs.

### Week 3: Companion v0 part 2 (BS-Checker uncalibrated + review queue)
- Build the BS-Checker Agent: it generates probing questions from logged claims.
- Implement the LLM-as-judge prompt v1 (uncalibrated, explicitly flagged as not yet trustworthy).
- Build the review queue: track which claims are due for which tier (spot/short/medium/long) per the FSRS rules in the methodology.
- Wire it to a session loop: present a question, accept an answer, judge it, schedule the next review.
- **Deliverable:** the end-to-end BS-Check flow works. Companion v0 is in active use for tracking learning claims from this point forward. Judge scores not yet trustworthy.

### Week 4: Use daily + judge calibration **(the critical week)**
- Use companion v0 daily for real learning capture (any module work, life learning, whatever you are studying).
- Hand-label 20-30 question-answer pairs from real use with your own scores.
- Run the judge against the same pairs.
- Compute agreement (% exact and Cohen's kappa).
- Iterate the judge prompt: add few-shot examples, refine the rubric, add chain-of-thought.
- Target: ≥80% exact agreement or κ ≥ 0.6 before declaring the judge usable.
- **Seed with intentional bad answers** (things you are pretending to understand), and verify the judge catches them.
- **Deliverable:** `../../companion/judge-calibration.md`, documenting the calibration set, methodology, agreement metric, and known failure modes. From this point forward the judge is trustworthy.

### Week 5: RAG component
- Compare 2-3 embedding models on the real accumulated corpus (now about three weeks of decision logs from Weeks 2-4).
- Pick a chunk strategy. Document why.
- Wire retrieval into Decision-Log queries.
- **Deliverable:** working RAG over the real corpus. A quick eval of retrieval quality on a small set of hand-crafted queries against your real entries.

### Week 6: Re-integration with RAG + iteration
- The BS-Checker now uses RAG to find related past claims when generating questions (cross-reference the current claim against your history).
- Fix things that broke in four weeks of real use.
- Adjust the system based on what real use revealed.
- **Deliverable:** companion v1 in mature use. Documented changes from real-use feedback.

### Week 7: Writeup + public ship
- README, architecture writeup, framework comparison, calibration writeup, and real-use retrospective all polished.
- Public GitHub push (MIT license).
- LinkedIn or blog post: "A multi-agent build-to-learn companion: what's actually different from single-agent AI tutors."
- Module retrospective written.
- **Deliverable:** publicly visible, linkable, demonstrable.

### Week 8: Buffer + docs polish
- Address any deferred friction from Weeks 2-7.
- Tighten rough edges in the public surfaces.
- Review parking-lot entries for anything ripe to close.
- **Deliverable:** none required, this is buffer. If everything is clean, start scoping Module 2 here.

---

## Resources (instrumental, narrow)

Pull as needed. Do not read in advance.

- **LangGraph docs** (state management, conditional edges), needed in Week 2-3 if LangGraph is chosen.
- **CrewAI docs**, needed in Week 1 for comparison.
- **OpenAI Assistants API**, needed in Week 1 for comparison.
- **Pydantic AI**, needed in Week 1 for comparison.
- Anthropic's [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents), short, read in Week 1.
- LLM-as-judge calibration: [G-Eval paper](https://arxiv.org/abs/2303.16634) and the [Vicuna LLM-as-judge writeup](https://lmsys.org/blog/2023-06-22-leaderboard/), read in Week 5-6 only, narrow.
- RAG: chunking strategy comparisons, read in Week 4 only.

**Anti-pattern:** spending Week 1 reading textbooks. Spend Week 1 *running* the frameworks against a hello-world workflow.

---

## BS-check questions (locked in advance)

These get probed by the companion itself across multiple tiers (spot at time of work, then short, medium, and long intervals; see `../../companion/spec-v1.md` for the schedule). **Lock them now**, before doing the work, so I can't game them.

Each question's *first* check tier is noted. All questions cascade to long-tier eventually; passing at long tier is the interview-defensibility bar.

1. **[first tier: spot, Week 1]** Explain the difference between LangGraph and CrewAI in their approach to state management. What did I actually choose, and why?
2. **[first tier: spot, Week 4]** How did I calibrate the LLM-as-judge? What was the agreement metric, what was the value, and how was it computed?
3. **[first tier: short, after Week 3]** Walk through the data flow when I make an "I learned X" claim to the companion. Which agents touch it, in what order, with what state changes?
4. **[first tier: spot, Week 5]** What chunk strategy did I use in the RAG component, and what tradeoff drove the choice? What would I change at 100× corpus size?
5. **[first tier: medium, after Week 7]** Where would the companion break first at 10× users? At 1000× users? What would I add to handle each tier?
6. **[first tier: medium, after Week 7]** Name three things the BS-Checker can't reliably catch. Why?
7. **[first tier: short, after Week 4]** What was the failure mode that made me change something material in Week 3 or 4? (If I don't have one, that is a flag that calibration was too easy.)
8. **[first tier: spot, Week 4]** Why is reading the judge's rationales not enough to trust it? What does calibration actually measure that reading cannot? (This is the "looks good is not the same as trustworthy" insight from Week 3, locked as a probe before Week 4 begins so it can't be gamed by the process of doing calibration.)

---

## What this gives me

- Concrete framework fluency I can demo and discuss.
- Hands-on RAG implementation with defensible choices.
- A real eval framework with a documented calibration story.
- A deployed multi-agent system with persistent state.
- A public GitHub artifact and writeup.
- A confident answer to "tell me about your AI work" that is about a *shipped* system.

## What this doesn't give me

- Transformer internals: covered at conversance level in Module 2's foundations consolidation; depth is out of curriculum.
- RL / RLHF: literacy only, covered in Module 2's foundations consolidation.
- Fine-tuning hands-on: out of curriculum.
- Production-scale ops: not built into the companion; production governance vocabulary is in Module 3.
- Enterprise-specific deployment patterns: addressed in Module 4 (applied AI in operations + shipped operating mechanism).
- Vendor landscape literacy: Module 7.
- Formal AI governance vocabulary: Module 3 (NIST AI RMF + EU AI Act).

Be explicit about these gaps when discussing the artifact. The credibility comes from being honest about what it does and does not demonstrate.

---

## Definition of done

All of these, or the module is not complete:

- [ ] Companion v1 in active use by me: at least 5 real decisions logged, at least 2 BS-check sessions completed.
- [ ] Public GitHub repo with README, architecture writeup, framework-choice writeup, calibration writeup.
- [ ] Calibrated judge with a documented agreement metric (≥80% exact or κ ≥ 0.6).
- [ ] LinkedIn or blog post published.
- [ ] Module retrospective written in `../retrospectives/`.
- [ ] BS-check questions locked and the first one scheduled.
- [ ] Companion's first real-use BS-check session completed.

---

## Open decisions (resolve in Week 1)

- **Framework choice:** TBD (LangGraph / CrewAI / OpenAI Assistants / Pydantic AI). Decide via comparison.
- **State persistence:** SQLite plus filesystem versus a vector DB versus something else. Probably SQLite plus filesystem for v1 simplicity; revisit later only if real-use scale demands it.
- **Embedding model:** TBD (Week 4).
- **Judge model:** TBD. Probably Claude or a GPT-4-class model; keep the *system under test* and the *judge* on different model families to avoid self-favoring bias.
