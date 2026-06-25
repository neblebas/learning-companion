# Integrating Retrieval into the BS-Checker

**Status:** Built and wired in. The BS-Checker now checks each claim against the rest of my history, instead of judging it on its own.

---

## What this adds: cross-claim consistency, checked at log time

The moment I log a new decision, the companion cross-references each of its claims against my history:

1. It retrieves related past claims by meaning, using one embedding per claim.
2. It checks for genuine tension between the new claim and each related one, using a conservative checker.
3. When the tension is real, it tells me right away and records that tension as its own tracked claim, which then climbs the spaced-repetition tiers like any other. A real contradiction in my reasoning is something to resolve and defend over time, so it gets probed at review like any claim, with no special handling.

Why log time rather than review time: the natural moment a tension surfaces is when I record a decision that conflicts with a past one. Catching it at log time flags it the instant it enters the record. Waiting for review time would leave a fresh contradiction sitting unnoticed until the older claim happened to come up again. Log time is also sufficient on its own, because the new claim is compared against the entire history, so every contradiction gets caught, in both directions, as it arises.

## The design choice that carries the most weight: related does not mean contradictory

Semantic retrieval returns claims that are related, and "related" includes claims that agree or simply share a topic. Treating those as contradictions would manufacture fake tension. I saw this directly: the router-rule claim pulled up the scheduler and framework claims as related, but those are consistent applications of the same principle ("use rules, not an AI call, for simple logic"), not contradictions of it.

So a conservative tension-checker sits between retrieval and any action. Its standard is additive-only: it should only ever improve things, so it favors precision over recall. The default answer is "no tension," and a false alarm counts as worse than a miss. I validated it on three cases: a pair that agreed (it correctly stayed silent), a real contradiction (it fired, with a clean one-sentence statement of the conflict), and a subtle pair that looks contradictory on the surface but is actually consistent ("don't use an AI call for routing" versus "use an AI to structure text"), which it correctly let pass.

Dedup protects the same standard. A surfaced tension would otherwise reappear every time either parent claim came up for review, so the tension's identifier is built from the sorted pair of source-claim ids. Re-detecting the same conflict cannot create a duplicate, which keeps the review queue from filling with repeats.

## A resilience change, prompted by real friction

A sustained `529 Overloaded` from the API blocked verification in the middle of the build. I added retry-with-backoff to all four model clients. Honest scope: this handles brief blips, not sustained outages. Graceful degradation, telling a temporary error apart from a permanent one, and fallbacks are production-governance work, parked for a later module.

## An honest note on real-use iteration

A mature tool should also fix whatever weeks of daily real use surface. This version was built on a compressed timeline, so that accumulated-use feedback genuinely does not exist yet. Rather than invent it, I integrated the deferred retrieval features and left the first genuine cross-referenced review for real use to drive.

## The single follow-up loop

When the judge rules an answer partial, meaning the core reasoning is there but it is missing what the tier requires, the BS-Checker asks one focused follow-up aimed at the specific gap, takes that answer, and re-judges the combined response with the same calibrated judge, so calibration still holds. It fires only on partial: a wrong reason will not be rescued by a follow-up, and a solid answer has already passed. It is capped at one, so it never turns into an interrogation. The loop needed a calibrated judge before it could fire on a trustworthy "partial" signal. Verified: a partial answer triggered a precisely targeted follow-up, and supplying the missing piece flipped the re-judge to solid.
