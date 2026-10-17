# Reproduction and benchmark scope

A full-corpus benchmark entry point now retains rankings and evaluates supplied judgments. A new fixed BEIR SciFact test run uses5,183 documents and300 queries, with corpus provenance and full-ranking MRR.

## Execute a recorded profile

```sh
python run_reproduction.py --profile checks --output reproduced/checks
```

Use a new output directory for each run. The driver writes command logs, source/input SHA-256 values, versions and an explicit outcome. It does not silently download data or turn generated fixtures into dataset-performance claims.

| Profile | Actual scope | Required inputs |
|---|---|---|
| `checks` | Offline behavioral regressions; not a fresh dataset benchmark | None |
| `lexical-benchmark` | BM25 full corpus ranking and supplied relevance judgments; not a dense-model benchmark | dataset |

Supply named paths with `--input name=/absolute/path`. Exact commands are versioned in [reproduction.json](reproduction.json); direct training commands and preparation contracts are below.

## Evidence boundary

This new SciFact benchmark is separate from the retained reduced Natural Questions experiment. Pretrained embedding use is not a claim of training those models.

Keep input acquisition and source credits in [DATA.md](DATA.md). Historical results, new reference runs and small contract fixtures have separate evidential scope.

## Direct commands and inputs

Acquire the [BEIR SciFact archive](https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/scifact.zip). The preparer checks its SHA-256 and preserves the fixed test judgments.

```sh
python prepare_beir.py scifact.zip --output data/scifact.json
python benchmark.py data/scifact.json --k 5 --output runs/scifact-bm25
python -m pip install -r requirements-dense.txt
python benchmark.py data/scifact.json --k 5 --dense-model sentence-transformers/all-MiniLM-L6-v2 --dense-revision 1110a243fdf4706b3f48f1d95db1a4f5529b4d41 --output runs/scifact-minilm
```

| Method | Recall@5 | Precision@5 | Full-ranking MRR |
|---|---:|---:|---:|
| BM25 | 0.72594 | 0.15733 | 0.63182 |
| Pretrained MiniLM | 0.73794 | 0.16400 | 0.61130 |

Both use 5,183 documents and 300 test queries; no parameters were tuned on these test judgments. The embedding model is pretrained third-party work, credited in its model card.

## Recorded command definitions

### checks

```text
{python} smoke_test.py
```

### lexical-benchmark

```text
{python} benchmark.py {input:dataset} --output {output}/retrieval
```

`{python}` is the current interpreter. `{output}` is the new run directory. `{input:name}` refers to a named absolute input path supplied to the driver. Install declared dependencies in a clean environment before executing. Never execute untrusted serialized models or notebooks.
