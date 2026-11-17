---
id: computing-software.ai-ml-engineering.ray.data-writing-and-shuffle
name: data-writing-and-shuffle
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, random-shuffle, write-parquet, repartition, local-shuffle]
level: practitioner
status: docs-checked
description: "Write Ray Data to Parquet/CSV/JSON/images, control output file count with min_rows_per_file and repartition, and shuffle globally or locally."
sources:
  - https://docs.ray.io/en/latest/data/saving-data.html
  - https://docs.ray.io/en/latest/data/shuffling-data.html
  - https://docs.ray.io/en/latest/data/iterating-over-data.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing and shuffling

```python
ds.write_parquet("<URI>/out/", min_rows_per_file=1_000_000)   # a hint, not a strict limit
ds.write_csv("/mnt/shared/out_csv/", min_rows_per_file=75)
ds.write_json("<URI>/out_json/")
ds.write_images("<URI>/imgs/", column="image", file_format="png")
ds.repartition(keys=["city", "year"], num_blocks=4).write_parquet(
    "<URI>/part/", partition_cols=["city", "year"], max_rows_per_file=3)
ds.write_parquet("<URI>/out/", mode="overwrite")              # SaveMode: create, append (default), overwrite, ignore
ds.random_shuffle(seed=123)                    # shuffles all rows, slow
ds.randomize_block_order()                     # shuffles block order only
for batch in ds.iter_batches(batch_size=512, local_shuffle_buffer_size=10_000):
    ...
```

## Facts from the docs and API source
- The number of output files follows the number of blocks. `min_rows_per_file` is a hint: if blocks hold more rows than the value, those rows are written per file.
- Hive-style partitioned writes: repartition by the partition columns first (with an explicit `num_blocks`) so each block holds one partition's rows, then cap with `max_rows_per_file`. Using `min_rows_per_file` together with non-empty `partition_cols` is deprecated (support ends after February 2027 per the guide).
- `write_parquet` has a `mode` argument (SaveMode create/append/overwrite/ignore) and defaults to append. Check the signature of your version before relying on it for other writers.
- Storage: shared local paths must be mounted at the same path on all nodes (the `local://` scheme is deprecated); for cloud URIs authenticate every node; GCS and Azure use a `gcsfs`/`adlfs` filesystem passed as `filesystem=`.
- Shuffle options: `random_shuffle` (all rows, slow), `randomize_block_order` (cheap but Ray Data must materialize all blocks in memory first), `repartition(keys=..., num_blocks=...)` (key-based hash shuffle, Ray 2.46+) and `local_shuffle_buffer_size` while iterating (not a true global shuffle but faster; use the smallest value that gives enough randomness).
- `repartition(num_blocks)` without `shuffle` splits and combines blocks to minimise data movement; with `shuffle=True` it does a full shuffle.

## Verify
List the output location for the expected number of files and compare `read_parquet(...).count()` with the source.

## Checked
2026-11-03. Confirmed in Ray repo docs `data/saving-data.md`, `shuffling-data.md`, `iterating-over-data.md` and `Dataset` docstrings in `python/ray/data/dataset.py`. Removed: unverified `num_rows_per_file` recommendation, partial-write and staging-prefix advice, network cost claim, "default may be metadata-only" claim, `write_datasink(MyDatasink())` example.
Method: documentation only; no commands were run.
