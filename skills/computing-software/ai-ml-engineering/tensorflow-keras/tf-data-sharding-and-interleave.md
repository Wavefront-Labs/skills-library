---
id: computing-software.ai-ml-engineering.tensorflow-keras.tf-data-sharding-and-interleave
name: tf-data-sharding-and-interleave
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow, tf-data, dataset-interleave, dataset-sharding, auto-shard-policy, list-files, input-pipeline]
level: practitioner
status: gated
description: "Read thousands of files with tf.data efficiently: list_files, parallel interleave, deterministic flag, and file vs data sharding for multi-worker training."
sources:
  - https://www.tensorflow.org/guide/data_performance
  - https://www.tensorflow.org/api_docs/python/tf/data/Dataset#interleave
  - https://www.tensorflow.org/tutorials/distribute/input
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tf.data sharding and interleave

**Goal:** saturate the accelerator when training data is spread across many TFRecord/Parquet shards, and give each worker a distinct slice.

## Parallel interleave over files
```python
AUTOTUNE = tf.data.AUTOTUNE
files = tf.data.Dataset.list_files("gs://bucket/train-*.tfrecord", shuffle=True, seed=42)
ds = files.interleave(
    lambda f: tf.data.TFRecordDataset(f, compression_type="GZIP"),
    cycle_length=16,                 # files read concurrently
    block_length=1,                  # records taken from each before moving on
    num_parallel_calls=AUTOTUNE,
    deterministic=False,             # allow out-of-order for throughput
)
ds = ds.shuffle(10_000).map(parse_fn, num_parallel_calls=AUTOTUNE).batch(256).prefetch(AUTOTUNE)
```
- `cycle_length` controls how many files are open at once; reading 1 file at a time from object storage is the most common input bottleneck.
- `deterministic=False` (or `options.deterministic = False`; both ran) lets fast files overtake slow ones. Keep it True when you need reproducible order (ran: `deterministic=True`, `cycle_length=2` over 2 files gave `0-0, 1-0, 0-1, 1-1, 0-2, 1-2`).
- `list_files(shuffle=True)` reshuffles file order each pass (ran: two passes over 4 files gave different orders); combine with a record-level `shuffle` buffer for proper mixing. A shuffle buffer smaller than one file means each batch comes mostly from one file.
- Shard size: the common advice is files large enough that open latency is amortised, but the exact target size was not checked against the tf.data performance guide (gated: unconfirmed, source is paywalled or blocked).

## Manual sharding
```python
ds = files.shard(num_shards=num_workers, index=worker_index)   # BEFORE reading
```
Shard at the file level, before `interleave` (ran: `list_files(shuffle=False).shard(2, 1)` returned `train-1`, `train-3`). Sharding after reading (`ds.shard` on records) makes every worker read every file and drop most of it.

## Auto-sharding with tf.distribute
With `MultiWorkerMirroredStrategy` (not run here), datasets passed to `fit` or `experimental_distribute_dataset` are auto-sharded:
```python
opts = tf.data.Options()
opts.experimental_distribute.auto_shard_policy = tf.data.experimental.AutoShardPolicy.FILE
ds = ds.with_options(opts)
```
- Policies in TF 2.21 (`list(AutoShardPolicy)`): `OFF, AUTO, FILE, DATA, HINT`. From the enum docstring: `FILE` shards by input files and "make sure that there is at least as many files as workers. If there are fewer input files than workers, a runtime error will be raised" (an error, not a hang); `DATA` has every worker process the whole dataset and discard the rest, and needs a deterministic element order to partition correctly; `AUTO` attempts FILE then falls back to DATA; `OFF` does no sharding, e.g. when you shard yourself (`distribute_datasets_from_function` with `input_context.input_pipeline_id`); `HINT` replaces a `shard(SHARD_HINT, ...)` placeholder with `shard(num_workers, worker_index)`.
- `with_options` with `auto_shard_policy = FILE` ran on a single process; multi-worker behaviour, including uneven file sizes giving workers different epoch lengths and the `repeat()` plus `steps_per_epoch` remedy, was not run (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] Profiler no longer reports the step as input-bound.
- [ ] Number of files >= number of workers x reasonable cycle_length.
- [ ] Each worker reads distinct files (log the file names per worker for one epoch).
