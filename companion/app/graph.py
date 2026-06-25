import config  # loads .env and disables tracing BEFORE langchain/langgraph import
import datetime
from typing import TypedDict
from pydantic import BaseModel, Field
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END

import store
import rag
import bschecker


class CompanionState(TypedDict):
    """The 'working note' that travels through the flowchart, start to finish.

    - mode:   which path to take ('log', 'query', or 'check')
    - text:   what the user said (used when logging)
    - tag:    optional filter for the 'query' path
    - since:  optional date filter for the 'query' path (YYYY-MM-DD)
    - find:   optional natural-language query for semantic search
    - result: what the system hands back at the end
    """
    mode: str
    text: str
    tag: str
    since: str
    find: str
    result: str


# --- The SCHEMA: the "form with labeled blanks" the AI fills from free-text. ---
# Each field has a plain-language description so the AI knows what goes where.
class DecisionFields(BaseModel):
    decision: str = Field(description="The build decision, in one clear sentence.")
    alternatives_considered: list[str] = Field(description="Other options that were weighed.")
    rationale: str = Field(description="Why this choice was made (2-5 sentences).")
    expected_tradeoffs: list[str] = Field(description="Downsides knowingly accepted.")
    tags: list[str] = Field(description="2-5 short lowercase topic tags.")
    claimed_learnings: list[str] = Field(description="Things the user claims to have learned.")


# Build the AI once. ".with_structured_output(...)" is what turns a normal,
# free-form model into one that MUST return data shaped like the form above.
_llm = ChatAnthropic(model=config.MODEL, max_tokens=1024, max_retries=5).with_structured_output(DecisionFields)


def route(state):
    """The traffic cop. Picks the next box purely from the mode -- no AI call.
    Three destinations now: log it, show me, or check me."""
    mode = state["mode"]
    if mode == "log":
        return "decision_log"
    if mode == "query":
        return "retrieve"
    return "bs_checker"


def decision_log(state):
    """Real logger: the AI structures your free-text into the form, then we
    save those fields to the corpus (readable document + index entry)."""
    # One API call: hand the model your note, get back the filled-in form.
    fields = _llm.invoke(
        "Pull the build decision out of the user's note and fill in the form. "
        "Stay faithful to what they actually said -- do not invent details.\n\n"
        f"User note:\n{state['text']}"
    )
    entry = fields.model_dump()                       # the form -> a plain dict
    entry["date"] = datetime.date.today().isoformat()
    entry["session"] = state.get("session", "manual")
    entry["linked_artifact"] = ""
    new_id = store.save_decision(entry)
    # Log-time cross-reference: catch genuine tension with your history the MOMENT a
    # contradicting decision is recorded (not whenever an old claim is next reviewed).
    note = _crossref_new_decision(new_id, entry["date"])
    return {"result": f"Logged {new_id}: {entry['decision']}  (tags: {entry['tags']}){note}"}


def _crossref_new_decision(decision_id, today):
    """For each claim of a just-logged decision, surface genuine tension with the
    existing history (conservative, additive-only) and spawn it as a tracked claim."""
    spawned = []
    for c in store.claims_of_decision(decision_id):
        for rid, _kind, _score in rag.related_claims(c["id"], c["claim_text"], k=3):
            v = bschecker.detect_tension(c["claim_text"], store.get_claim(rid)["claim_text"])
            if v["has_tension"]:
                tid = store.spawn_tension_claim(c["id"], rid, v["statement"], decision_id, today)
                if tid:
                    spawned.append(tid)
                break   # one surfaced tension per new claim is enough for v0
    return ("\n  tension(s) surfaced & now tracked: " + ", ".join(spawned)) if spawned else ""


def retrieve(state):
    """Show-me path. Two modes: semantic search by meaning (--find), or the exact
    tag/date filter. Both return short summaries to scan, not full documents."""
    if state.get("find"):
        hits = rag.semantic_search(state["find"], k=3)
        if not hits:
            return {"result": "No decisions logged yet."}
        lines = [f"- {id_} ({score:.2f})  {dec}" for id_, dec, score in hits]
        return {"result": f"Closest by meaning to '{state['find']}':\n" + "\n".join(lines)}

    hits = store.query_decisions(tag=state.get("tag"), since=state.get("since"))
    if not hits:
        return {"result": "No matching decisions found."}
    lines = [f"- {d['id']} [{d['date']}] {d['decision']}  (tags: {d['tags']})"
             for d in hits]
    return {"result": f"{len(hits)} decision(s):\n" + "\n".join(lines)}


def bs_checker(state):
    """PLACEHOLDER. The BS-Checker is built in Week 3."""
    return {"result": "[bs-checker] coming in Week 3 -- nothing to check yet."}


def build():
    """Assemble and compile the flowchart -- this IS the orchestrator."""
    g = StateGraph(CompanionState)
    g.add_node("decision_log", decision_log)
    g.add_node("retrieve", retrieve)
    g.add_node("bs_checker", bs_checker)
    # At the very start, hand control to the router, which chooses the box.
    g.add_conditional_edges(START, route, {
        "decision_log": "decision_log",
        "retrieve": "retrieve",
        "bs_checker": "bs_checker",
    })
    g.add_edge("decision_log", END)
    g.add_edge("retrieve", END)
    g.add_edge("bs_checker", END)
    return g.compile()
