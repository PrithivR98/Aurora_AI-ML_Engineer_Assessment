# app/utils.py

from sentence_transformers import util

def semantic_search(question, messages, embedder, top_k=5):
    if not messages:
        return []

    corpus = [msg.get("message", "") for msg in messages]

    q_emb = embedder.encode(question, convert_to_tensor=True)
    c_emb = embedder.encode(corpus, convert_to_tensor=True)

    hits = util.semantic_search(q_emb, c_emb, top_k=min(top_k, len(corpus)))[0]

    ranked = []
    for hit in hits:
        idx = hit["corpus_id"]
        msg = messages[idx].copy()
        msg["__score"] = float(hit["score"])
        ranked.append(msg)

    return ranked
