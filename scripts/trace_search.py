"""Explain a BM25 query using the same term contributions as search()."""
import argparse
import json
from pathlib import Path

from metrics import metrics
from retrieval import BM25, tokens


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--data", type=Path, default=root / "data/sample/memes.json")
    parser.add_argument("--positive", action="append", default=[])
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--b", type=float, default=.75)
    args = parser.parse_args()
    if args.k < 1 or not 0 <= args.b <= 1:
        parser.error("require k >= 1 and 0 <= b <= 1")
    docs = json.loads(args.data.read_text(encoding="utf-8"))
    model = BM25(docs, b=args.b)
    terms = list(dict.fromkeys(tokens(args.query)))
    ranked = model.search(args.query, args.k)
    details = []
    for index, doc in enumerate(docs):
        parts = list(model.contributions(terms, index))
        if parts:
            details.append({"id": doc["id"], "length": model.lengths[index],
                            "score": sum(part["score"] for part in parts), "parts": parts})
    result = {
        "query": args.query, "tokens": terms, "document_count": len(docs),
        "average_length": model.avg, "query_df": {term: model.df[term] for term in terms},
        "matching_docs": sorted(details, key=lambda item: (-item["score"], item["id"])),
        "top_k": [item for item, _ in ranked],
        "metrics": metrics([item for item, _ in ranked], args.positive, args.k),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
