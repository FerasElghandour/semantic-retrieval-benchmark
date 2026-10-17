"""Prepare the fixed BEIR SciFact test corpus and qrels without extracting ZIPs."""
import argparse,csv,io,json,hashlib,zipfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('archive',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
if a.output.exists():raise ValueError('Use a new output')
if hashlib.sha256(a.archive.read_bytes()).hexdigest()!='536e14446a0ba56ed1398ab1055f39fe852686ecad24a6306c80c490fa8e0165':raise ValueError('Expected canonical BEIR SciFact archive')
with zipfile.ZipFile(a.archive) as z:
 corpus=[json.loads(line) for line in z.read('scifact/corpus.jsonl').decode().splitlines()]
 queries={str(row['_id']):row['text'] for row in (json.loads(line) for line in z.read('scifact/queries.jsonl').decode().splitlines())}
 qrels={}
 for row in csv.DictReader(io.StringIO(z.read('scifact/qrels/test.tsv').decode()),delimiter='\t'):
  if int(row['score'])>0:qrels.setdefault(row['query-id'],[]).append(row['corpus-id'])
 documents=[{'id':str(r['_id']),'text':r.get('title','')+' '+r['text']} for r in corpus]
 data={'source':'BEIR SciFact fixed test split','archive_sha256':hashlib.sha256(a.archive.read_bytes()).hexdigest(),'documents':documents,'queries':[{'id':q,'text':queries[q],'relevant':relevant} for q,relevant in sorted(qrels.items())]}
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(data)+'\n')
print(json.dumps({'documents':len(documents),'test_queries':len(qrels),'archive_sha256':data['archive_sha256']}))
