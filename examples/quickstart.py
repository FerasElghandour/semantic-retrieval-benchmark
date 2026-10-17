"""Offline example using the public implementation; see README for evidence scope."""
import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
os.chdir(ROOT)

from retrieval import BM25, evaluate
# Three fictional documents; no model download.
documents = ['walrus tusks', 'green bicycle', 'winter snow']
ranked = BM25(documents).search('WALRUS', 1)
result = {'ranked_indices': ranked, 'top_document': documents[ranked[0]], 'metrics': evaluate({0: ranked}, {0: {0: 1}}, k=1)}

import json
print(json.dumps(result, indent=2))

