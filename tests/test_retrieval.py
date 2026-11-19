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
