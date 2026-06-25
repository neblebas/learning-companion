# Judge Calibration: the BS-Checker's LLM-as-judge

**Status:** Calibrated and in use.
**Judge under test:** Claude Sonnet (`claude-sonnet-4-6`), tier-aware rubric, temperature 0.
**Headline result:** 82% exact agreement and a Cohen's κ of 0.73 over the full set; 88% and κ of 0.81 on the answers I wrote myself; 7 of 7 seeded bad answers caught. Gate met.

> The hand-labeled question-and-answer pairs behind these numbers stay on my machine (gitignored). This document is the method and the results.

---

## Why calibrate at all

The judge decides whether I genuinely understood a decision I made. If it is wrong, the tool is worse than having no tool, because it would certify understanding I do not actually have. So before I trust its scores, I measure them against my own judgment. The risky case is a judge that produces plausible-looking scores without ever being checked, because plausibility invites trust it has not earned. Reading its written reasons only shows that the judge is internally consistent. It says nothing about whether the judge agrees with me.

## What the judge produces

For each answer the judge returns five things: a verdict (solid, partial, or wrong), a score from 1 to 5, a plain-English reason, a flag for when the question itself was ambiguous, and a teaching note showing what a complete answer would have covered. The rigor is tier-aware. The standard to earn "solid" climbs from a same-session spot check ("explain your reasoning") up to the long interval ("defensible cold in an interview"). The verdict is what drives behavior: solid advances a claim, while partial and wrong leave it due.

## Method

- Ground truth is my own labels. Calibration measures whether the judge's verdict matches my verdict on the *same* answer. It does not measure whether the answer was correct. That distinction matters, because it means I need a spread of answer quality, so my partial and wrong answers are useful data rather than something that skews the result.
- The primary metric is the three-way verdict. It drives behavior, and it is easier to self-label reliably than a fine 1-to-5 score.
- Blind labeling. I answered each question and graded my own answer before seeing any judge output, so the judge could not anchor me. The judge graded without seeing my labels.
- The calibration set held 22 pairs: 8 genuine ones (my own cold answers to questions about real build decisions, self-graded), 7 crafted answers of known quality to anchor the range, and 7 seeds. A seed is a confident-but-wrong answer that cites plausible but false reasons such as latency, security, or cost. The pairs spanned the spot, medium, and long tiers.
- Agreement was measured two ways: percent exact (identical verdicts) and Cohen's κ, which corrects agreement for what chance alone would produce.
- The gate to declare the judge trustworthy: at least 80% exact or κ of at least 0.6, and every seed caught.

## Results

| Subset | n | Exact | Cohen's κ |
|---|---|---|---|
| All pairs | 22 | 82% | 0.73 |
| Genuine (answers I wrote) | 8 | 88% | 0.81 |
| Seeds caught (not passed as solid) | 7 | 7/7 | n/a |

Gate met on both the exact-agreement and the κ criteria, with all seeds caught.

## The finding that mattered most: a judge has to be repeatable

The biggest lesson here was not a better rubric. It was discovering that the judge was not repeatable. Running the identical rubric a second time gave different numbers, with agreement on the genuine answers swinging from 88% to 75%, because the model was sampling its output with the API's built-in randomness turned up. With only 8 genuine pairs, one flipped grade moves the metric by 12.5%, so I could not tell one run apart from another, let alone tell a real rubric change apart from noise.

The fix was to set the judge to temperature 0, the setting that makes a model as repeatable as it can be. After that, two full runs produced results identical down to the byte, and only then did the agreement number mean anything.

A second lesson rode along with it. An earlier attempt to sharpen the wrong-versus-partial line looked like it lowered agreement, but at temperature 0 that apparent drop sat inside the run-to-run noise and could not be credited to the change, so I reverted it. The discipline that came out of this: measure more than once, remove the source of variance before tuning the prompt, and do not overfit a 22-point set.

## Known failure modes and limits

1. **Mild leniency on wrong answers.** On about 3 of the 22 pairs the judge called a confidently-wrong answer "partial" where I called it "wrong." This turns out to be harmless in practice: it never called a wrong answer "solid," and both partial and wrong leave a claim un-advanced, so nothing fake clears the gate. It only softens the label shown in feedback.
2. **Occasional harshness on hard long-tier answers** that brush aside the question's premise instead of engaging it. One answer I scored "partial" the judge scored "wrong." A genuinely debatable boundary.
3. **Single-rater calibration.** The judge is tuned to one person's standard, mine, so it cannot catch my own blind spots except through the seeded answers. Accepted for a single-user tool.
4. **Small sample.** Twenty-two pairs, eight of them genuine, is a thin estimate. Worth enlarging later, or judging each answer a few times and taking the majority, to tighten it.

## When to re-calibrate

Re-run this whenever the model changes, the judge's prompt or rubric changes, or the question generator changes. Calibration is not a one-time event. An unchecked change to the judge is an untrusted judge.
