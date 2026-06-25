# Discipline Reference: AI-Assisted Build Sessions

Reference file. The five discipline rules for directing AI in build sessions, with each rule's purpose. Look here if you go hazy mid-prompt. **The intent is NOT to bypass writing the prompt from memory:** that's where the directing skill develops. The intent is a safety net when memory gaps slow you down.

For the underlying principles in prose, see `methodology.md` "Building with AI assistance." For tactical decision tests applied during the build itself (build-right-vs-defer, verifiable-benefit threshold, where-does-it-fire, surface-security-before-acting), see `DESIGN-PATTERNS.md` (sibling reference file).

---

## The five rules

### 1. Propose plan before any code. I review first.

**Purpose:** force architectural reasoning into the open where you can see it and push back. Without this, the AI writes finished code while you're still reading requirements, and you become a reviewer of finished work instead of a director.

### 2. One component at a time. Show, stop, I respond.

**Purpose:** prevent the AI from writing many files in one shot. Catches issues at file boundaries instead of after a massive diff. Forces the AI to wait for your input between units of work.

### 3. New primitive → STOP and explain in plain English BEFORE first use.

**Purpose:** every new framework concept (StateGraph, TypedDict, Node, Checkpointer, etc.) gets explained before being instantiated. You don't write `class GraphState(TypedDict)` without first hearing what TypedDict is, why the framework uses it, and what alternatives exist.

**Sharpening from the LangGraph debrief:** this includes **execution methods** (`.invoke()`, `.stream()`, `.kickoff()`, etc.) that the AI might bundle into walkthroughs instead of treating as first-class primitives. If the AI mentions `X.method()` in passing, it owes you a stop-and-explain on it first.

**Sharpening from the Week 3 BS-Checker debrief:** **design-discussion is NOT primitive-explanation.** During design-heavy phases (component scoping, architectural debate, judge rubric design), the AI may *discuss* what a primitive does as part of architectural conversation without ever *naming and defining* it at the right altitude. Both are required: design talk shapes the choice; primitive-explanation gives the learner the vocabulary to defend it. If a session has gone several components without explicit *"this is a [primitive name], it [plain English what + why]"* moments, the discipline has silently drifted. Recovery: a retroactive primitives ledger ("here's what got introduced but not formally named, with each one explained now"), then lead with primitives for every subsequent component.

### 4. After each file is written, ask me to summarize what it does in my own words before continuing.

**Purpose:** forces YOU to articulate understanding before moving on. This is the spot-tier BS-check applied to code. If you stumble summarizing the file, that's a flag; revisit before the AI keeps building.

> **Frequently forgotten, flag for memory:** This rule is the easiest to forget because it requires *your* action, not the AI's. The other four describe AI behavior; this one describes a learner action that fires after the AI completes a file. If you're going to drop one rule from memory, statistically it's this one.

### 5. ~30 line check-in limit.

**Purpose:** backstop for when other discipline pieces are forgotten. Sets a hard ceiling on how much code can be written without you in the loop. Even if rules 1-4 slip, you can't be more than ~30 lines behind.

---

## The five-section prompt structure

Reference for the overall shape of a directing prompt:

1. **Files to read:** the specific files the AI should read before any work
2. **Config:** environment setup (the model, virtual environment, secret location, and any tracing or telemetry settings; assembled per session)
3. **Discipline:** the five rules above (memorize and write from memory; this file is the safety net)
4. **Time-box:** context-dependent per `methodology.md` "Time-boxing":
   - **Evaluation work:** hard cap with bail behavior, friction-as-signal fires
   - **Production work:** tiered. Per-session (1-2hr) = pacing; per-week budget = scope check; per-module budget = hard wall
5. **Kickoff:** "Propose plan first. No code yet."

---

## When to consult this file

- You're mid-prompt and can't recall a rule
- You finish a session and want to verify you applied all five
- You want to remind yourself of the sharpening on rule 3
- You suspect you dropped rule 4 (the frequently-forgotten one)

The act of writing the prompt from memory IS the skill-building exercise. Consulting this file after a memory gap doesn't undo that; the exercise is *"write what you can recall, look up gaps."* That's the recall-first pattern from the methodology applied to your directing skill.

---

## What this file is NOT

- A copy-paste template for the full prompt. The discipline block is the only standardized part; the rest (files, config, time-box, kickoff context) varies per session and you assemble it.
- A substitute for the skill of remembering the rules.
- A canonical prompt. Your actual prompt should be adapted to the specific session's work, not lifted verbatim.
