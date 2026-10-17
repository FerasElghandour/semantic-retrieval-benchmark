# Validation

Run `python smoke_test.py` for the included offline behavior checks. These use synthetic inputs or an in-memory database. They do not recertify historical benchmark metrics or test a live external service.

## Executed checks — October 17, 2026

Lexical relevance, empty corpora, duplicated hits, and missing-query metrics passed.

Executed locally on Python 3.14.3. The hosted workflow repeats these checks on Python 3.12.
