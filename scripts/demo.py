import argparse, json
from pathlib import Path
from retrieval import BM25
from metrics import metrics

def main():
    root = Path(__file__).resolve().parents[1]
    p = argparse.ArgumentParser()
    p.add_argument('--query', default='不想上班')
    p.add_argument('--data', type=Path, default=root/'data/sample/memes.json')
    p.add_argument('--queries', type=Path, default=root/'data/sample/queries.json')
    args = p.parse_args()
    docs = json.loads(args.data.read_text())
    model = BM25(docs)
    print(json.dumps({'query':args.query,'results':model.search(args.query,3)},ensure_ascii=False))
    results = [metrics([i for i,s in model.search(q['query'],3)],q['relevant'],3)
               for q in json.loads(args.queries.read_text())]
    valid = [x for x in results if x is not None]
    print(json.dumps({'dataset':'handcrafted-text-smoke-fixture','k':3,'queries':len(results),
        'excluded_no_positive':len(results)-len(valid),
        'metrics':{k:sum(r[k] for r in valid)/len(valid) for k in valid[0]} if valid else {}},ensure_ascii=False))
if __name__=='__main__': main()
