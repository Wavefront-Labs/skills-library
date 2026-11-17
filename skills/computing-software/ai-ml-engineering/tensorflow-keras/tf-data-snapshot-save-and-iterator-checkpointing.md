---
id: computing-software.ai-ml-engineering.tensorflow-keras.tf-data-snapshot-save-and-iterator-checkpointing
name: tf-data-snapshot-save-and-iterator-checkpointing
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow-keras, dataset-snapshot, tf-data, dataset-save, iterator-checkpoint, preprocessing-cache]
level: practitioner
status: gated
description: "Persist expensive tf.data preprocessing with Dataset.save/load and snapshot, and checkpoint iterator position with tf.train.Checkpoint to resume mid-epoch."
sources:
  - https://www.tensorflow.org/api_docs/python/tf/data/Dataset#save
  - https://www.tensorflow.org/api_docs/python/tf/data/Dataset#snapshot
  - https://www.tensorflow.org/guide/data#iterator_checkpointing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dataset save / snapshot and iterator checkpointing

## When preprocessing is the bottleneck
If decoding, augmentation-free transforms or tokenisation dominate and repeat identically every epoch, compute once and reuse.

| Tool | Scope | Notes |
|---|---|---|
| `ds.cache()` | memory | data must fit in RAM; lost when process ends |
| `ds.cache("/local/cache")` | local files | per process, rebuilt if file missing; not shareable |
| `ds.save(path)` / `tf.data.Dataset.load(path)` | files, explicit | write once, reuse across jobs |
| `ds.snapshot(path)` | files, automatic | writes on first run, reads afterwards; fingerprinted |

## save / load
```python
ds = raw.map(decode_and_resize, num_parallel_calls=tf.data.AUTOTUNE)
ds.save("gs://bucket/preproc/v3", compression="GZIP", shard_func=lambda x, y: tf.random.uniform([], 0, 16, tf.int64))
train = tf.data.Dataset.load("gs://bucket/preproc/v3", compression="GZIP")
train = train.shuffle(10000).map(augment, num_parallel_calls=tf.data.AUTOTUNE).batch(64).prefetch(tf.data.AUTOTUNE)
```
- Put random augmentation **after** load, otherwise every epoch sees the same augmentations.
- Ran with a local path and `compression="GZIP"` plus a `shard_func` returning `tf.random.uniform([], 0, 4, tf.int64)`: `save` wrote a directory with `dataset_spec.pb`, `snapshot.metadata` and one subdirectory; `Dataset.load(path, compression="GZIP")` returned 20 elements with the same `element_spec`. The `gs://` path was not run. Version the path when preprocessing code changes.

## snapshot
```python
ds = raw.map(expensive).snapshot("/fast/snap", compression="AUTO").shuffle(...).batch(...)
```
Ran with a local path: the first pass wrote a fingerprint-named subdirectory (`snap/<hash>`) and the second pass read from it. That the fingerprint covers the upstream graph, and that partial snapshots are ignored and rewritten, comes from the `Dataset.snapshot` docs and was not tested (gated: unconfirmed, source is paywalled or blocked).

## Iterator checkpointing
```python
it = iter(train_ds)
ckpt = tf.train.Checkpoint(step=step, model=model, optimizer=opt, iterator=it)
manager = tf.train.CheckpointManager(ckpt, "ckpts", max_to_keep=3)
manager.save()            # stores iterator position (and shuffle buffer contents)
ckpt.restore(manager.latest_checkpoint)
# ran: a shuffled, batched range(100) dataset resumed after 3 batches produced the same next 2 batches
```
- Keras `fit` does not checkpoint the iterator; use `keras.callbacks.BackupAndRestore` for epoch-level resume, or a custom loop for mid-epoch.
- Shuffle buffers are saved in the checkpoint, so a large buffer of images makes checkpoints large (size not measured here). Use small buffers or shuffle at file level instead.
- Not all transformations are checkpointable: `from_generator` raised `FailedPreconditionError: PyFunc is stateful` and a `map(tf.py_function(...))` pipeline raised `EagerPyFunc is stateful` at save (ran).
- `tf.data.Options().experimental_symbolic_checkpoint = True` exists in TF 2.21 (ran: attribute set); its buffer-saving effect and the TF version that introduced it were not checked (gated: unconfirmed, source is paywalled or blocked).

## Verify
Time one epoch before and after (`tf.data` throughput only: iterate without the model); restore from checkpoint and confirm the next batch matches what an uninterrupted run would produce (with fixed seeds).
