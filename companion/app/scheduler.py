import datetime

# The spaced-repetition ladder. Days until the next review after PASSING into a
# tier. (spot is same-session = 0 days.) Tuned for this instance: long = 30 days
# rather than the methodology's default 45.
PASS_INTERVAL = {"short": 2, "medium": 10, "long": 30}
LONG_STRETCH = 2.5   # each pass AT the long tier multiplies the interval


def _next_review(today, days):
    """Add `days` to an ISO date string and return the new ISO date string."""
    return (datetime.date.fromisoformat(today) + datetime.timedelta(days=days)).isoformat()


def schedule(tier, interval_days, outcome, today):
    """Pure, deterministic rule: given a claim's current tier + interval and a
    pass/fail, return its new (tier, status, interval_days, next_review).
    No database, no AI -- same inputs always give the same answer."""
    if outcome == "pass":
        if tier == "spot":
            new_tier, days = "short", PASS_INTERVAL["short"]
        elif tier == "short":
            new_tier, days = "medium", PASS_INTERVAL["medium"]
        elif tier == "medium":
            new_tier, days = "long", PASS_INTERVAL["long"]
        else:  # already long: stay long, stretch the interval, mark durable
            new_tier, days = "long", round(interval_days * LONG_STRETCH)
        # Durable only once a claim PASSES while already at the long tier.
        status = "durable" if tier == "long" else "active"
        return new_tier, status, days, _next_review(today, days)

    # fail: drop back to a quick re-check (same-session if you were only at short).
    if tier in ("spot", "short"):
        new_tier, days = "spot", 0
    else:
        new_tier, days = "short", PASS_INTERVAL["short"]
    return new_tier, "active", days, _next_review(today, days)
