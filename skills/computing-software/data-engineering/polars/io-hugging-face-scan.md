---
id: computing-software.data-engineering.polars.io-hugging-face-scan
name: io-hugging-face-scan
category: computing-software
field: data-engineering
product: polars
tags: [polars, io, hugging-face, hf-path, scan-parquet, scan-csv, hf-token, polars-io-hugging-face]
level: practitioner
status: docs-checked
description: "Scan Hugging Face datasets and spaces from Polars with hf:// paths (bucket, repository, revision, glob) and authenticate private repos with a token."
sources:
  - https://docs.pola.rs/user-guide/io/hugging-face/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: read datasets hosted on Hugging Face directly with Polars.

All cloud-enabled scan functions and their `read_` counterparts support Hugging Face: `scan_parquet`/`read_parquet`, `scan_csv`/`read_csv`, `scan_ndjson`/`read_ndjson`, `scan_ipc`/`read_ipc`.

Path format
`hf://BUCKET/REPOSITORY@REVISION/PATH`
- `BUCKET`: `datasets` or `spaces`.
- `REPOSITORY`: usually `username/repo_name`.
- `REVISION`: branch or commit name; optional, defaults to `main`. A branch is given by appending `@branch` to the repository.
- `PATH`: a file, directory or glob from the repository root.

Examples from the page
- `hf://datasets/nameexhaustion/polars-docs/iris.csv` (branch main, file iris.csv)
- `hf://datasets/nameexhaustion/polars-docs@foods/*.csv` (branch foods, glob)
- `hf://datasets/nameexhaustion/polars-docs/hive_dates/` (directory)
- `hf://spaces/nameexhaustion/polars-docs/orders.feather` (spaces bucket)

```python
pl.scan_csv("hf://datasets/nameexhaustion/polars-docs/iris.csv").collect()
pl.scan_ndjson("hf://datasets/nameexhaustion/polars-docs/iris.jsonl").collect()
pl.scan_parquet("hf://datasets/nameexhaustion/polars-docs/hive_dates/").collect()
pl.scan_ipc("hf://spaces/nameexhaustion/polars-docs/orders.feather").collect()
```
The iris CSV example returns shape (150, 5) with columns sepal_length, sepal_width, petal_length, petal_width, species; the hive_dates directory returns shape (4, 3) with columns date1 (date), date2 (datetime[us]) and x (i32); the orders.feather IPC example returns shape (10, 9) with TPC-H style o_* columns.
Because `hf://` is a cloud-enabled path, the `read_*` counterpart works the same way when you want an eager DataFrame, for example `pl.read_csv("hf://datasets/nameexhaustion/polars-docs/iris.csv")` (same path, `read_` instead of `scan_`).

Authentication for private locations (either):
- `scan_parquet(..., storage_options={'token': '<your HF token>'})`
- environment variable `HF_TOKEN`, e.g. `export HF_TOKEN=<your HF token>`

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). Removed or trimmed claims the cited page does not confirm.

Method: documentation only; no commands were run.
