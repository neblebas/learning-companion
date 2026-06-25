# Track B: Curriculum

A sequence of modules. Each one builds on the last where it should, and each is self-contained enough to defer or reorder without breaking the others. Every module produces a tangible artifact, though the artifact's shape varies by what the module is teaching: a working system, a separate operating mechanism, an audit document, a framework, a vendor map. Long-form writeups are produced when they document a real build (as in Module 1), not as a default deliverable per module.

## Module roadmap

| # | Module | Skill focus | Deliverable shape | Companion change | Status |
|---|---|---|---|---|---|
| 1 | Agentic Orchestration + Evals | Multi-agent orchestration, RAG basics, calibrated LLM-as-judge | A shipped multi-agent system + five build-documentation writeups (architecture, framework choice, calibration, RAG, integration) | v1: Orchestrator, Decision-Log, BS-Checker, RAG, calibrated judge, log-time cross-claim consistency | Complete |
| 2 | AI Foundations Consolidation + Risk Landscape | LLM mechanics, fine-tuning vs RAG vs prompt engineering, production deployment patterns at concept level, AI risk landscape | A one-page operator reference + BS-check questions registered for spaced retention + occasional public posts as topics surface naturally | None (v1.1 ingest command ships before this module begins; see "Companion development" below) | Planned |
| 3 | AI Governance: NIST AI RMF + EU AI Act | The two frameworks in real detail; bridges general compliance posture into AI-governance vocabulary | A governance audit document applying both frameworks to a real artifact (the companion) | None | Planned |
| 4 | Applied AI in Operations + ship one operating mechanism | How AI is actually deployed into business operations; human-in-the-loop patterns; closing the "designed-not-shipped" gap for ops roles | A shipped AI-augmented operating mechanism with kill switch, audit log, and adoption metrics, **separate from the companion**, for a real user base | None (separate artifact) | Planned |
| 5 | AI Adoption & Change Management | Champion programs, enablement, workshops, adoption-metrics frameworks | An adoption playbook with reusable templates (champion program, enablement plan, metrics) | None | Planned |
| 6 | AI Program / Product Operations | Use-case prioritization (value/feasibility/risk), launch-readiness, portfolio governance, AI-product success metrics | A reusable operator toolkit: prioritization rubric, launch-readiness checklist, success-metrics framework | None | Planned |
| 7 | Vendor Landscape + Cost Economics + Operational Tooling Literacy | Vendor ecosystem relevant to business-operator targets; token/inference economics; operational-tooling baseline (CRM, workflow automation, BI) | A vendor map (table), a cost model (spreadsheet), and demonstrated competency in core operational tooling | None | Planned |

## Companion development

The companion is the centerpiece artifact, not a substrate that every module grows. v1 shipped in Module 1. **v1.1** ships as a small, focused iteration before Module 2 begins: an `ingest` command that extracts and registers claim-shaped statements from external transcripts (session exports, conversation logs) so the BS-Checker can probe curriculum learning the same way it probes build decisions. Beyond v1.1, further companion iteration is real-use driven rather than pre-scheduled. The original "one new component per module" trajectory was redirected after Module 1 in favor of operator-shaped deliverables that match the target role set.

The companion remains the verification mechanism throughout the curriculum: claims registered via `ingest` flow into the existing spaced-repetition + calibrated-judge loop. Modules 2-7 do not produce companion components, but they do produce companion-tested claims.

## Deliverable shape: why not a writeup per module

Module 1 produced five long-form writeups because Module 1 was a substantial build and the writeups document the build. For modules where the work is primarily applied learning or operating-skill development, the natural deliverable is an operator-shaped artifact (an audit document, a vendor map, a cost model, an adoption playbook, a prioritization rubric), not a synthesizing essay manufactured to give the module "something shipped." Operators ship templates, audits, frameworks, decisions, and conversations. The deliverable column above reflects that. Long-form public content (LinkedIn long-form, blog posts) is produced when there is something substantive to say, not on a one-per-module schedule.

## Sequencing rationale

**Why Module 1 is Agentic Orchestration + Evals.** It produces the centerpiece artifact early. The companion's calibrated LLM-as-judge becomes the verification mechanism for every subsequent module. Evaluation calibration is among the scarcest skills in the operator-with-AI-fluency profile and benefits from being grounded in a real artifact rather than discussed abstractly.

**Why foundations consolidation is Module 2.** The build-heavy Module 1 produces substantial implicit foundations (RAG mechanics, evaluation calibration, agent orchestration, structured output). Module 2 makes them explicit and fills the remaining gaps (LLM mechanics, deployment patterns, fine-tuning vs RAG vs prompt engineering, the risk landscape) before the applied modules build on them.

**Why governance precedes the applied operating-mechanism module.** Module 3 (Governance) establishes the vocabulary and frameworks; Module 4 ships an operating mechanism that can be designed with governance baked in from the start rather than retrofitted.

**Why adoption follows applied + artifact.** Adoption is the discipline of getting something used. It needs something shipped to be adopted. Module 4's operating mechanism gives Module 5 a real target rather than a hypothetical one.

**Why program/product ops follows adoption.** Use-case prioritization, launch-readiness, and success-metrics formalization are easier to design after one applied build has informally exercised them. Module 6 systematizes what Module 4 did organically.

**Why vendor + cost + tooling is last.** It is the most pragmatic operating-literacy module and the least dependent on the build sequence. Placing it last keeps the build-heavy and governance-heavy modules in the highest-energy window and uses the later, lower-energy time for the most reading-and-doing literacy work.

## Module activation protocol

When a module moves from planned to active:

1. Create its spec from the module template.
2. Lock its BS-check questions before any work starts, so they cannot be gamed.
3. Update the status in this file and in the instance README.
4. Update the companion's spec if the module changes a companion capability (most modules will not).
5. Open a retrospective for the period.

## When to reorder

Reorder a module only when there is a real reason:

- An artifact lands faster than planned and frees time.
- Real use of the companion surfaces a gap the current order does not address.
- A live opportunity (an interview, a contracting offer, a domain-specific application) changes the priority. A regulated-industry interview makes the governance module worth pulling forward; an operations-tooling-heavy role makes Module 7 more urgent.

Do not reorder because a new paper, framework, or tool looks exciting. That is the drift trap.
