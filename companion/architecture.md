# Learning Companion: Architecture

Most AI tutors check whether you understood what you read. This one checks whether you understood what you built. It captures your real build decisions as you make them, then later asks whether you can still defend them weeks after the fact, and grades your answer with an AI judge that has been calibrated against your own judgment.

This document walks through how the system is put together: its parts, how information moves between them, and the reasoning behind each major design choice. It is written to be readable without a coding background. Every technical term is named and explained in plain English the first time it appears.

> Scope. This is the v1 of the tool, a single-user program you run from the command line. There is no website and no graphical interface, and it leaves the production safety and monitoring layer for a later module. What it does show: coordinating several AI "agents," storing information so it survives and stays searchable, retrieving by meaning, and most important of all, an evaluation loop whose grader has been measured and shown to be trustworthy.

---

## 1. What it is

The companion runs alongside a real project. Three things happen through it.

1. **Log.** You describe a build decision in your own words. An AI reads your note and fills in a fixed form: the decision, the alternatives you weighed, your rationale, the tradeoffs, a few tags, and what you claim to have learned. Forcing the AI to answer on a fixed form instead of in free-flowing prose is called **structured output**, and the form itself is a **schema**. The filled-in decision is filed away in durable storage, and each rationale and each claimed learning becomes its own **checkable claim**.
2. **Query.** You pull back past decisions, either by an exact filter such as a tag or a date, or by meaning. Searching by meaning is called **semantic search**. It surfaces related past reasoning even when that reasoning shares none of the same words as your search, which a plain keyword search cannot do.
3. **Check.** The companion takes a claim that is due, asks a probing question pitched to how well you should know it by now, and grades your answer with a calibrated AI judge. Claims you defend well climb a **spaced-repetition** ladder, the same spacing idea behind flashcard apps, where each success pushes the next review further out. The long-interval pass is the real test: can you still defend this in an interview weeks later?

A fourth thing happens on its own. If you log a decision that contradicts something you decided earlier, the system notices the tension as soon as it appears and starts tracking it as its own claim, so you have to reconcile it over time instead of letting it sit.

What it runs on, in plain terms: Python is the language. **LangGraph** is the coordinator that decides which part of the system handles each request. Claude, Anthropic's AI, does the two language jobs, structuring your notes and judging your answers. Information lives in two complementary places: a single-file database called **SQLite** for fast lookups, and plain markdown text files for the full readable record. Search by meaning runs on a small open-source model on your own machine, with no key required and nothing leaving your computer.

---

## 2. System overview

```
                        ┌──────────────────────┐
        log / query     │     Orchestrator     │
        ───────────────▶│   the "traffic cop": │
                        │  decides which path  │
                        └───────────┬──────────┘
                      ┌─────────────┼─────────────┐
                      ▼             ▼             ▼
              ┌──────────────┐ ┌─────────┐ ┌──────────────┐
              │ Decision-Log │ │ Retrieve│ │  Search by   │
              │  structures  │ │ by tag/ │◀┤   meaning    │
              │  your note   │ │ date or │ │ (embeddings) │
              │              │ │ meaning │ │              │
              └──────┬───────┘ └────┬────┘ └──────┬───────┘
                     │              │             │
                     └──────────────┼─────────────┘
                                    ▼
                        ┌──────────────────────┐
                        │   Stored & searchable │
                        │  SQLite index +       │
                        │  markdown documents   │
                        └──────────┬───────────┘
                                   │ claims that are due
   check  ─────────────────────────▼──────────────────────────
                             ┌──────────────────────┐
                             │      BS-Checker      │
                             │  writes the question,│
                             │  grades the answer   │
                             │  (calibrated judge), │
                             │  schedules the next  │
                             │  review              │
                             └──────────────────────┘
```

The orchestrator looks at each request and sends it down the right path, the way a traffic cop directs an intersection. It is built with LangGraph, which lets you lay the system out as a flowchart with clearly defined routes. The traffic cop makes its choice with a simple rule rather than an AI call. When the path is obvious from what you typed, spending an AI call to decide it would waste money and time.

One boundary in the design is worth pointing out. Logging and querying are one-and-done: a request goes in, an answer comes straight back, nothing waits. A check is a conversation. It asks a question, waits for you to type an answer, grades it, and sometimes asks one follow-up. A back-and-forth conversation does not fit a one-and-done flowchart, so the check runs in the outer command-line layer that handles what you type, rather than inside the orchestration flowchart. The rule across the system is simple: predictable one-shot work goes in the flowchart, and anything that has to pause and wait for a person runs outside it.

---

## 3. The components

**The router.** The traffic cop from the overview. It reads one field, the mode you asked for, and points to the matching path. It is built once when the program starts. Because the same request always produces the same route, it is *deterministic*, the opposite of the AI's *probabilistic* behavior where the same prompt can yield different wordings. Routing is a fixed-rule job, so it gets a fixed rule.

**The Decision-Log agent.** This is the first place the AI does real work. It takes your free-text note and makes a single AI call that returns the filled-in form (the structured output from section 1). The instruction it runs under is strict: pull out what the user actually said, and invent nothing. The no-invention rule matters more here than it might seem. If the AI were allowed to fill in a plausible "claimed learning" you never stated, the system would later test you on something you never understood, and certify the AI's guess as your knowledge. The decision is then written to storage as both a readable document and an index entry, and its claims are registered for review.

**The store: where things live and stay searchable.** Each decision is saved in two forms. The full content goes into a markdown text file, the readable "book." A short summary row goes into the SQLite database, the "catalog card." Looking something up reads only the catalog cards, so search stays fast even as the library of decisions grows, and you open the full book only when you want the detail. Tags get their own separate table rather than being stuffed into one field, which is what lets you actually filter by a tag later. This separating of data into clean, queryable tables is called **normalization**. Two more tables sit alongside: one holds the **claims** waiting to be reviewed (the review queue), and one is an **append-only** history of every check ever run, a log that is only ever added to, never edited, so there is always a truthful audit trail.

**The search-by-meaning layer.** To search by meaning, the system turns each decision into an **embedding**, a list of numbers that captures the meaning of the text, so that similar meanings land near each other. A search turns your query into the same kind of numbers and returns the decisions whose numbers sit closest, measured by an angle between them called **cosine similarity**. The whole approach of fetching the most relevant stored material this way is known as **RAG** (retrieval-augmented generation). This layer does two jobs: it powers search-by-meaning over your decisions, and it finds the past claims most related to a new one, which is what the contradiction-catcher relies on.

**The BS-Checker: a question writer and a grader.** When a claim is due, one AI call writes a single probing question, grounded in the actual decision so it cannot drift off into invented territory, and pitched to the claim's current level. A second AI call, the grader, reads your answer and returns four things: a verdict (solid, partial, or wrong), a 1-to-5 score, its reasoning, and a teaching note that shows what a complete answer would have covered. This grader is an **LLM-as-judge**, a second AI whose only job is to evaluate the first one's subject, here your answers. It runs at **temperature 0**, the setting that makes an AI as repeatable as possible, so the same answer gets the same grade twice. Section 5 covers why that repeatability had to come before anything else.

**The scheduler.** Deciding when a claim comes back is a lookup-table job, so it uses fixed rules and no AI. A passed claim climbs the ladder: a same-session check, then two days later, then ten, then thirty, after which the interval stretches by about two and a half times on each further pass. A missed claim drops back to a short re-check. Predictable spacing means you can trust the timing and you never pay for an AI call to compute a date.

---

## 4. How information moves through it

**Logging a decision.** You type your note. The router sends it to the Decision-Log agent, which makes one AI call to structure it. The result is written to the corpus as a markdown document plus an index row plus its tags, and each rationale and claimed learning is registered as a claim due for a same-session check. The moment that write finishes, the contradiction-catcher runs (described below).

**Running a check.** You start a check. The system pulls the claim that has been due longest, asks the question writer for a question at that claim's level, and waits for your typed answer. The grader scores it. If the verdict is partial, the system asks one focused follow-up at the exact gap and then re-grades the combined answer with the same calibrated grader, so the grading bar does not move. The result is appended to the history log, the claim's current position is updated in place, and the scheduler sets the next review date. A solid answer advances the claim; a partial or wrong answer keeps it due.

**Catching a contradiction as it appears.** Each time you log a decision, the system takes its claims and, for each one, pulls the few most related past claims using search-by-meaning. It then asks a conservative checker whether the new claim and an older one genuinely conflict. Related is not the same as contradictory: two claims can sit near each other simply because they share a topic while fully agreeing, so this checker is built to stay quiet unless the conflict is real. When it does find one, it records that tension as its own claim, with an identifier built from the two source claims so the same conflict can never be logged twice. This runs at log time, when a contradiction is first introduced, rather than waiting for the older claim to come up for review someday. The contradiction is caught the moment it enters the record.

---

## 5. The decisions behind the design

These are the choices that shaped the system, with the reasoning behind each. They are the parts worth defending in a conversation about the architecture.

**A flowchart framework, with a rule-based router.** The system needed a way to coordinate several AI steps. The two main candidates were LangGraph, which models the work as an explicit flowchart whose state you control directly, and CrewAI, which gives AI agents more autonomy and tends to spend an AI call on each step. I chose LangGraph for the explicit control. Then I made the router itself a plain rule rather than an AI call. Picking the next step from a known mode is simple logic, and paying an AI to do it would add cost, delay, and randomness to a decision that should be instant and certain.

**Two kinds of memory, kept separate.** Early on there was a pull to wire in a "checkpointer," a feature that saves the in-progress state of a conversation so it can resume later. I held off, because it solves a different problem than the one in front of me. The thing that has to last here is the record of decisions, stored so it can be read back and searched. A checkpointer saves an opaque snapshot you cannot search by tag or date. So the corpus became the lasting memory, and the resumable conversation state was left out until something actually needed it. The principle I kept: do not store state you cannot yet read back.

**Tags in their own table.** When saving a decision's tags, the cheap path is to dump them into a single text field. I built a separate, structured tags table instead. The need, searching by tag, was certain and happening that same week, and the correct version cost only a few extra lines. That became my test throughout the build: build it right now only when the need is certain and the right version is cheap, and otherwise keep it simple behind a clean seam and revisit when a real need appears.

**Make the grader trustworthy before trusting it.** The grader produces convincing scores and sharp reasons even before anyone checks it, which is the trap. Convincing prose only shows the grader is internally consistent, not that it agrees with me. So I measured it before relying on it: I answered a spread of questions, graded my own answers, and compared the two. The first surprise was that the grader gave different scores across runs of the identical rubric, because the AI was sampling its output with some built-in randomness. At a small sample size, that swing was big enough to look like a real change in the rubric. The fix was to make the grader as repeatable as possible at temperature 0 first, and only then measure agreement. When an AI does the grading, remove its randomness before tuning anything, or you are measuring noise instead of your changes.

**The smaller model, when the test cannot tell them apart.** For search-by-meaning I compared three models. On my test set they tied: each one retrieved the right entries. A tie on a small, easy test does not mean the models are equal in general. It means the test cannot separate them. When the benefit cannot be measured, the smaller, simpler, cheaper option wins by default, and switching later is cheap if a real difference ever appears. I took the smallest of the three. A theoretical edge I cannot measure is not an edge I can spend.

**Catch contradictions where they are born.** The contradiction-catcher first ran when an old claim came up for review. It worked, but the timing was wrong. A contradiction enters the record the moment you log a decision that conflicts with a past one, so that is when it should be caught. Moving the check to log time catches the conflict as it appears, and it still covers every case, since each new decision is compared against the whole history. A feature can run correctly in the wrong place. The question to ask is where it logically belongs, then put it there.

---

## 6. Limits and what was left out

The credibility of a tool like this comes from being clear about what it does not do.

- **One user, one machine, command line only.** There is no website, no login, no support for multiple people. That is the right shape for a personal learning tool and would have to change for anything shared.
- **The grader is calibrated, but on a thin set.** Agreement was measured against twenty-two of my own labeled answers, graded by one person, me. It clears the bar that was set, and it reliably catches answers that fake understanding, but a larger set and a second labeler would make the measurement stronger. It also has a documented soft spot: it is occasionally too lenient on confidently wrong answers, though never lenient enough to wave one through.
- **No production safety layer.** There are no kill switches, no monitoring, no graceful handling of a sustained outage. When the AI provider went down mid-build, I added automatic retries, which cover brief blips but not a long outage. Real resilience is its own module later.
- **Search is exact but unindexed.** It compares your query against every stored entry directly. That is fast and exact at this size. At a much larger corpus it would need an approximate index, which trades a little accuracy for speed. Building that now would be solving a problem the tool does not yet have.

---

## 7. Stack and how to run it

The pieces, and what each is for:

| Piece | What it is | Why it's here |
|---|---|---|
| Python | The programming language | The whole tool is written in it |
| LangGraph | The flowchart coordinator | Lays out and runs the orchestrator |
| Claude (Anthropic) | The AI model | Structures notes, writes questions, grades answers |
| SQLite | A single-file database | Fast lookups over the index of decisions and claims |
| Markdown files | Plain text documents | The full, readable record of each decision |
| sentence-transformers | A small local AI model | Turns text into embeddings for search-by-meaning |

You drive it with three commands: `log` to record a decision in your own words, `query` to pull decisions back by tag, date, or meaning, and `check` to run a review session. The AI key lives in a single local file that never leaves your machine, and all of your own data, the decisions, the grading labels, and the review history, stays local as well. Only the code is meant to be public.

