import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from retrieval import BM25,rrf
class RetrievalTest(unittest.TestCase):
    def test_lexical_unknown_and_chinese(self):
        m=BM25([{'id':'a','text':'上班 疲惫'},{'id':'b','text':'开心'}])
        self.assertEqual(m.search('上班')[0][0],'a')
        self.assertEqual(m.search('abc'),[])
    def test_rrf_duplicate(self):
        self.assertEqual(rrf([['a','a','b'],['b']])[0],'b')

    def test_bm25_hand_calculated_length_and_tie(self):
        docs = [{'id':'b','text':'累'}, {'id':'a','text':'很累'}, {'id':'c','text':'笑'}]
        model = BM25(docs)
        ranking = model.search('累累')
        self.assertEqual([item for item, _ in ranking], ['b', 'a'])
        self.assertAlmostEqual(ranking[0][1], 0.52958155, places=7)
        self.assertAlmostEqual(ranking[1][1], 0.38367643, places=7)
        self.assertEqual([item for item, _ in BM25(docs, b=0).search('累')], ['a', 'b'])
