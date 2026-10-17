# Semantic Retrieval Benchmark

**Feras Elghandour** · Technical case study

Compare lexical, static-embedding, and transformer retrieval to quantify the accuracy and indexing-cost trade-off for question answering.

## Implementation

A standalone BM25 implementation, an optional Sentence Transformers index, and macro retrieval metrics.

```mermaid
flowchart LR
    A[Validated inputs] --> B[Portable implementation]
    B --> C[Evaluation and contract checks]
    C --> D[Inspectable results]
```

## Completed study

On the saved 1,600-query test partition, MPNet reports Recall@5 of 0.9606 and MRR of 0.9296, compared with MiniLM MRR 0.8979 and BGE-small MRR 0.9058. MPNet indexing takes 767.8 seconds in the recorded environment versus 110.9 seconds for MiniLM.

These historical figures describe the completed study. This refactored standalone implementation has separate validation and has not been used to recertify the historical benchmark. The public release contains the portable core and focused tests.

## Run locally

Python 3.11 or later.

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python smoke_test.py
python retrieval.py /path/to/documents.json "your question"
```

Prepare your own inputs as described in [DATA.md](DATA.md). Tests use generated fixtures and do not need credentials or provider calls. [VALIDATION.md](VALIDATION.md) records their scope.

## Practical relevance and limitations

The experiment uses a reduced Natural Questions corpus containing judged documents and 1,000 distractors, with 400 validation queries. These scores are not full-corpus BEIR leaderboard results; timings depend on hardware and cache state.

This edition makes the core behavior reusable and inspectable. Historical metrics and synthetic contract tests provide different kinds of evidence; neither establishes client deployment or commercial impact.
