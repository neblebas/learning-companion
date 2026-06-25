import numpy as np

import store


def _entry_text(path):
    """The whole-entry text we embed: the markdown body, frontmatter stripped."""
    raw = open(path, encoding="utf-8").read()
    parts = raw.split("---", 2)          # frontmatter sits between the first two '---'
    return parts[2].strip() if len(parts) == 3 else raw.strip()


def corpus_entries():
    """Every decision as (id, one-line decision, whole-entry text)."""
    with store.connect() as conn:
        rows = conn.execute("SELECT id, decision, path FROM decisions").fetchall()
    return [(r["id"], r["decision"], _entry_text(r["path"])) for r in rows]


def build_index(model, entries=None):
    """Embed a list of (id, label, text) entries once; defaults to the decision
    corpus. Normalizing to unit length makes cosine similarity a plain dot product."""
    if entries is None:
        entries = corpus_entries()
    vecs = model.encode([e[2] for e in entries], normalize_embeddings=True)
    return [e[0] for e in entries], [e[1] for e in entries], np.array(vecs)


def claims_entries():
    """Every active claim as (id, kind, claim_text) -- the per-claim retrieval unit
    (the chunking we deferred in Week 5, now pointed at the BS-Checker's purpose)."""
    with store.connect() as conn:
        rows = conn.execute(
            "SELECT id, kind, claim_text FROM claims WHERE status='active'").fetchall()
    return [(r["id"], r["kind"], r["claim_text"]) for r in rows]


_claim_model = None


def related_claims(claim_id, claim_text, k=3):
    """Claims most similar in MEANING to a given one, excluding itself. Rebuilds the
    claim index each call so newly-logged claims are included. NOTE: 'related' is not
    'in tension' -- that stricter judgment happens downstream."""
    global _claim_model
    if _claim_model is None:
        from sentence_transformers import SentenceTransformer
        _claim_model = SentenceTransformer(_MODEL_NAME)
    index = build_index(_claim_model, claims_entries())
    hits = search(claim_text, _claim_model, index, k=k + 1)   # +1 so we can drop self
    return [(i, kind, s) for i, kind, s in hits if i != claim_id][:k]


def search(query, model, index, k=3, query_prefix=""):
    """Top-k entries by cosine similarity. Some models (bge) want a query prefix;
    pass it in so passages and queries are encoded the way the model expects."""
    ids, decisions, matrix = index
    q = model.encode([query_prefix + query], normalize_embeddings=True)[0]
    sims = matrix @ q                    # all 8 cosine similarities in one multiply
    order = np.argsort(-sims)[:k]        # indices of the highest scores
    return [(ids[i], decisions[i], float(sims[i])) for i in order]


# --- Convenience wrapper for the app: the model chosen in the Week 5 eval. ---
_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"   # MiniLM needs no query prefix
_model = None
_index = None


def semantic_search(query, k=3):
    """Search the corpus by MEANING. Lazily loads the model + builds the index
    once per process -- the heavy sentence-transformers/PyTorch import is deferred
    to here, so plain log/query commands never pay for it."""
    global _model, _index
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(_MODEL_NAME)
        _index = build_index(_model)
    return search(query, _model, _index, k=k)
