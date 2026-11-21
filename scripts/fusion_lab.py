"""Inspect where lexical and visual toy rankings contribute unique positives."""
import json
from pathlib import Path

from metrics import metrics
from retrieval import BM25, rrf


CORPUS = Path(__file__).resolve().parents[1] / "data/sample/memes.json"
CASES = (
    ("台词", "下班", {"m02"}, ["m04", "m07", "m02"]),
    ("语义", "累成狗", {"m01", "m08"}, ["m01", "m08", "m05"]),
    ("对象", "猫", {"m06"}, ["m03", "m06", "m05"]),
    ("空结果", "量子力学", set(), ["m03", "m07", "m01"]),
)


def main():
    model = BM25(json.loads(CORPUS.read_text(encoding="utf-8")))
    limit = 2
    for kind, query, relevant, visual in CASES:
        lexical = [item for item, _ in model.search(query, 3)]
        mixed = rrf([lexical, visual])
        print(json.dumps({
            "kind": kind,
            "query": query,
            "positive_ids": sorted(relevant),
            "lexical": lexical,
            "visual_fixture": visual,
            "fusion": mixed,
            "lexical_only_positive": sorted((set(lexical) - set(visual)) & relevant),
            "visual_only_positive": sorted((set(visual) - set(lexical)) & relevant),
            "scores_at_2": {
                name: metrics(ranking, relevant, limit)
                for name, ranking in (("lexical", lexical), ("visual", visual), ("fusion", mixed))
            },
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()
