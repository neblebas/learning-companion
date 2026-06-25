import json
from pathlib import Path

import store
import bschecker

CAL_PATH = Path(__file__).resolve().parent / "calibration" / "calibration_set.json"


def cohens_kappa(labels_a, labels_b, categories):
    """Agreement beyond chance. po = how often the two raters actually agree;
    pe = how often they'd agree by luck given how often each uses each label;
    kappa = (po - pe) / (1 - pe) = the share of above-luck room captured."""
    n = len(labels_a)
    po = sum(1 for a, b in zip(labels_a, labels_b) if a == b) / n
    pe = sum((labels_a.count(c) / n) * (labels_b.count(c) / n) for c in categories)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def run():
    pairs = json.loads(CAL_PATH.read_text(encoding="utf-8"))

    # Run the judge BLIND over every pair -- it never sees your label, and it
    # judges at each pair's tier so rising rigor is exercised.
    for p in pairs:
        claim = store.get_claim(p["claim_id"])
        summary = store.get_decision_summary(claim["decision_id"])
        j = bschecker.judge_answer(claim["claim_text"], summary,
                                   p["question"], p["answer"], p["tier"])
        p["judge_verdict"] = j["verdict"]
        p["judge_score"] = j["score"]
    CAL_PATH.write_text(json.dumps(pairs, indent=2), encoding="utf-8")

    cats = ["solid", "partial", "wrong"]

    def report(subset, name):
        mine = [p["my_label"] for p in subset]
        judge = [p["judge_verdict"] for p in subset]
        exact = sum(1 for a, b in zip(mine, judge) if a == b)
        k = cohens_kappa(mine, judge, cats)
        print(f"{name}: n={len(subset)}  exact={exact}/{len(subset)} "
              f"({100*exact/len(subset):.0f}%)  kappa={k:.2f}")

    report(pairs, "ALL    ")
    report([p for p in pairs if p["source"] == "genuine"], "GENUINE")

    seeds = [p for p in pairs if p["source"] == "seed"]
    caught = sum(1 for p in seeds if p["judge_verdict"] != "solid")
    print(f"SEEDS caught (not passed as solid): {caught}/{len(seeds)}")

    print("\nDisagreements (you vs judge):")
    for p in pairs:
        if p["my_label"] != p["judge_verdict"]:
            print(f"  {p['id']} [{p['tier']:6} {p['source']:7}] "
                  f"you={p['my_label']:7} judge={p['judge_verdict']:7} (score {p['judge_score']})")


if __name__ == "__main__":
    run()
