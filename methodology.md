# Methodology

Universal principles for self-directed adult professional AI learning. Pair with the templates in `framework/` and the companion tool in `companion/`. For an applied example, see `instance/`.

---

## True North discipline

Every instance starts with a True North paragraph: who you are, what role or outcome you're optimizing for, and the explicit non-goals.

Reread monthly. Edit only when the targets or context actually change, not when a shiny topic crosses your desk.

The paragraph's job is to be the anti-drift trigger: when you notice yourself slipping into a curriculum that doesn't translate to your target outcome, this paragraph is what stops you.

---

## Three operating rules

1. **Build > read.** Every module produces a tangible shipped artifact. Reading is instrumental to a build, never the primary mode. *"Build" does not mean "type every character yourself"; see "Building with AI assistance" below.*
2. **Ship > consume.** A small thing in active use beats a large thing in notes.
3. **Spot check, then retention check.** Every claimed learning gets a same-session spot check ("can I explain this back without hand-waving?") and then a multi-stage retention check. The long-interval pass is what makes it interview-defensible cold.

---

## Motivation alignment as design constraint

This methodology measures what matters for the learner's actual target outcomes. It avoids exhaustive completeness, pedantic precision, and engineer-grade detail when the target is operator-grade fluency.

A test that doesn't reflect the learner's real progress is worse than no test at all. Tests like that actively misdirect effort and erode motivation. When the methodology produces friction without producing signal toward the learner's actual goals, the methodology is wrong, not the learner.

**Friction-is-the-signal applies to the methodology itself.** Learner frustration is data about the system's design quality. A motivated learner who pushes through misalignment AND flags it is doing user research on the methodology. A less-motivated learner just quits silently. The discipline of treating frustration as design feedback is what keeps the methodology honest; without it, the methodology drifts toward the wrong things and fails learners silently.

**Critical caveat: this is not a license to lower the bar.** The goal of this methodology is genuine learning, comprehension, and skill-building toward the target outcome. It is **not** comfort, ego-stroking, or removal of all friction. Real learning requires productive frustration: wrestling with hard concepts, sitting with ambiguity, struggling to explain something the first few times, failing at first attempts. **Productive frustration is a feature of real learning and must not be removed.** Two kinds of friction to distinguish:

| Kind | What it looks like | Methodology response |
|---|---|---|
| **Productive frustration** | Wrestling with a real architectural concept at the right level; struggling to articulate something you understand intuitively; failing at a first build attempt; the "I almost get it" stage | **Sit with it.** This *is* the learning. Don't soften, don't shortcut, don't lower the bar. |
| **Misalignment friction** | Memorizing API details for a role that doesn't require them; perfecting phrasing on concepts already internalized; pushing precision on fields that don't drive any downstream decision | **Recalibrate.** The methodology is wrong. Change the test, and keep the learner's bar. |

**The failure mode this caveat prevents.** "Motivation alignment" could easily drift into people-pleasing or dumbing-down. If an assistant (or the eventual BS-Checker) reads frustration as *"we should make this easier"* rather than *"we should check whether the test is calibrated to the goal,"* the methodology becomes a comfort machine that produces no real learning. The discipline is exactly the opposite: hard tests aligned to actual outcomes, easy tests removed, hard tests at the wrong level recalibrated to the right level, never lowered.

**The bar that does not drop:** the long-tier BS-check. *Can the learner defend the load-bearing claims cold, weeks after the work, in an interview for their actual target role?* This bar is hard by design. If the methodology lowers this, it has failed.

**Practical implications:**

- Probe at the right level for the learner's actual target outcome (see *Probe calibration*).
- Measure what reasonably needs measuring; don't push precision beyond what serves the goal.
- *"I don't remember the exact API"* is not a learning gap when the target role doesn't require holding the API. It's correct calibration.
- *"I'm not sure how to phrase this"* on a probe question whose architectural concept the learner has internalized is not a comprehension gap. The wording doesn't need polish; the concept is held.
- When in doubt, ask: *"Does pushing on this serve the learner's actual target outcome?"* If no, stop pushing.

**Why this matters for the companion (recursion alert).** This methodology will eventually be encoded as the companion's BS-Checker logic. Whatever the methodology rewards or punishes will be reflected in how the BS-Checker treats every future user. Mis-calibration here propagates into the product; calibrating the methodology IS calibrating the product. Catching mis-calibration early is design work, not personal preference.

---

## Building with AI assistance

This methodology is written for adult professionals who are not (and don't need to become) hands-keyboard software engineers. If you're using Claude Code, Cursor, Aider, or a similar AI development tool as your primary build surface, the methodology still works, but the discipline shifts. What matters is *what you can defend*, not *who typed the keys*.

This is closer to actual target-role behavior than the keyboard-time framing would be. Senior operators, AI deployment leads, and AI product managers in 2026 do not generally write framework implementations by hand. They direct the work, read the output, catch issues, make structural calls, and can defend the architecture cold. That's the skill being demonstrated, and the methodology measures it directly through the BS-check, not indirectly through how the code got typed.

**Failure mode this discipline prevents:** *accept-everything mode.* The AI writes 200 lines, you accept the diff, you have no idea what just happened. Learning is zero. Interview exposure is one technical follow-up away.

**The discipline that converts AI-assisted building into real learning:**

- **Direct, don't delegate.** Specify *what* to build, not implementation details. Architectural choices (framework, model, primitives, state shape, persistence target) are yours. Implementation details can be delegated.
- **Read diffs before accepting.** Every line should make sense, or you ask. "Why this primitive and not that one?" is a fine question. "Walk me through what happens when input X arrives" is better.
- **Make architectural decisions yourself.** The AI implements at your direction. If you find yourself letting the AI pick the framework, the model, or the design, pause. That's the part that's *yours*.
- **Run it yourself, read the output.** Don't trust "looks good." Trust observed behavior matching expected behavior.
- **Closed-book walkthrough at milestones.** Close the AI tool. Open the file. Explain to yourself (out loud or on paper) what each section does. If you stumble, that's a flag; revisit before moving on. This is the same idea as the spot-tier BS-check, applied to *code* rather than *claims*.

**The BS-checker matters MORE in this setup.** It's the safety net that catches "the AI wrote it, I never really learned it." The long-tier BS-check is the interview-defensibility test: if you can't answer it cold, weeks after the build, the AI did it and you didn't. The methodology fails silently if the BS-check is skipped or watered down in this mode.

---

## Spec design discipline

This methodology applies to anyone designing learning work, whether that's you, a collaborator, or an AI assistant helping you scope the next module or write a spec. The "Building with AI assistance" section above is rules for the *learner*. This section is rules for the *spec-author*, because the failure modes are different but structurally analogous.

**Failure mode this discipline prevents:** writing a spec that produces measurements (scorecard fields, rubric items, BS-check questions, retrospective claims) the build itself cannot generate evidence for. The learner ends up filling in the unanswerable fields with research, opinion, or the spec-author's prior knowledge, none of which counts as built understanding. The spec is then dressed up to look like build evidence but is actually read evidence.

**The discipline that prevents it:**

- **Mental walkthrough of the build before locking the spec.** If a hypothetical learner executes the spec exactly, what concrete evidence will they have at the end? Walk it through step by step.
- **Every scorecard / rubric / BS-check field must be answerable from that evidence.** If a field requires external research or the spec-author's prior knowledge, either change the spec to exercise that capability, or mark the field explicitly as "research, not build" and treat it accordingly (it doesn't count as defensible from the work).
- **Apply "no claims without checks" to the spec itself.** The implicit claims a spec makes about what the learner will know after doing it must survive a learner-simulation test. Run that simulation explicitly before locking the spec.
- **Specs are themselves BS-check fodder.** When a spec is drafted, the immediate question is: *which fields in the produced scorecard will the build actually let the learner defend cold?* Any that won't are flags. Either fix the spec or label the field honestly.

**Why this matters more when AI assistants help design specs.** LLMs writing methodology and specs do not have a persistent unified perspective checking new work against prior commitments. Inconsistencies that span responses can be invisible to the AI and require explicit human review to surface. The methodology working as designed *includes* the human catching things the AI can't, and that's a feature, not a bug. If you're working with an AI assistant on a spec, the human-side discipline is: "Would a learner who only does this spec be able to answer these fields without consulting anything else?" If no, push back.

---

## Friction is the signal

In comparison work and build-to-learn contexts, what *fails* often reveals more about a system's true behavior than what succeeds. A framework that runs smoothly may be hiding tradeoffs behind defaults; a framework that breaks reveals where its hidden dependencies, default assumptions, and architectural compromises actually live.

**When to invoke this discipline.** You're partway through a build and hitting unexpected friction: auth bugs, missing dependencies, naming gotchas, native crashes, configuration surprises. The instinct is to grind on the original goal until it works. The friction-is-signal move is to *pause*, ask "what does this friction reveal that I wouldn't have learned from a clean run?", and capture that as primary learning before deciding whether to keep debugging.

**The discipline:**

- **Friction reveals architecture.** A `huggingface` vs `sentence-transformer` naming collision is evidence of the framework's provider-registry design. An `OPENAI_API_KEY` required for embeddings despite using Anthropic for agents is evidence that "vendor-agnostic" claims have boundaries. Read failures as architectural disclosures.
- **Document friction immediately.** Failed runs produce data points only if you write them down before context fades. The session log + notes file are the artifact when the working code isn't.
- **Decide to continue debugging based on signal, not stubbornness.** Will additional debugging produce *additional* signal, or are you now retrying the same thing hoping it works? If the latter, stop.
- **Time-box still applies.** Friction-as-signal is not a justification for grinding past the cap. It's a re-frame for what counts as a successful outcome *at* the cap.
- **Close the loop honestly.** *"I attempted X. The implementation hit Y, Z, W. I captured these as comparison data points. I did not complete X."* That sentence is a defensible interview answer. *"I tried, I failed, I gave up"* is not.

**Failure modes to avoid:**

- Mistaking this for "any failure is fine." Friction-as-signal requires the friction to be *captured*, turned into documented data points. If you bail without writing it down, you have neither the artifact nor the learning.
- Using it to justify grinding past time-boxes. The discipline re-frames what counts at the cap; it does not eliminate the cap.
- Applying it where you actually need a working artifact. If downstream work depends on this thing running, friction-as-signal isn't enough; you need to resolve it.

**Why this matters especially for AI-assisted builds.** The AI's instinct will often be to grind on the original goal: fix the next error, then the next, then the next. The human-side discipline of "stop, what does this friction reveal?" is one of the most important applied roles for a learner directing rather than typing. It's also exactly the kind of judgment senior operators and AI deployment leads exercise in real projects, making the call to stop, name what was learned, and not let sunk cost dictate the next move.

---

## Time-boxing: different rules for evaluation vs. production work

Time-boxes serve different purposes in different work contexts. Applying the wrong frame creates either premature abandonment of necessary work or grinding past sensible limits. The *Friction is the signal* discipline assumes evaluation context by default, but most module work is production, and the rules differ.

### Evaluation / comparison work (e.g., framework selection, vendor evaluation, candidate-approach shootouts)

Time-boxes are **hard caps with bail behavior.** When the cap hits:

- Stop pushing on the current implementation.
- Log the friction as a comparison data point; this is exactly where *Friction is the signal* fires.
- Move to the next thing being evaluated.

The work here is collecting signal, not producing a working artifact downstream work depends on. Bailing at the cap doesn't break anything; it just means one fewer data point in a comparison where partial coverage is acceptable.

### Production-build work (building artifacts the rest of the module depends on)

Time-boxes are **tiered, with different responses at each tier.** Bailing on production work means the artifact doesn't exist for downstream work; that's broken-cadence, not friction-as-signal.

| Tier | Methodology constraint? | What to do when hit |
|---|---|---|
| **Per-session (learner-defined)** | No: personal pacing, not a methodology rule | Learner's choice. Some pace in 90-minute blocks; others work in irregular windows determined by available time. **Methodology does not prescribe a session length.** When the session ends (by your choice), save state, commit, note what's next. |
| **Per-week budget** | **Yes: scope discipline** | Pause and reassess. Cut scope, adjust slightly into next week, or recognize an architectural problem requiring step-back. Not "push harder." |
| **Total module budget** | **Yes: real hard wall** | Genuine re-plan. Determine what's load-bearing vs. cuttable. If the wall has been blown through significantly, the methodology itself may need adjustment for future modules. |

**Note on session pacing.** Adult professional learners often have sporadic, irregular available time: a 4-hour block one weekend, 30 minutes another evening, nothing for a week, then a long stretch. Forcing artificial session caps wastes the productive blocks the learner actually gets. Use the time you have; stop when you need to. The methodology cares about week-level scope and module-level totals, not session length.

**Estimates are starting points, not constraints; recalibrate to the specific learner.** Generic time estimates in module specs (e.g., "8-12 hours for Week N") are scoping placeholders, not personal forecasts. Real per-learner pace varies dramatically based on prior experience, AI-direction skill, and decisiveness. Treat *actuals* as the signal:

- After 2-3 weeks of consistent actuals, recalibrate forward estimates to the learner's observed pace.
- "Banked time" is the wrong framing; coming in well under generic estimates is a *recalibration signal*, not headroom to spend.
- The right operational reading: track actuals against estimates, refine forward, document the learner's actual pace in their operator profile. Don't treat the original estimates as the truth; they were guesses.
- This protects against two failure modes: (a) treating early under-budget weeks as license to expand scope unnecessarily, and (b) treating late over-budget weeks as personal failure rather than estimate error.

**The "Propose plan first" discipline earns its keep at the per-week tier.** If a proposed plan looks too ambitious for the week's budget, push back at *plan* time, not at hour 12. Plan-time scope cuts cost minutes; hour-12 scope cuts cost the week.

### How to tell which context you're in

- *Evaluation work:* goal is collecting signal about something (frameworks, vendors, approaches). Output is a comparison artifact. Downstream work doesn't depend on every option being fully implemented.
- *Production work:* goal is producing a working artifact that downstream work builds on. Bailing means a real gap someone (probably future-you) will have to fill.

When in doubt, ask: *"If I bail at the cap, does next week's work still function?"* If yes → evaluation rules. If no → production rules, and at most you stop a *session*, not abandon the work.

---

## Measurement vs. comprehension-probe: separate them; weight the probes highest

Every rubric, scorecard, retro template, and BS-check carries two distinct kinds of field. They look the same on the page but they measure different things, and conflating them produces a recurring confusion: *"is this document gauging my learning, or just recording correct answers?"* Both, but at different moments and in different places.

| Field type | Definition | Examples | How to fill it |
|---|---|---|---|
| **`[measure]`** | An outside observer with no build access could answer this via docs, code, or search. Recall is *not* required. | Lines of code, setup time, framework primitive names, env var values, version numbers, install steps | Measure or look up accurately. No recall ceremony. The assistant may compute and hand over the precise number. |
| **`[probe]`** | Only a builder who *did* and *understood* the work can answer this. Recall *is* the point. | "Why does this build need manual state.py when the framework has its own state?", design tradeoff rationales, qualitative ergonomics, "what surprised you and why" | Recall from memory first. The divergence between recall and correct answer is the learning signal, never the polished text. |

**The boundary test:** if the answer is LLM-searchable, it's `[measure]`. If only the build's author can defend it cold in interview, it's `[probe]`. Mixed fields get explicitly tagged `[mixed]` with their measure and probe sub-components named.

**The weighting:** `[probe]` fields bear the **greater** weight. They are the true learning gate. `[measure]` fields are reporting and administration, important for the document's downstream accuracy, but they tell you nothing about whether learning happened.

**Resolves the felt conflict** between "honest gauge" and "correct document" by separating them in *space*: the honest recall lives in the moment of comparison and the parking-lot recall-gap entry; the corrected text lives in the scorecard. The scorecard ends up accurate; the learning signal is preserved elsewhere. Same `[probe]` field is filled by recall first, corrected after, and the divergence is what got measured.

**Rule for assistant behavior on probe fields.** The assistant flags **only genuine fact or understanding gaps**, never phrasing polish. Test before suggesting any edit to a `[probe]` answer:

- Is the divergence a *fact or understanding gap* (legitimate to flag; log to parking-lot recall-gaps)?
- Is the divergence a *reporting-polish gap* (the learner's wording captures their actual understanding; polishing it erases the signal)?

If the latter, **leave the wording alone.** Polishing "No friction" to "No friction, no default to override" on a `[probe]` field is the failure mode. If the learner already understood there was no default to override, the polish adds nothing real; it just makes the document look sharper while destroying the measurement of what the learner actually knew.

**Per-module comprehension-probe set, locked first.** For every module, define a small set of `[probe]` questions up front (same discipline as BS-check questions, locked before the work so they can't be gamed). Treat these as the *primary* learning gate, weighted highest. Scorecards and measurement fields exist to support the document's downstream uses; probes exist to measure whether learning happened. Both matter; the probe set is what determines whether a module's learning succeeded.

This discipline complements **Spec design discipline** (specs must produce evidence the build can generate) and **No unverifiable scorecard fields** (no fields without buildable evidence). Together they ensure scorecards measure what they claim to measure rather than acting as polished facades.

---

## Probe calibration: anchor to the actual target outcome

The *Measurement vs. comprehension-probe* discipline splits fields by what kind of answer they require. Probe calibration adds the next-order question: **for `[probe]` fields, what *level* of probe is appropriate?** The answer depends on what the learner is actually trying to achieve.

**The calibration test:** before locking a probe question, ask *"Would someone evaluating the learner against their actual target role or outcome reasonably probe this?"* rather than *"could anyone anywhere probe this?"*

For an operator targeting AI Workflow Lead, AI PM, or COO/CoS-with-AI-fluency roles (Tier 1-3 of typical career-pivot frames):

- **Appropriate probes:** Why did you choose framework X over Y? What does this design tradeoff reveal about the framework's priorities? How would you deploy this in [specific domain]? How do you measure if it's working? What would you change at 10× scale? Tell me about a failure mode you hit and what it taught you.
- **Inappropriate probes:** Name the framework's primitive. What's the exact API for X? Recite the env var. Recall the precise lines-of-code count. Explain the internals of someone else's library.

The first set tests **reasoning**, the actual skill being built. The second set tests **memorization**, a low-value, low-transfer activity the learner can do at lookup time when needed.

**Two failure modes that fire simultaneously when probes are mis-calibrated:**

1. **The learner can't answer** (because the answer is dead-string memorization they shouldn't be holding) → registers as a learning gap → logged to parking-lot → revisited later → still can't answer because the question is still mis-calibrated. The cycle wastes attention and creates the false impression of stuck progress.
2. **The learner *can* answer**, but spent disproportionate effort memorizing → registers as success → reinforces the wrong skill. The learner is being trained to be a worse version of themselves for the actual role.

Both failure modes are silent unless someone catches the mis-calibration. Catching it is what this discipline exists to do.

**Specific guidance for AI-assisted methodology and review.** When an AI assistant proposes or polishes a probe question, OR flags a learner's answer as wrong/incomplete on a probe field, the assistant must apply the calibration test first. If the divergence between the learner's answer and the "ideal" answer is at a level the actual target role wouldn't probe, **the assistant's flag is itself the bug.** Leave the answer alone. Polish on mis-calibrated probes is exactly the failure mode *Measurement vs. comprehension-probe* warns against, but applied to questions that shouldn't have been asked at the current level in the first place.

**The companion will inherit this.** When the BS-Checker is built, its probe-generation logic will use whatever calibration this methodology encodes. Probes that fire at the wrong level will demotivate every future user silently. Calibrating here = calibrating the product.

---

## Vocabulary calibration: the mainstream middle band

The *Probe calibration* discipline anchors probes to target outcomes. Vocabulary calibration is the tactical companion: **what level of technical vocabulary is appropriate when probing, explaining, or comprehension-checking?** Mis-calibration on vocabulary is one of the most common drift modes in AI-assisted learning sessions, and one of the most demotivating when it fires.

For operators targeting AI Workflow Lead, AI PM, COO/CoS-with-AI-fluency, or AI Deployment Lead roles (Tier 1-3 of the career framework), there are three vocabulary tiers:

| Tier | Examples | Status |
|---|---|---|
| **CEO / business** | Strategy, ROI, vendor selection, governance, risk, build-vs-buy, total cost of ownership | Floor; learner already has this |
| **Cross-functional operator (THE TARGET BAND)** | structured output, schema, API call, state, orchestration, index, router, RAM vs. disk, idempotent, checkpoint, persistence, transient, durable, dual-write, normalization, latency, throughput, deterministic vs. probabilistic, prompt engineering, eval, fine-tune, embedding, vector search, RAG, agent, tool use, retrieval, LLM-as-judge, observability, tracing | **Calibrate here** |
| **Dev-fluent** | Specific method names (`executemany`), syntax, type signatures, library internals, exception classes, framework-specific APIs, async/await mechanics, recursion patterns | Out of scope; never quiz at this level |

**The middle-band test:** *"Could a CTO use this term in a meeting with the learner and reasonably expect them to follow, push back, or ask a clarifying question at the same level?"*

- If yes → middle band → in scope for explanation, probing, comprehension checks.
- If the term only matters when typing code → dev-fluent → **out of scope.**

**Rules for the assistant (and the eventual BS-Checker):**

1. **Actively name and define mainstream cross-functional terms** when they come up. Don't avoid the term to "simplify"; that strands the learner without the vocabulary they need to talk to engineers and CTOs. Give the concept AND the label.
2. **Never quiz on dev-tier specifics.** Method names, syntax, library internals, exact API signatures are `[measure]` (the assistant's job to get right). Architecture rationale and middle-band terms are `[probe]` (the learner's actual learning gate).
3. **Explanations in plain English with analogies, always.** Even when naming middle-band terms, the explanation is plain English. The label gives them the vocabulary; the analogy makes the concept stick.
4. **Code-side teaching pattern.** Showing code for transparency is fine, but with a plain-English "what & why" written alongside it. Never make *reading the code* the comprehension gate.

**Why this matters for the companion.** The BS-Checker's probe-generation will inherit whatever vocabulary tier the methodology rewards. Probes pitched at dev-fluent level will demotivate operators every time. Probes pitched at CEO-only level will underbuild the vocabulary the role actually requires. The middle band is what makes the companion useful for operators with AI-fluency targets.

**Drift mode this prevents.** Without explicit vocabulary calibration, AI assistants drift toward dev-tier probing because that's where the AI's own vocabulary lives. The learner's frustration in those moments is correct methodology signal: the assistant is mis-calibrated, not the learner under-prepared.

---

## Track structure

Two tracks per instance:

| Track | Purpose | Cadence |
|---|---|---|
| **Curriculum (B)** | Structured skill development through sequenced modules + parallel lanes | Monthly modules, continuous lanes |
| **Portfolio (C)** | Ledger of shipped artifacts, the proof of what you've actually done | Continuous |

Interview prep is *not* a track here. If you're job-searching while learning, interview prep lives in its own working directory and preempts curriculum work when the funnel demands it. There is no automated cross-context sync.

---

## Multi-tier BS-check methodology (FSRS-style)

Every claimed learning is checked at multiple intervals:

| Tier | When | Question |
|---|---|---|
| spot | same session | Can you explain it back without hand-waving? |
| short | +2 days after spot pass | Survived the immediate forgetting curve? |
| medium | +10 days after short pass | Transferred to durable memory? |
| long | +45 days after medium pass | Defensible cold in an interview? |

**Rules:**
- On pass, advance to next tier (or extend long-tier review by ~2.5×).
- On fail, reset to the previous tier or to short, whichever is shorter.
- At long-tier success, claim is flagged as durable. Reviews continue at long intervals indefinitely but at lower priority.

**Calibration is mandatory.** If you use an LLM-as-judge to evaluate your own learning claims, you must calibrate it against your own ground-truth labels first. Uncalibrated judges produce feel-good feedback. Target: ≥80% exact agreement or κ ≥ 0.6, *and* the judge catches deliberately seeded bad answers.

### Determinism before measurement: fix LLM judge variance before tuning

When measuring an LLM-as-judge's agreement with ground truth, **the judge must be deterministic first.** Default LLM sampling (non-zero temperature) introduces output variance that is indistinguishable from rubric changes in a small calibration set.

**The trap.** Run calibration → get a number. Change the rubric to address a disagreement. Re-run → get a different number. Attribute the change to your edit. But with a thin calibration set (n=20-30), single-run differences can be entirely sampling noise; you cannot separate the rubric change's effect from random variation.

**The fix.** Set the judge's temperature to **0** (or as deterministic as the API allows). Re-run calibration twice and verify byte-identical results. Only then is the agreement metric usable for evaluating prompt changes.

**Generalizes to any eval where an LLM is the rater.** Determinism is a prerequisite to measurement; without it you're measuring noise, not your changes.

**Recalibration trigger:** every model swap, prompt change, or rubric change. Temperature must stay at 0 across all comparisons or the comparison is invalid.

*Discovered by Module 1 Week 4 of the reference instance: a rubric "sharpening" appeared to lower agreement; reverting to the same rubric gave different numbers again; investigation found default-temperature sampling was the variance source.*

### Gaps are fuel: what calibration actually measures

A common misreading of LLM-as-judge calibration: *"If my answers are wrong, my labels will skew the data."* This is incorrect, and worth naming explicitly because the misreading discourages learners from doing the calibration honestly.

**What calibration measures:** whether the judge's grade of an answer **matches the learner's grade of that same answer.** The unit being labeled is `(answer → quality)`. The ground truth is the learner's honest judgment of answer quality, **not** the answer's correctness.

**Consequence:** you don't need to know every answer cold. You need a *spread* of answer quality (solid, partial, wrong examples) so the judge has something to be calibrated against across the full range. **A calibration set of all-correct answers is useless** (nothing in the partial/wrong range to verify the judge against).

**Gaps are fuel.** Honest "I don't remember this" or "I half-understand this" answers ARE calibration data. They populate the partial and wrong ranges. The whole point is to test whether the judge agrees with you on what those answers look like at each grade.

**The real risk is mislabeling, not knowledge gaps.** The single-rater blind spot: thinking a vague answer was solid, or thinking a correct-but-rough answer was wrong. Mitigations:
- **Seeds** (confident-but-wrong "pretend I understand" answers citing plausible-but-false reasons) test the wrong end of the distribution.
- **Crafted anchors** (known-quality reference answers) test the solid end.
- **Grade cold** before seeing the judge's output, so anchoring bias doesn't drift your labels toward the judge's.

If a learner finds themselves trying to "give better answers" to make calibration succeed, the test has been inverted. The judge needs to handle bad answers correctly; making them rare hides the failure modes the calibration exists to surface.

---

## Parking lot: deferred encoding

Not every observation can be processed in the moment it's made. When you encounter something during a build that you *noticed* but cannot yet fully *explain* (a framework behavior that surprised you, a concept that almost made sense, a primitive whose purpose was unclear), log it in the instance's `parking-lot.md` and move on.

This is *deferred encoding*: marking concepts you're not ready to fully process and letting them ripen through repeated exposure. It's an intentional learning pattern, not a failure state.

**The discipline:**

- **Log, don't grind.** When something is unclear after a reasonable attempt to understand it, write a brief entry (date, what you noticed, what's unclear, where you saw it) and move on. Grinding on an unclear concept until you "get it" often produces frustration without learning; deferred encoding lets later context illuminate it.
- **Revisit when context arrives.** When a similar concept reappears in a later module, open `parking-lot.md` and look for relevant entries. Either close them ("now I understand X") or extend them with new observations.
- **Honest about what's not understood.** Parking-lot items are explicit acknowledgments of gaps. That honesty is more useful than fake claims of understanding, and it interacts cleanly with the BS-check discipline. A scorecard field that points to a parking-lot entry is a defensible position; a scorecard field padded with hand-waving is not.
- **Not a backlog.** Parking-lot items aren't tasks to grind through. They're markers waiting for context. The right cadence to revisit them is "when the topic reappears in active work," not "weekly homework."

**Why this matters with build-to-learn methodology.** The build-to-learn loop produces real observations faster than they can be fully processed, especially in early modules with heavy unfamiliar vocabulary. A learner who insists on understanding every observation immediately will either slow the build to a crawl or fake understanding to keep moving. Parking-lot is the third option: continue the build, mark what's unclear, revisit when ripe.

This pattern is what active learners do naturally. The methodology making it explicit gives you permission to do it as a sanctioned practice.

---

## Module activation protocol

When a module transitions from Planned to Active:

1. Create the module spec file (copy `framework/module.template.md` to `instance/modules/0N-<slug>.md`).
2. Lock the BS-check questions **before** starting work, so you can't game them.
3. Update the curriculum track's status table.
4. Open a monthly retrospective stub for the period.

---

## Anti-drift disciplines

- **No reordering for excitement.** Reorder a module only if (a) interview funnel demands it, (b) bandwidth changes, (c) actual usage of the companion surfaces a real gap. Not because a new paper looked interesting.
- **No reading-driven learning.** If a module's deliverable is "I read X," it's not a real module. Every module ships something.
- **No claims without checks.** Anything claimed in a retrospective is BS-check fodder. Vague claims get caught by their own vagueness; the judge can't find a specific question to ask.
- **No "the AI did it" defense at BS-check time.** If you used AI assistance to build something (you almost certainly did), the BS-check still applies fully. "I built it but the AI wrote the code" is not a passing answer to "explain how this works." Either you understand it well enough to defend cold, or you didn't actually learn it.
- **No unverifiable scorecard fields.** Any field in a scorecard, rubric, or retrospective that the underlying build doesn't produce evidence for is a flag. Either change the spec to exercise that capability, or mark the field as research-not-build and don't let the learner pretend they know it from doing the work. (See "Spec design discipline" for the prevention pattern.)
- **No grinding past time-boxes.** When sunk cost is pulling for "one more attempt," that's the signal to stop and re-frame the outcome via "Friction is the signal" rather than push past the cap.
- **No state lies.** When work transitions, status tables get updated same session. Never let the documentation lie about state.

---

## Public / private posture

The framework + tool itself is best public. Each instance's contents are a personal choice: public makes a good portfolio asset for job-search; private is fine if the user isn't job-searching.

For instances that go public:

- **Code public, operational state local.** Even after publishing the companion code, runtime state (decision logs, BS-check results, hand-labels) stays local-only or gitignored.
- **Hybrid launch is usually right.** Private during early build; public when v1 ships with a controlled launch post; public from then on. Mid-build commits no longer read as "still learning" once there's an anchor narrative.
- **Decide at file creation, not at flip time.** When you create a working file or working directory, declare immediately whether it's intended for the public commit, stays local-only, or is gitignored runtime state. Reactive cleanup at flip time produces rushed polish or accidental over-sharing. Intentional preparation lets you write each file at the right level of polish for its audience from the start.
- **Public when it adds reader signal; private when writing-for-a-reader destroys the artifact's purpose.** Build-in-public has real signaling value for some artifacts: honest session logs, rough working scorecards, design rationale writeups. But living learning notes (parking-lot entries, personal retrospectives) lose their actual value if you sanitize them for an audience. Default isn't blanket public; default is *intentional choice* at creation.
- **The "who will read this?" check.** Before writing new content, ask the question and give it a conscious answer. The answer determines tone, polish level, and gitignore status. The decision is reversible (with cost) but should be conscious at creation, not deferred.
- **Session-output docs: trap or tool, depending on sequence.** When an AI session produces a wrap-up doc (extension notes, session summaries, "lessons learned" files) with polished answers to scorecard questions, the doc is a **trap** if used as a copy-paste source; it bypasses the learner's distillation and produces fake claims of understanding. The doc is a **tool** if used as a *foil after recall*: write your scorecard from memory first, then read the session output side-by-side and identify gaps. Retrieval-first + delayed comparison is a well-supported active-learning pattern; it produces measurably better encoding than either retrieval or reading alone.
- **Recall-gap discipline.** When the foil comparison surfaces something you missed in recall but the session output captured, log it as a parking-lot entry marked as a *recall gap* (distinct from a noticed-but-unclear gap). Both are deferred-encoding items but they signal different things: noticed-but-unclear means "I sensed it during the work"; recall-gap means "I lost it between then and now." Both are useful targets for revisit when the topic reappears.

---

## What this methodology assumes

- Adult learner with professional context and limited bandwidth (5-10 hrs/wk realistic).
- Self-directed: no instructor, no cohort.
- Learning AI specifically. The build-heavy emphasis depends on AI being the subject (real builds are tractable in single-digit hours per week). Other domains may need a different ratio.
- Has working familiarity with an AI development tool (Claude Code, Cursor, Aider, or similar) and can direct it. You do **not** need to be able to write Python from scratch. You **do** need to be able to (a) read what an AI writes, (b) ask sharp questions about it, (c) make architectural decisions yourself, and (d) verify the code does what you expected. Pure non-technical learners (someone who has never opened a code editor or run a script) will struggle; the methodology assumes you can drive an agentic dev environment with intent.

If those don't hold, the methodology doesn't apply cleanly.

---

## What this methodology is NOT

- Not a curriculum. The framework gives you the *structure* for a curriculum; you pick the modules.
- Not a course. There is no instructor and no grading. The BS-checker is your only quality gate.
- Not a credential. Nothing here results in a certificate. The artifact and the interview defensibility are the proof.
- Not a substitute for shipping. If you finish a module without a tangible artifact, you failed the module.
