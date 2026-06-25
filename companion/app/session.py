import datetime

import store
import bschecker
import scheduler


def run_check():
    """One interactive BS-check: pull the soonest-due claim, ask, wait for your
    typed answer, judge it, record the history, and reschedule the claim."""
    today = datetime.date.today().isoformat()
    due = store.due_claims(today)
    if not due:
        print("Nothing due for review right now. Log decisions, or come back later.")
        return
    claim = due[0]   # soonest-due
    decision_summary = store.get_decision_summary(claim["decision_id"])

    question = bschecker.generate_question(
        claim["claim_text"], decision_summary, claim["kind"], claim["tier"])
    print(f"\n[{claim['tier']} review of {claim['id']}]\n\n{question}\n")
    answer = input("Your answer: ").strip()   # <-- waits here for you to type

    j = bschecker.judge_answer(
        claim["claim_text"], decision_summary, question, answer, claim["tier"])

    # Deferred from Week 3 (needed a calibrated judge): ONE follow-up on a PARTIAL
    # answer -- a chance to supply the missing piece before scoring. Then re-judge the
    # combined response with the SAME calibrated judge, so calibration still holds.
    if j["verdict"] == "partial":
        fq = bschecker.followup_question(claim["claim_text"], question, answer, j["rationale"])
        print(f"\nClose -- one follow-up before I score it:\n\n{fq}\n")
        fa = input("Your answer: ").strip()
        answer = f"{answer}\n\n[Follow-up: {fq}]\n[Answer: {fa}]"
        j = bschecker.judge_answer(
            claim["claim_text"], decision_summary, question, answer, claim["tier"])

    outcome = "pass" if j["verdict"] == "solid" else "fail"   # partial/wrong don't advance

    new_tier, status, interval, next_review = scheduler.schedule(
        claim["tier"], claim["interval_days"], outcome, today)

    store.record_check({
        "claim_id": claim["id"], "date": today, "tier": claim["tier"],
        "question": question, "answer": answer, "score": j["score"],
        "verdict": j["verdict"], "rationale": j["rationale"],
        "ambiguous_question": int(j["ambiguous_question"]),
        "complete_answer": j["complete_answer"], "outcome": outcome,
        "next_review": next_review,
    })
    store.update_claim_state(claim["id"], new_tier, interval, next_review, status)

    print("\n--- Judge verdict (calibrated; see companion/judge-calibration.md) ---")
    print(f"Verdict: {j['verdict']}  (score {j['score']}/5)  ->  {outcome}")
    print(f"Why: {j['rationale']}")
    if j["ambiguous_question"]:
        print("(The judge flagged the QUESTION itself as ambiguous -- not held against you.)")
    print(f"\nFor your learning, a complete answer:\n{j['complete_answer']}")
    print(f"\nNext review: {next_review}  (tier: {new_tier}, status: {status})")
