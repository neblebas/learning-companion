# Worked Example: building the Learning Companion

This directory is a filled-in example of the framework described in [`../methodology.md`](../methodology.md). It shows how I applied that method to design, build, and evaluate a real artifact: the multi-agent Learning Companion in [`../companion/`](../companion/).

The framework is the general method. This is one run of it, with the curriculum, the build decisions, and the evaluation work left visible, so the method can be seen in practice rather than only described.

## Who this run is for

I am a 14-year operator with an MBA and prior design-stage AI work, targeting operator-with-AI-fluency roles at business-buyer remote-first companies: operations leadership, strategy and business operations, customer success and customer ops, program and project management, chief of staff / strategy and operations, and adjacent AI-program and AI-implementation lanes. Everything here is calibrated to that target. The goal is the fluency to design, deploy, govern, and drive adoption of AI in business operations: to direct AI builds, make and defend architectural decisions, and judge whether a system actually works. It is not the depth of a machine-learning engineer or researcher, and it does not pretend to be.

## What's here

| Path | What it is |
|---|---|
| [`tracks/B-curriculum.md`](tracks/B-curriculum.md) | The curriculum: a sequence of monthly modules, each one shipping a working artifact |
| [`tracks/C-portfolio.md`](tracks/C-portfolio.md) | The portfolio ledger: what has actually shipped |
| [`modules/01-agentic-orchestration-and-evals.md`](modules/01-agentic-orchestration-and-evals.md) | The module spec that drove the companion's v1 build |

The artifact this module produced lives one level up in [`../companion/`](../companion/), alongside its architecture, framework-choice, calibration, and retrieval writeups.

## How the method shows up here

Three operating rules run through every module:

- **Build over read.** Every module ships a working artifact, and reading serves the build rather than standing in for it.
- **Ship over consume.** A small thing in real use beats a large thing sitting in notes.
- **Check understanding, then re-check it over time.** Every claimed learning is probed when it is first made, then again at spaced intervals, so it has to survive past the moment it was fresh.

The companion's module spec shows these in action. The framework decision was made by building two options and comparing them. The judge that grades my own understanding was calibrated against my labels before it was trusted. And the design decisions were captured as they were made, so they could be defended cold later.
