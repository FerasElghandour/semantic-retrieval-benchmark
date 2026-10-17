# Input contract

For the CLI, provide a JSON array of document strings. BM25 returns zero-based document indices. evaluate accepts query-to-ranked-index mappings and query-to-positive-relevance dictionaries. SemanticIndex additionally requires sentence-transformers and an independently obtained model identifier authorized for your use. No corpus, query text, embedding store, or model weights are bundled. Historical scores refer to the earlier reduced-corpus study, not this portable index.
