# Semantic Retrieval: choices and evaluation

**Status:** Built and wired into the companion.
**What it does:** searches my decision log by meaning rather than exact keywords, exposed as `query --find "<natural language>"`. It closes an earlier gap where an exact-tag search for `state` missed related entries that happened to be tagged `state-management`.

---

## Decisions

### Local open-source embeddings

I ruled out the hosted options (OpenAI, Voyage, Cohere). Each one needs an API key and, more to the point, ships my private corpus off my machine. A local open-source model needs no key, costs nothing to run or to compare against rivals, keeps my data on the machine, and by 2026 benchmarks now matches OpenAI's `text-embedding-3-small` on ordinary retrieval. The stack is `sentence-transformers` running on the CPU.

### The model, chosen by a small evaluation

I compared three local models on a hand-built query set:

| Model | Size / dims | P@1 | Recall@3 |
|---|---|---|---|
| all-MiniLM-L6-v2 | 22M / 384 | 7/8 | 8/8 |
| bge-small-en-v1.5 | 33M / 384 | 7/8 | 8/8 |
| bge-base-en-v1.5 | 109M / 768 | 7/8 | 8/8 |

They tied. Every model retrieved the right entries. That is a sign the test is saturated: with eight short, distinct entries it is too easy to separate the models, so it can confirm all three are good enough but cannot crown a quality winner. (The single query that missed the top rank missed it for all three, which is a property of that query, not of the models.) So the choice falls to secondary factors. MiniLM is the smallest and fastest, and it needs no special query prefix, where the bge models do. I ruled out bge-base because it costs twice the vector size for no measured gain. Nothing here is locked in: re-embedding the whole corpus takes seconds, so the plan is to re-run this evaluation as the corpus grows and move to a stronger model only if retrieval quality measurably slips.

### One vector per entry

Each decision is embedded whole, as a single vector over its full text. The entries are short and carry a single idea, so the blended-meaning problem that hurts large chunks barely applies. At a hundred times the scale, with longer documents covering several topics, three things would change: chunk smaller so each vector stays focused, add overlap between chunks so meaning is not cut off at a boundary, and replace the brute-force search with a vector index. None of those earns its place at this size.

### Brute-force exact comparison

At anywhere from eight to a few dozen vectors, comparing the query against all of them is instant and exact. A vector index would be approximate, meaning it can miss the true best match, and it would be slower to build than a full scan is to run, with an extra dependency to maintain on top. Brute-force is the right tool at small scale, and an approximate index becomes the right tool at large scale. The vectors are normalized to unit length, which turns the meaning-distance into a single fast matrix multiply.

## How I evaluated it

I hand-built a query-to-target set, one query per logged decision, and measured two things: Precision@1 (the right entry ranked first) and Recall@3 (the right entry somewhere in the top three). Honest scope: at about eight entries this illustrates the method rather than standing as a robust benchmark. The harness is reusable as the corpus grows.

## A security note

One early candidate, `gte-base`, required a `trust_remote_code` setting, which means it downloads and runs custom model code on my machine. That is a supply-chain trust decision, not a plain download, so I swapped it for a model with a standard architecture and no remote code, and scrubbed the cached code. The model I shipped runs no third-party code.

## Limits and future work

- The evaluation is small and saturated. Re-run it and re-pick the model as the corpus grows.
- Whole-entry chunking for now. Per-claim retrieval, which checks a new claim against my history, uses the same embedding machinery and came next.
- Brute-force search for now. Move to a vector index only at real scale.
