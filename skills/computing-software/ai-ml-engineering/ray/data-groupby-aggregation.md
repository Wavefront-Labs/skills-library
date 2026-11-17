---
id: computing-software.ai-ml-engineering.ray.data-groupby-aggregation
name: data-groupby-aggregation
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, ray-data-groupby, aggregate, groupby-map-groups, sort-limit]
level: practitioner
status: docs-checked
description: "Aggregate Ray Data with groupby, Count/Sum/Mean aggregation objects, map_groups, sort, unique and whole-dataset aggregates."
sources:
  - https://docs.ray.io/en/latest/data/aggregating-data.html
  - https://docs.ray.io/en/latest/data/api/grouped_data.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Groupby and aggregation

```python
import ray
from ray.data.aggregate import Count, Mean, Sum

ds = ray.data.range(100).add_column("group_key", lambda x: x["id"].to_numpy() % 3)

ds.max("id")                                         # direct method on a Dataset
ds.groupby("group_key").min("id")                    # [{'group_key': 0, 'min(id)': 0}, ...]
ds.aggregate(Count())                                # {'count()': 100}
ds.groupby("group_key").aggregate(Mean(on="id"), Sum(on="id")).take_all()
ds.sort("id", descending=True).limit(10)
ds.unique("group_key")
```
`ds.groupby("k").map_groups(fn, batch_format="pandas")` applies `fn` to each whole group.

## Facts from the docs and API source
- Built-ins (`max`, `min`, `sum`, `mean`...) work on a Dataset or on GroupedData. Each has an `AggregateFnV2` object (`Count`, `Sum`, `Mean`, `Min`, `Max`, `Std`, `Unique`...) that you pass to `Dataset.aggregate()` or `groupby(...).aggregate()`.
- Result column names are generated from the aggregation, such as `count()`, `count(id)`, `sum(col)`, `mean(id)`; pass `alias_name` to the aggregation object to rename.
- `ignore_nulls` defaults to True for Sum, Min, Max and Mean; `Dataset.unique` defaults to `ignore_nulls=False`.
- `Dataset.aggregate` returns one dict; `groupby(None)` is the whole-dataset group.
- Grouping hash-shuffles the dataset by key. When the data is far larger than the cluster's object-store memory, the API docs suggest disk-based shuffle (`DataContext.use_disk_based_hash_shuffle = True` or env `RAY_DATA_ENABLE_DISK_SHUFFLE=1`).
- `map_groups` needs each group to fit in memory on one node and may be slower than specific aggregations; the docs prefer `aggregate()`.
- `sort(key, descending=False)` requires a key and takes optional `boundaries`.

## Verify
Compare a small sample against pandas: `ds.limit(1000).to_pandas().groupby(...)`.

## Checked
2026-11-03. Confirmed in Ray repo docs `data/aggregating-data.md` and `python/ray/data/dataset.py`, `grouped_data.py`, `aggregate.py`. Removed: expected output with invented figures, "stragglers" and "OOM" speculation, claim that sort costs a sample pass, `target_shuffle_buffer_size` advice (marked confirm), `top_n` example.
Method: documentation only; no commands were run.
