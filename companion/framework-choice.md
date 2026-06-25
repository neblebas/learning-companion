# Framework Choice: why LangGraph

**Decision:** LangGraph, over CrewAI, for the companion's orchestration.

I needed a way to coordinate several AI steps over shared, lasting state: a router, a decision-logger, a retrieval layer, and a calibrated judge. Before committing, I built the same minimal workflow by hand in two frameworks, researched the rest of the field, and chose on what the build actually showed rather than on reputation.

## How I compared

I implemented a small multi-agent workflow twice, once in CrewAI and once in LangGraph, including a state-and-persistence extension that forced each framework to reveal how it natively holds and saves state. Two more on the shortlist, the Anthropic Agent SDK and Pydantic AI, I evaluated through their documentation rather than a full build. A few others I ruled out for clear reasons, listed at the end.

I stopped at two hands-on builds rather than four. After CrewAI and LangGraph, the core contrast was already clear: role-based agents that lean on the model for each step, against an explicit graph with state I control directly. A third and fourth build would have added detail without changing that contrast, so the better use of the time was to capture the decision and start building the actual tool. Grinding on for marginal data points is the kind of diminishing return worth walking away from.

## What the two builds showed

| What mattered | CrewAI | LangGraph |
|---|---|---|
| Control model | Role-based agents; leans on an AI call for each step | Explicit flowchart with state I control directly |
| Non-AI steps | Still tend to run through the model | Run as plain code, no wasted AI call |
| State and persistence | Built-in memory system | Explicit state schema, with a checkpointer that saves and resumes it |
| Vendor neutrality | Defaulted to OpenAI for its memory and embeddings, and failed silently without an OpenAI key | Model-agnostic, with no default to override |

Two findings stood out.

**The wasted-call problem.** CrewAI routes work through an AI call even when the step is plain logic, like picking the next path from a known mode. That is slower, costs money, and adds randomness to decisions that should be instant and certain. LangGraph let me run those steps as ordinary code and spend an AI call only where judgment was genuinely needed.

**The silent vendor default.** CrewAI's memory system quietly defaulted to OpenAI for its embeddings. Without an OpenAI key it did not raise an error, it degraded silently, which is the worst way for a dependency to fail. It showed that "vendor-agnostic" has boundaries worth checking before you rely on the claim. LangGraph had no such default to trip over.

## The decision

LangGraph, for two reasons that held up across the build:

1. Explicit state with a checkpointer for persistence was more robust, and easier to reason about, than an opaque built-in memory.
2. Steps that need no AI call run as plain functions, so the system never burns a call, or invites randomness, on simple logic.

CrewAI was the runner-up. Its role-based model is quicker to stand up when every step genuinely is an AI task, but spending an AI call on everything was a hard limit for this tool, and its building blocks looked thin for the complexity I expected to add later.

## What would make me reconsider

If the orchestration stayed simple and the LangGraph setup ever felt heavier than the job deserved. CrewAI is easier to spin up when the tasks are uncomplicated and every step is an AI step. If the companion never grew past that, the explicit-graph overhead is the thing I would question.

## Considered but not implemented

- **Anthropic Agent SDK:** a vendor SDK, light but locked to Claude. Evaluated through docs.
- **Pydantic AI:** type-safe and Python-native. Evaluated through docs.
- **OpenAI Agents SDK:** locked to OpenAI, and the older Assistants API it replaced is being retired.
- **Mastra:** TypeScript only, out of scope for a Python build.
- **Smolagents and Google ADK:** left out to keep the comparison focused.

Naming these, with a reason for each, is part of defending the choice. It was made against a known field.
