# AI Learning Framework + Companion

A methodology and a tool for self-directed adult professional AI learning. Build over read. Ship over consume. Check understanding, then re-check it over time.

The intellectual core is [`methodology.md`](methodology.md), the principles every instance of the framework should respect. Two tactical reference files sit alongside it: [`DESIGN-PATTERNS.md`](DESIGN-PATTERNS.md) for decision tests applied during builds (build-right-vs-defer, verifiable-benefit threshold, where-does-it-fire, surface-security-before-acting), and [`DISCIPLINE-REFERENCE.md`](DISCIPLINE-REFERENCE.md) for the rules of directing AI in build sessions.

---

## What's in this repo

Three things, each usable on its own:

- **[`companion/`](companion/):** a multi-agent build-to-learn companion tool. It captures your build decisions, runs spaced-repetition BS-checks on what you claim to have learned, and is iterated as real use surfaces what to improve.
- **[`framework/`](framework/):** universal templates for applying the methodology to your own learning, covering the curriculum track, portfolio track, module spec, case study, and retrospective.
- **[`instance/`](instance/):** a filled-in example, showing how one operator (a 14-year operator with an MBA, targeting operator-with-AI-fluency roles at business-buyer companies) applied the framework to build the companion.

---

## Three audiences

**1. You want the tool.** Head to [`companion/`](companion/). It is a multi-agent system you can run for your own learning, and it works on its own, independent of the methodology. The [architecture writeup](companion/architecture.md) explains how it is built.

**2. You want to apply the methodology.** Read [`methodology.md`](methodology.md) first. Then either copy the templates from [`framework/`](framework/) into your own working directory, or fork this repo and fill in your own instance. The companion is optional but recommended once you have a few modules going.

**3. You're a hiring manager browsing.** [`instance/`](instance/) shows the framework applied to build a real system. For the engineering and evaluation work, read the [companion architecture](companion/architecture.md) and the [judge-calibration writeup](companion/judge-calibration.md). For the decision rationale, the [framework-choice writeup](companion/framework-choice.md). For how the whole thing was planned and executed, [`instance/`](instance/).

---

## Quick start

| If you want to | Start at |
|---|---|
| Run the companion as a tool | [`companion/`](companion/) (see [`spec-v1.md`](companion/spec-v1.md) and [`architecture.md`](companion/architecture.md)) |
| Apply the methodology to yourself | [`methodology.md`](methodology.md), then [`framework/instance-README.template.md`](framework/instance-README.template.md) |
| See one instance in action | [`instance/README.md`](instance/README.md) |

---

## Layout

```
ai-learning/
├── README.md                  ← this file
├── methodology.md             ← universal principles
├── DESIGN-PATTERNS.md         ← tactical decision tests
├── DISCIPLINE-REFERENCE.md    ← AI-directing rules for build sessions
├── companion/                 ← the tool: code + spec + writeups
│   ├── app/                   ← the multi-agent system
│   ├── spec-v1.md
│   ├── architecture.md
│   ├── framework-choice.md
│   ├── judge-calibration.md
│   ├── rag-notes.md
│   └── v1-integration-notes.md
├── framework/                 ← templates for adopters
└── instance/                  ← worked example: the framework applied
    ├── README.md
    ├── tracks/
    └── modules/
```

---

## Status

- **Methodology and framework templates:** v1, structurally complete.
- **Companion:** v1 shipped. Orchestrator, Decision-Log, and BS-Checker agents over a persistent store, a calibrated LLM-as-judge, and semantic retrieval.
- **Reference instance:** Module 1 complete; Module 2 next.

---

## License

MIT for the framework and the companion. Instance contents follow each user's choice; this reference instance is MIT.

---

## Contributing / forking

If you fork to apply the framework to yourself, rename `instance/` to your own (or move it to a separate repo) and start from [`framework/instance-README.template.md`](framework/instance-README.template.md). Pull requests to the framework or companion are welcome; instance-specific changes belong in your fork.
