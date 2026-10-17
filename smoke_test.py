from retrieval import BM25,evaluate
index=BM25(['walrus tusks','green bicycle','winter snow'])
assert index.search('WALRUS',1)==[0] and index.search('walrus',0)==[]
result=evaluate({0:[1,1,2],1:[2,0]},{0:{1:1,2:1},1:{0:1},2:{9:1}},k=3)
assert abs(result['recall']-2/3)<1e-9 and abs(result['mrr']-.5)<1e-9
try:BM25(['',''])
except ValueError:pass
else:raise AssertionError('Empty index accepted')
print('Lexical relevance, empty corpora, duplicated hits, and missing-query metrics passed.')
