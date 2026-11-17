---
id: computing-software.database-administration.duckdb.duckdb-hugging-face-hf-protocol
name: duckdb-hugging-face-hf-protocol
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, httpfs, hugging-face, hf-protocol, datasets, secrets]
level: intro
status: docs-checked
description: "Query Hugging Face datasets from DuckDB with hf:// URLs: globbing, branch or revision selection (@~parquet), local copies, and token secrets."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/core_extensions/httpfs/hugging_face.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: read datasets hosted on Hugging Face directly with SQL.

URL pattern (provided by the `httpfs` extension): `hf://datasets/<username>/<dataset>/<path_to_file>`.

```sql
SELECT * FROM 'hf://datasets/datasets-examples/doc-formats-csv-1/data.csv';
SELECT * FROM 'hf://datasets/datasets-examples/doc-formats-jsonl-1/data.jsonl';
SELECT * FROM 'hf://datasets/datasets-examples/doc-formats-parquet-1/data/train-00000-of-00001.parquet';
```
The page shows CSV, JSONL and Parquet files read this way.

Globs work across a directory:

```sql
SELECT count(*) FROM 'hf://datasets/cais/mmlu/astronomy/*.parquet';   -- 173 in the docs example
```

Revisions: a dataset version is a git-like branch or commit. Append `@<branch>` to the dataset name:

```sql
SELECT * FROM 'hf://datasets/datasets-examples/doc-formats-csv-1@~parquet/**/*.parquet';
```
`~parquet` is a special branch where Hugging Face auto-generates Parquet files for every dataset, to enable efficient scanning.

Avoid hitting the remote endpoint on every query by materializing:

```sql
CREATE TABLE data AS SELECT * FROM 'hf://datasets/datasets-examples/doc-formats-csv-1/data.csv';
```

Private or gated datasets need a token (create one in your Hugging Face account settings) stored as a secret:

```sql
CREATE SECRET hf_token (TYPE huggingface, TOKEN 'your_hf_token');         -- CONFIG provider
CREATE SECRET hf_token (TYPE huggingface, PROVIDER credential_chain);     -- reads the locally cached HF token file
```
For general remote-file behaviour see duckdb-https-remote-files.

## Checked

2026-11-07. Read the Hugging Face Support page in full and confirmed the hf:// URL pattern, the CSV, JSONL and Parquet examples, the local-table CTAS, glob use with the 173 count, revisions as branches or commits with the `~parquet` branch, and the CONFIG and credential_chain secrets (token file under the Hugging Face cache directory). Replaced the claim that the extension selects the reader with what the page shows, reworded the `~parquet` purpose to the page's wording, and removed the PERSISTENT secrets sentence (not on this page) and the Verify step.

Method: documentation only; no commands were run.
