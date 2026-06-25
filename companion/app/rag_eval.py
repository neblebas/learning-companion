from sentence_transformers import SentenceTransformer
import rag

# Hand-crafted ground truth: each query -> the decision id that should rank top.
QUERIES = {
    "how do we avoid saving the in-progress conversation": "dl-20260615-002",
    "fast lookups without opening every file as the corpus grows": "dl-20260615-003",
    "making it easy to find entries by topic label": "dl-20260615-004",
    "why use a plain rule instead of the model to route": "dl-20260615-005",
    "what makes the review scheduling predictable and repeatable": "dl-20260615-006",
    "why grading gets stricter for more mature claims": "dl-20260615-007",
    "why we didn't build session persistence yet": "dl-20260615-008",
    "picking the agent orchestration framework": "dl-20260615-001",
}

# bge models want a query-side instruction prefix; MiniLM does not.
BGE_PREFIX = "Represent this sentence for searching relevant passages: "
MODELS = [
    ("all-MiniLM-L6-v2", "sentence-transformers/all-MiniLM-L6-v2", ""),
    ("bge-small-en-v1.5", "BAAI/bge-small-en-v1.5", BGE_PREFIX),
    ("bge-base-en-v1.5", "BAAI/bge-base-en-v1.5", BGE_PREFIX),
]


def evaluate():
    n = len(QUERIES)
    for label, name, prefix in MODELS:
        model = SentenceTransformer(name)
        index = rag.build_index(model)
        p1 = r3 = 0
        misses = []
        for q, target in QUERIES.items():
            ranked = [h[0] for h in rag.search(q, model, index, k=3, query_prefix=prefix)]
            if ranked[0] == target:
                p1 += 1
            if target in ranked:
                r3 += 1
            else:
                misses.append((q, target, ranked[0]))
        print(f"{label:20} P@1 = {p1}/{n}   Recall@3 = {r3}/{n}")
        for q, target, got in misses:
            print(f"    miss: '{q[:45]}...' wanted {target[-3:]} got {got[-3:]}")


if __name__ == "__main__":
    evaluate()
