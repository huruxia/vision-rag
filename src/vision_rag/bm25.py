import math
import jieba

class BM25:
    """简易 BM25：k1=1.5, b=0.75，中文用 jieba 分词"""
    def __init__(self, texts: list[str]):
        self.corpus = [jieba.lcut(t) for t in texts]   # 每篇分词后的词列表
        self.N = len(self.corpus)
        self.doc_len = [len(d) for d in self.corpus]
        self.avgdl = sum(self.doc_len) / self.N
        self.df: dict[str, int] = {}                    # 词 -> 出现在几篇文档
        self.tf: list[dict[str, int]] = []              # 每篇文档: 词 -> 词频
        for doc in self.corpus:
            tf = {}
            for term in doc:
                tf[term] = tf.get(term, 0) + 1
            for term in set(doc):
                self.df[term] = self.df.get(term, 0) + 1
            self.tf.append(tf)
        self.k1 = 1.5
        self.b = 0.75

    def idf(self, term: str) -> float:
        df = self.df.get(term, 0)
        return math.log((self.N - df + 0.5) / (df + 0.5) + 1.0)

    def scores(self, query: str) -> list[float]:
        qterms = jieba.lcut(query)
        out = []
        for i in range(self.N):
            dl = self.doc_len[i]
            s = 0.0
            for t in qterms:
                tf = self.tf[i].get(t, 0)
                if tf == 0:
                    continue
                tf_part = tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * dl / self.avgdl))
                s += self.idf(t) * tf_part
            out.append(s)
        return out
