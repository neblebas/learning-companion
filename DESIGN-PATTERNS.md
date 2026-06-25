# Design Patterns: Tactical Decision Tests

Reference file. Specific decision tests and design questions you apply at decision points. Each pattern includes the test, when to apply, the failure modes it prevents, and a worked example from a real session.

For the principle / orientation layer (motivation alignment, friction-is-signal, BS-check tiers, vocabulary calibration, etc.) see `methodology.md`. For the directing discipline rules for AI-assisted sessions see `DISCIPLINE-REFERENCE.md`.

Patterns are **decision-grade tools** rather than principles. They tell you *what to ask* at a fork in the road, not *what to believe*.

---

## 1. Build-right-vs-defer: the three-condition test

**The test:** When deciding whether to build a piece of infrastructure properly vs. defer it (or build a simpler version):

1. **Is the need certain and exercised now?**
   - **No** → **defer or simplify.** Don't build speculative, unverifiable infrastructure. You can't tell if it's right until something exercises it.
   - **Yes** → continue to question 2.
2. **Is the correct version cheap (small marginal cost over the simpler version)?**
   - **Yes** → **build it right the first time.** Cheap + certain need = no reason to defer.
   - **No** → judgment call. Often: build the simpler version with a clean interface, plan to revisit.
3. **Either way: keep it behind a stable interface** so the choice stays cheap to reverse.

### Sharpening for scale/purpose-dependent choices (added Week 5)

"Build it right the first time" assumes one fixed right answer exists *now*. When the right answer depends on **scale** or **purpose**, build the tool that fits *current* scale/purpose behind a stable interface. The later swap isn't a shortcut fix; it's an adaptation to a new condition.

| Type | Example | Rule |
|---|---|---|
| **Purpose-dependent** | Whole-entry chunking for "find decisions"; per-claim chunking for "find claims" | Same machinery, different unit: build the unit that matches the *current* purpose |
| **Scale-dependent** | Brute-force exact search at small scale; ANN (approximate) at large scale | Brute-force is *worse* at large scale and *better* at small scale, so it is not the same answer at different sizes |
| **Doesn't-exist-yet** | Chunk overlap only matters once entries are long enough to split | Building it now = unverifiable infrastructure |

### Two failure modes this prevents

- **Premature elaboration:** building sophisticated infrastructure for needs that aren't yet certain. *"I built a full checkpointer before knowing how I'd query it."*
- **False economy:** simplifying things certain to be exercised and cheap to do correctly. *"I stored tags as a JSON blob to save 4 lines; now I can't query by tag without rewriting."*

The two failures look like opposites ("build less" vs. "build more"), but they're both signaled by the same questions. Different answers from the same rule.

### Worked examples

- **Module 1 Week 2, deferred:** session-memory checkpointer. Need uncertain. Rule #1 → defer.
- **Module 1 Week 2, built right:** normalized `decision_tags` table instead of JSON blob. Need certain + cheap. Rule #2 → build right.
- **Module 1 Week 5, deferred:** ANN search index, chunk overlap, per-claim chunking. Need uncertain *at current scale/purpose*. Rule applied to scale/purpose-dependent choices.

### Interactions

- Complements **Spec design discipline** (methodology): specs producing no buildable evidence are a "build speculative" failure mode.
- Complements **Friction is the signal** (methodology): if you build something whose need is uncertain and it produces friction without signal, that's a flag the deferral question wasn't asked.
- Complements **Pattern 2 (Verifiable-benefit threshold):** both default toward simpler when the cost-benefit can't be verified.

---

## 2. Verifiable-benefit threshold: when the eval can't separate, smaller wins

**The test:** When choosing between technical options (frameworks, models, embeddings, vendors, architectural approaches) and your evaluation can't measurably separate them on quality:

1. Is the eval **saturated** (too easy to discriminate options) or **noisy** at your sample size?
2. If yes → **default to the smaller, simpler, cheaper, more reversible option.**
3. Verify the choice is **reversible at low cost** so a real signal later can flip it.

The principle: **a theoretical advantage you cannot measure is not an advantage you can spend.** When the test can't pick a winner, simplicity wins by default because every other dimension (cost, latency, maintenance, debuggability) favors it.

### The failure mode this prevents

**Speculative sophistication-bias.** Picking the option with the better theoretical profile (more parameters, more features, higher leaderboard rank) when your actual eval shows it ties with simpler options at your real task. The sophistication is purchased; the benefit is not.

### Worked example (Module 1 Week 5)

Compared three embedding models for the companion's RAG layer:

| Model | Size | P@1 | Recall@3 |
|---|---|---|---|
| all-MiniLM-L6-v2 | 22M | 7/8 | 8/8 |
| bge-small-en-v1.5 | 33M | 7/8 | 8/8 |
| bge-base-en-v1.5 | 109M | 7/8 | 8/8 |

All three tied. The eval was saturated at 8 short entries. Decision: **MiniLM**, the smallest and simplest, with no query-prefix quirk. The "bigger is better" instinct would have picked bge-base; the threshold rejected it as 2× size for zero measured gain.

Reversibility check: re-embedding takes seconds. If the corpus grows and the eval can separate models, swap is cheap.

### When this pattern does NOT apply

If the eval *does* show measurable, repeatable differences, pick the winner. That's normal evaluation. The pattern fires specifically when ties or near-ties occur in evals too small or too easy to be diagnostic.

### Interactions

- Complements **Pattern 1 (Build-right-vs-defer):** both default toward simpler when the benefit case is unverified.
- Related to **Spec design discipline** (methodology): an eval that can't separate options is the spec-design analog of a scorecard field with no buildable evidence. If the test can't measure the thing, the test is wrong rather than the options.

---

## 3. Where does this logically fire? The placement test

**The test:** When designing a feature, after confirming it *works*, ask: *"Where in the system flow does this logically belong / fire?"*, not just *"can we make it work where I put it?"*

A feature that functions in placement X may be more valuable, more correct, or more efficient in placement Y. A working placement isn't always the right one.

### When to apply

After implementation, before considering the feature complete:

1. Identify the events / states in the system flow where the feature *could* fire.
2. Ask: which event / state is the **logical origin** of the condition this feature addresses?
3. Confirm the current placement matches the logical origin. If not, refactor.

### The failure mode this prevents

**Feature-functions-where-built bias.** Implementing a feature at the point in code where it was easiest to add, rather than at the point in flow where its trigger condition actually arises. The feature works, the test passes, the design is silently wrong.

### Worked example (Module 1 Week 6)

The BS-Checker's cross-claim consistency feature: when you log a decision, the system surfaces tension with related past decisions.

- **Initial implementation:** the feature fired at *review time* (when a claim came up for spaced-repetition check). Functioned correctly.
- **The placement question:** *"What is the logical place for tension to fire?"*
- **The answer:** **log time.** Tension *surfaces* the moment you record a decision that contradicts a past one; that's where the condition arises. Log-time catches the contradiction instantly. Review-time would leave fresh contradictions lurking until the old claim next resurfaced.
- **Sufficiency check:** log-time is also sufficient, because the newer claim is always compared against all older ones, so every contradiction is caught in both directions as it arises.
- **Refactor:** moved detection to log-time; removed the review-time augmentation as redundant.

### Why this is more than "code review"

Code review checks: does it work, does it match the spec, are there bugs.

This pattern checks: is the *spec itself* right, did we put the feature at the right point in the flow.

The placement question is a **design** check rather than an implementation check. It catches issues that pass every implementation review because the implementation is fine; the design is silently wrong.

### Interactions

- Complements **Spec design discipline** (methodology): a spec that gets the placement wrong produces working-but-wrong implementations.
- Complements **Friction is the signal** (methodology): if a feature in placement X requires special handling, state, or triggers that wouldn't be needed in placement Y, that friction is signal of misplacement.

---

## 4. Surface security / trust / privacy decisions BEFORE acting

**The rule:** Any choice that changes the trust, security, or privacy posture gets surfaced for explicit user approval **before** it happens, not narrated after.

### Why this matters specifically for AI-assisted work

The AI assistant sits between the user and raw tool output. Warnings, security signals, and trust-posture-changing decisions only reach the user if the assistant surfaces them; the user cannot independently see what scrolled past in a command's output. This makes the assistant a **single point of failure for security visibility** unless it actively surfaces these decisions.

### What counts as a trust / security / privacy decision

- Enabling remote-code execution (e.g., `trust_remote_code=True`, executing downloaded code)
- Installing unvetted or executable-code dependencies
- Sending operational data to an external service (API calls with private corpus, telemetry)
- Bypassing TLS / certificate verification
- Granting elevated permissions
- Any supply-chain decision (which model, which library, which fork)
- Storing credentials, tokens, or keys in non-standard locations

### The test

Before executing any command or writing any code that touches one of the above, **stop and surface the decision** with:

- What you're about to do
- Why
- What the trust / security / privacy implications are
- The default alternatives that *don't* have those implications
- Request explicit user approval before proceeding

Narration *after* the fact is insufficient. By then the action has happened: the cache contains the executed code, the data has been sent, the dependency is installed.

### The failure mode this prevents

**Silent trust escalation.** The assistant takes an action with security implications, the user never sees the warning that fired in raw output, and the trust posture has shifted without user awareness. Even if the assistant later mentions the action, the user can't undo the cache state, the downloaded code, or the data already sent.

### Worked example (Module 1 Week 5)

During embedding-model comparison, the assistant set `trust_remote_code=True` inline when loading `gte-base`, allowing the model to download and execute custom Python code on the user's machine. The action worked; the model loaded; no error to the user.

The user caught it: *"there was a `trust_remote_code` warning that I didn't see, what got executed?"*

Real process gap. Fix: switched to `bge-base` (no remote code), scrubbed the executed code from cache. Final stack runs zero third-party code.

The pattern going forward: any supply-chain decision (model loading, library install, dependency choice) gets flagged *before* the action, with the trust / security implication named explicitly. The user makes the call; the assistant does not delegate it to themselves.

### Interactions

- Complements **Building with AI assistance** (methodology): the user directs; the AI implements. Security decisions are part of what gets *directed*, not delegated.
- Distinct from `[measure]` vs. `[probe]`: this is about giving the learner the information they need to make a decision the assistant is not authorized to make on their behalf, rather than about probing learner understanding.

---

## When to use this file

- You're at a decision point and want a quick check on which pattern applies.
- You're writing a spec and want to verify the decisions it asks the learner to make are well-framed.
- You're an AI assistant reading this for inheritance; these are the tactical tools the methodology principles produce in practice.

## What this file is NOT

- A complete catalog. Each pattern was derived from a real session moment of friction or insight. New ones get added as they surface.
- A substitute for `methodology.md`. The patterns sit *on top of* the methodology principles; they don't replace them.
- A set of rules to apply mechanically. Each pattern is a **question** that surfaces a decision; the right answer still depends on context.

## Adding new patterns

New patterns get added when a session produces a tactical decision insight that:
- Generalizes beyond the specific session (universally applicable, not just to this instance)
- Names a question or test that wasn't obvious before
- Has a worked example demonstrating where it fires and what it catches

Pattern format: name → test → when to apply → failure mode prevented → worked example → interactions.
