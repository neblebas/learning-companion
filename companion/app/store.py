import datetime
import sqlite3

import config


def connect():
    """Open (creating if needed) the SQLite database file."""
    conn = sqlite3.connect(config.DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")   # SQLite ignores FKs unless switched on
    conn.row_factory = sqlite3.Row             # rows accessible by column name, not index
    return conn


def init_db():
    """Create the corpus dir and both tables if absent. Safe to run every startup."""
    config.CORPUS_DIR.mkdir(exist_ok=True)
    with connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS decisions (
                id              TEXT PRIMARY KEY,
                date            TEXT,
                session         TEXT,
                decision        TEXT,
                linked_artifact TEXT,
                path            TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS decision_tags (
                decision_id TEXT REFERENCES decisions(id),
                tag         TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS claims (
                id            TEXT PRIMARY KEY,
                decision_id   TEXT REFERENCES decisions(id),
                claim_text    TEXT,
                kind          TEXT,       -- 'rationale' or 'learning'
                tier          TEXT,       -- spot | short | medium | long
                interval_days INTEGER,    -- current spacing; long tier stretches it
                next_review   TEXT,       -- YYYY-MM-DD, when this claim is next due
                status        TEXT        -- 'active' or 'durable'
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS bs_checks (
                id                 TEXT PRIMARY KEY,
                claim_id           TEXT REFERENCES claims(id),
                date               TEXT,
                tier               TEXT,    -- tier at the time of this check
                question           TEXT,
                answer             TEXT,
                score              INTEGER,
                verdict            TEXT,    -- solid | partial | wrong
                rationale          TEXT,
                ambiguous_question INTEGER, -- 0/1
                complete_answer    TEXT,    -- the teaching field
                outcome            TEXT,    -- pass | fail (what the scheduler used)
                next_review        TEXT     -- what was scheduled next
            )
            """
        )


def _next_id(conn, date):
    """dl-YYYYMMDD-NNN, where NNN is the next sequence number for this date.
    Uses count(*)+1 — fine for v0 since we never delete; a deletion could
    otherwise collide an old id with a reused number."""
    n = conn.execute(
        "SELECT count(*) FROM decisions WHERE date = ?", (date,)
    ).fetchone()[0] + 1
    return f"dl-{date.replace('-', '')}-{n:03d}"


def _render_markdown(entry):
    """The human-readable 'book' — YAML frontmatter + readable body."""
    def bullets(items):
        return "\n".join(f"- {x}" for x in items) or "- (none)"
    return (
        f"---\n"
        f"id: {entry['id']}\n"
        f"date: {entry['date']}\n"
        f"session: {entry['session']}\n"
        f"tags: {entry['tags']}\n"
        f"linked_artifact: {entry.get('linked_artifact', '')}\n"
        f"---\n\n"
        f"# Decision\n{entry['decision']}\n\n"
        f"## Alternatives considered\n{bullets(entry['alternatives_considered'])}\n\n"
        f"## Rationale\n{entry['rationale']}\n\n"
        f"## Expected tradeoffs\n{bullets(entry['expected_tradeoffs'])}\n\n"
        f"## Claimed learnings\n{bullets(entry['claimed_learnings'])}\n"
    )


def save_decision(entry):
    """Persist a structured decision: markdown 'book' + SQLite 'catalog card'."""
    entry.setdefault("date", datetime.date.today().isoformat())
    entry.setdefault("session", "manual")
    with connect() as conn:
        entry["id"] = _next_id(conn, entry["date"])
        path = config.CORPUS_DIR / f"{entry['id']}.md"
        path.write_text(_render_markdown(entry), encoding="utf-8")
        conn.execute(
            "INSERT INTO decisions (id, date, session, decision, linked_artifact, path)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (entry["id"], entry["date"], entry["session"], entry["decision"],
             entry.get("linked_artifact", ""), str(path)),
        )
        conn.executemany(
            "INSERT INTO decision_tags (decision_id, tag) VALUES (?, ?)",
            [(entry["id"], tag) for tag in entry["tags"]],
        )
        register_claims(conn, entry["id"], entry, entry["date"])
    return entry["id"]


def query_decisions(tag=None, since=None):
    """Read decisions back out, optionally narrowed by tag and/or date.

    Plain-English what & why:
    - We read ONLY the lightweight index here (the 'catalog cards'), never the
      full documents -- so lookups stay fast even with a large corpus.
    - tag   = only decisions carrying this tag.
    - since = only decisions logged on or after this date (YYYY-MM-DD).
    - No filters = return everything. Either way, newest first.
    """
    with connect() as conn:
        if tag:
            # Find cards whose id appears in the tag list for this tag.
            sql = ("SELECT d.* FROM decisions d "
                   "JOIN decision_tags t ON d.id = t.decision_id "
                   "WHERE t.tag = ?")
            params = [tag]
        else:
            # "1=1" is just a harmless placeholder so we can tack on the optional
            # date filter below without worrying whether a WHERE already exists.
            sql = "SELECT * FROM decisions d WHERE 1=1"
            params = []
        if since:
            sql += " AND d.date >= ?"
            params.append(since)
        sql += " ORDER BY d.date DESC, d.id DESC"

        results = [dict(r) for r in conn.execute(sql, params).fetchall()]
        # Re-attach each decision's tags so the caller gets the full card back.
        for r in results:
            r["tags"] = [t["tag"] for t in conn.execute(
                "SELECT tag FROM decision_tags WHERE decision_id = ?", (r["id"],)
            ).fetchall()]
    return results


def register_claims(conn, decision_id, entry, date):
    """Register each checkable claim from a decision -- the rationale plus each
    claimed learning -- as its own row. All start at 'spot' tier, due today
    (the same-session check the spec requires for every new claim)."""
    claims = [("rationale", entry["rationale"])]
    claims += [("learning", text) for text in entry.get("claimed_learnings", [])]
    rows = [
        (f"{decision_id}-c{i}", decision_id, text, kind, "spot", 0, date, "active")
        for i, (kind, text) in enumerate(claims, start=1)
    ]
    conn.executemany(
        "INSERT INTO claims (id, decision_id, claim_text, kind, tier, interval_days,"
        " next_review, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        rows,
    )


def due_claims(today):
    """The review queue: active claims due on/before `today`, soonest first."""
    with connect() as conn:
        rows = conn.execute(
            "SELECT * FROM claims WHERE status = 'active' AND next_review <= ? "
            "ORDER BY next_review ASC, id ASC", (today,)
        ).fetchall()
    return [dict(r) for r in rows]


def get_decision_summary(decision_id):
    """The one-line decision text for a claim's source decision."""
    with connect() as conn:
        row = conn.execute("SELECT decision FROM decisions WHERE id=?",
                           (decision_id,)).fetchone()
    return row["decision"] if row else ""


def get_claim(claim_id):
    """Fetch a single claim row by id (used by the calibration harness)."""
    with connect() as conn:
        row = conn.execute("SELECT * FROM claims WHERE id=?", (claim_id,)).fetchone()
    return dict(row) if row else None


def claims_of_decision(decision_id):
    """The non-tension claims belonging to one decision (its rationale + learnings)."""
    with connect() as conn:
        rows = conn.execute(
            "SELECT * FROM claims WHERE decision_id=? AND kind!='tension'", (decision_id,)
        ).fetchall()
    return [dict(r) for r in rows]


def record_check(check):
    """Append one row to the bs_checks HISTORY log -- append-only, never edited.
    This is what Week 4 calibration reads back to compare the judge against you."""
    with connect() as conn:
        n = conn.execute("SELECT count(*) FROM bs_checks WHERE date = ?",
                         (check["date"],)).fetchone()[0] + 1
        check_id = f"bsc-{check['date'].replace('-', '')}-{n:03d}"
        conn.execute(
            "INSERT INTO bs_checks (id, claim_id, date, tier, question, answer, score,"
            " verdict, rationale, ambiguous_question, complete_answer, outcome, next_review)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (check_id, check["claim_id"], check["date"], check["tier"], check["question"],
             check["answer"], check["score"], check["verdict"], check["rationale"],
             check["ambiguous_question"], check["complete_answer"], check["outcome"],
             check["next_review"]),
        )
    return check_id


def update_claim_state(claim_id, tier, interval_days, next_review, status):
    """Overwrite a claim's CURRENT review state in place. History lives in bs_checks;
    this row only ever holds 'where the claim is now.'"""
    with connect() as conn:
        conn.execute(
            "UPDATE claims SET tier=?, interval_days=?, next_review=?, status=? WHERE id=?",
            (tier, interval_days, next_review, status, claim_id),
        )


def spawn_tension_claim(a_id, b_id, statement, decision_id, today):
    """Register a surfaced tension as its OWN tracked claim, once per A-B pair.
    The id is derived from the sorted pair, so re-detecting the same tension can't
    create a duplicate. Returns the new claim id, or None if it already existed."""
    tid = "tn-" + "--".join(sorted([a_id, b_id]))
    with connect() as conn:
        if conn.execute("SELECT 1 FROM claims WHERE id=?", (tid,)).fetchone():
            return None
        conn.execute(
            "INSERT INTO claims (id, decision_id, claim_text, kind, tier, interval_days,"
            " next_review, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (tid, decision_id, statement, "tension", "spot", 0, today, "active"),
        )
    return tid
