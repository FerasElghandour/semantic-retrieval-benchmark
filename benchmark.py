"""Full lexical retrieval evaluation for a supplied corpus/query/judgment JSON.

Input: documents [{id,text}], queries [{id,text,relevant:[document IDs]}].
Parameters are fixed before scoring. All rankings are retained so MRR uses the
complete corpus, while precision and recall use the requested cutoff.
"""
import argparse,hashlib,json,time
from pathlib import Path
from retrieval import BM25,SemanticIndex,evaluate
p=argparse.ArgumentParser(description=__doc__);p.add_argument('dataset',type=Path);p.add_argument('--output',type=Path,required=True);p.add_argument('--k',type=int,default=5);p.add_argument('--dense-model');p.add_argument('--dense-revision');a=p.parse_args()
if a.output.exists() or a.k<1:raise ValueError('New output directory and positive cutoff required')
d=json.loads(a.dataset.read_text());docs=d['documents'];queries=d['queries'];ids=[r['id'] for r in docs]
if len(ids)!=len(set(ids)) or not queries or len({q['id'] for q in queries})!=len(queries):raise ValueError('Unique document/query IDs and nonempty queries required')
if any(not set(q['relevant'])<=set(ids) for q in queries):raise ValueError('Relevance IDs must exist in corpus')
a.output.mkdir(parents=True);start=time.perf_counter();index=BM25([r['text'] for r in docs]);
if a.dense_model:
 import torch
 torch.set_num_threads(2);index=SemanticIndex([r['text'] for r in docs],a.dense_model,revision=a.dense_revision)
rankings={q['id']:[ids[i] for i in index.search(q['text'],len(ids))] for q in queries};judgments={q['id']:{key:1 for key in q['relevant']} for q in queries}
result={'method':a.dense_model or 'BM25 k1=1.2 b=0.75','documents':len(docs),'queries':len(queries),'k':a.k,'metrics':evaluate(rankings,judgments,a.k),'seconds':time.perf_counter()-start,'input_sha256':hashlib.sha256(a.dataset.read_bytes()).hexdigest(),'dense_revision':a.dense_revision,'mrr_scope':'full ranking; not truncated at k'}
(a.output/'metrics.json').write_text(json.dumps(result,indent=2)+'\n');(a.output/'rankings.json').write_text(json.dumps(rankings,indent=2)+'\n')
