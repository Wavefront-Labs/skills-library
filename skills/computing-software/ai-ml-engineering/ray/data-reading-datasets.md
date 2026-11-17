---
id: computing-software.ai-ml-engineering.ray.data-reading-datasets
name: data-reading-datasets
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, ray-data-read, read-parquet, read-csv, from-items]
level: practitioner
status: docs-checked
description: "Load data into Ray Data with read_parquet, read_csv, read_images, read_json, from_pandas, from_items, override_num_blocks and column pruning."
sources:
  - https://docs.ray.io/en/latest/data/loading-data.html
  - https://docs.ray.io/en/latest/data/performance-tips.html
  - https://docs.ray.io/en/latest/data/api/input_output.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading datasets

```python
import ray
from ray.data.expressions import col, lit

ds = ray.data.read_parquet("<URI>/events/", columns=["user", "ts"])      # projection pushdown
ds = (ray.data.read_parquet("<URI>/iris.parquet")
        .filter(expr=col("sepal.length") > lit(5.0))                     # filter + select pushed to the scan
        .select_columns(["sepal.length", "variety"]))
ds = ray.data.read_csv("<URI>/iris.csv")
ds = ray.data.read_images("<URI>/imgs/", mode="RGB", size=(224, 224))
ds = ray.data.read_json("<URI>/logs.jsonl")
ds = ray.data.from_pandas(df)                      # in-memory pandas frame
ds = ray.data.from_items([{"x": i} for i in range(1000)])   # list of dicts, each a row
ds = ray.data.range(10**6)
print(ds.schema(), ds.count(), ds.take(3))
```
Tuning: `ray.data.read_parquet(path, override_num_blocks=200)` and `num_cpus=0.25`.

## Facts from the docs and API source
- `read_parquet` reads all columns unless you pass `columns=` or call `select_columns` afterwards; both push the projection into the file scan. The API docs also show `filter(expr=...)` pushed to the scan.
- Block count: by default Ray Data picks it dynamically from input size and resources. `override_num_blocks` sets the number of output blocks, equal to the number of read tasks; a following `map_batches` is usually fused with the read, so it also sets map tasks. The `parallelism` argument is deprecated in favour of `override_num_blocks`.
- Each read task requests 1 CPU by default; `read_parquet(path, num_cpus=0.25)` allows four read tasks per CPU.
- Remote storage: authenticate every node, then use URIs for buckets, folders or objects. Credentials go through PyArrow filesystems; pass `filesystem=` (for example a gcsfs or adlfs filesystem) for other backends. A shared local filesystem must be mounted at the same path on every node; the `local://` scheme is deprecated.
- `ds.materialize()` executes and holds the dataset in memory (returns a `MaterializedDataset`).

## Verify
`ds.schema()` shows the expected columns and `ds.count()` matches the source.

## Checked
2026-11-03. Confirmed in Ray repo docs `data/loading-data.md`, `data/performance-tips.md` and `python/ray/data/read_api.py`. Fixed: a `filter=` argument on `read_parquet` (marked confirm) does not exist in the signature; row filtering is `Dataset.filter(expr=...)`. Removed: small-file overhead claim, lazy execution claim, `from_pandas` object-store advice, concrete bucket names.
Method: documentation only; no commands were run.
