"""Small, original character-token BM25 and reciprocal-rank fusion baseline."""
import math, re
from collections import Counter, defaultdict

def tokens(text):
    return re.findall(r"[\u4e00-\u9fff]|[a-z0-9]+", text.lower())

class BM25:
    def __init__(self, docs, k1=1.5, b=.75):
        if not docs:
            raise ValueError("empty corpus")
        self.docs = docs
        self.tf = [Counter(tokens(x["text"])) for x in docs]
        self.lengths = [sum(x.values()) for x in self.tf]
        self.avg = sum(self.lengths) / len(docs) or 1
        self.df = Counter(t for d in self.tf for t in d)
        self.k1, self.b = k1, b

    def contributions(self, terms, doc_index):
        """Return one dictionary per matched term, using the production score."""
        counts = self.tf[doc_index]
        length = self.lengths[doc_index]
        normalizer = self.k1 * (1 - self.b + self.b * length / self.avg)
        for term in terms:
            frequency = counts[term]
            if frequency:
                df = self.df[term]
                idf = math.log(1 + (len(self.docs) - df + .5) / (df + .5))
                tf_weight = frequency * (self.k1 + 1) / (frequency + normalizer)
                yield {"term": term, "tf": frequency, "df": df, "idf": idf,
                       "tf_weight": tf_weight, "score": idf * tf_weight}

    def search(self, query, k=10):
        if k <= 0:
            raise ValueError("k must be positive")
        out = []
        terms = tuple(dict.fromkeys(tokens(query)))
        for index, doc in enumerate(self.docs):
            score = sum(part["score"] for part in self.contributions(terms, index))
            if score > 0:
                out.append((doc["id"], score))
        return sorted(out, key=lambda x:(-x[1], x[0]))[:k]

def rrf(rankings, c=60):
    if c < 0:
        raise ValueError("c must be nonnegative")
    scores = defaultdict(float)
    for ranking in rankings:
        for rank, item in enumerate(dict.fromkeys(ranking), 1):
            scores[item] += 1 / (c + rank)
    return sorted(scores, key=lambda x:(-scores[x],x))
