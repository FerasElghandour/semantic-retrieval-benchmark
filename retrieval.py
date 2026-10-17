"""Lexical and optional semantic retrieval with explicit macro evaluation."""
import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path
import numpy as np

def tokens(text):return re.findall(r"\w+",text.lower())

class BM25:
    def __init__(self,documents,k1=1.2,b=.75):
        if not documents or not 0<=b<=1 or k1<=0:raise ValueError('Nonempty documents and valid BM25 parameters required')
        self.documents=list(documents);self.counts=[Counter(tokens(t)) for t in documents]
        self.lengths=np.array([sum(c.values()) for c in self.counts]);self.average=float(self.lengths.mean())
        if not self.average:raise ValueError('Corpus has no indexable terms')
        self.k1,self.b=k1,b;df=Counter(term for row in self.counts for term in row)
        self.idf={t:math.log(1+(len(documents)-n+.5)/(n+.5)) for t,n in df.items()}
    def search(self,query,k=5):
        if type(k) is not int or k<0:raise ValueError('Nonnegative integer k required')
        scores=np.zeros(len(self.counts))
        for term in set(tokens(query)):
            freq=np.array([row.get(term,0) for row in self.counts])
            denominator=freq+self.k1*(1-self.b+self.b*self.lengths/self.average)
            scores+=self.idf.get(term,0)*freq*(self.k1+1)/denominator
        return np.argsort(-scores,kind='stable')[:k].tolist()

class SemanticIndex:
    def __init__(self,documents,model_name,revision=None):
        from sentence_transformers import SentenceTransformer
        if not documents:raise ValueError('Nonempty documents required')
        self.model=SentenceTransformer(model_name,revision=revision)
        self.embeddings=self.model.encode(list(documents),normalize_embeddings=True)
    def search(self,query,k=5):
        if type(k) is not int or k<0:raise ValueError('Nonnegative integer k required')
        q=self.model.encode([query],normalize_embeddings=True)[0]
        return np.argsort(-(self.embeddings@q),kind='stable')[:k].tolist()

def evaluate(rankings,relevance,k=5):
    if type(k) is not int or k<1:raise ValueError('Positive integer k required')
    if not relevance:return {'recall':0.,'precision':0.,'mrr':0.}
    totals=np.zeros(3)
    for query,judgments in relevance.items():
        relevant={doc for doc,grade in judgments.items() if grade>0};rank=list(rankings.get(query,[]))
        hits=len(set(rank[:k])&relevant)
        reciprocal=next((1/i for i,d in enumerate(rank,1) if d in relevant),0.)
        totals+=[hits/len(relevant) if relevant else 0.,hits/k,reciprocal]
    return dict(zip(['recall','precision','mrr'],(totals/len(relevance)).tolist()))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('corpus',type=Path);p.add_argument('query');p.add_argument('--k',type=int,default=5);args=p.parse_args()
    documents=json.loads(args.corpus.read_text());index=BM25(documents)
    print(json.dumps([{'index':i,'text':documents[i]} for i in index.search(args.query,args.k)],indent=2))

