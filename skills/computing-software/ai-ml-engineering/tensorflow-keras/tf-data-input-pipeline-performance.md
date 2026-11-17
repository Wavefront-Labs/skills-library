---
id: computing-software.ai-ml-engineering.tensorflow-keras.tf-data-input-pipeline-performance
name: tf-data-input-pipeline-performance
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow, tf-data, keras, input-pipeline, prefetch, autotune, tfrecord, performance, gpu-utilization, dataset-cache, parallel-map, data-loading-bottleneck]
level: advanced
status: gated
description: "Build a tf.data input pipeline that keeps the GPU fed: parallel map, prefetch/AUTOTUNE, TFRecord vs on-the-fly decoding, and diagnosing a CPU-bound training loop."
sources:
  - https://www.tensorflow.org/guide/data_performance
  - https://www.tensorflow.org/tutorials/load_data/tfrecord
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tf.data input pipeline performance — keeping the GPU fed

**Goal:** build a `tf.data.Dataset` pipeline whose CPU-side work (reading, decoding, augmenting) overlaps with GPU compute instead of serializing in front of it, which is the most common reason a Keras training job under-utilizes an expensive GPU.

## 1. The pipeline shape that overlaps, not serializes
```python
ds = tf.data.Dataset.list_files(pattern)
ds = ds.interleave(tf.data.TFRecordDataset, cycle_length=8, num_parallel_calls=tf.data.AUTOTUNE)
ds = ds.map(parse_and_augment, num_parallel_calls=tf.data.AUTOTUNE)
ds = ds.shuffle(buffer_size=10_000)
ds = ds.batch(batch_size)
ds = ds.prefetch(tf.data.AUTOTUNE)
```
- **End the pipeline with `.prefetch(tf.data.AUTOTUNE)`**: it lets `tf.data` prepare future batches while the model trains on the current one. Caveat measured on TF 2.21 (CPU, a 50 ms `py_function` map and a 50 ms consumer step, 20-30 steps): with no explicit prefetch the loop took 1.06 s for 20 steps, whereas iterating the dataset alone took 1.03 s and the consumer sleeps alone 1.0 s (a serial pipeline would take about 2 s), so the work already overlapped, because `tf.data.Options().experimental_optimization.inject_prefetch` defaults to True ("Whether to inject prefetch transformation as the last transformation when the last transformation is a synchronous transformation", from the TF source). Explicit `prefetch` is still the way to set the buffer and is harmless; do not assume a missing `prefetch` is the cause of low GPU utilization without profiling. GPU utilisation itself was not measured here (gated: unconfirmed, source is paywalled or blocked).
- `num_parallel_calls=tf.data.AUTOTUNE` on `.map()` and `.interleave()` lets TensorFlow pick parallelism dynamically based on available CPU and observed throughput — prefer this over a hardcoded worker count unless you've benchmarked a specific fixed value doing better (rare).
- Order matters: `.shuffle` before `.batch` shuffles individual examples (ran on `range(12)`: `[[4, 9, 3, 8], [5, 2, 7, 0], [1, 6, 11, 10]]`); `.batch` before `.shuffle` only shuffles the order of whole batches, leaving each batch's composition fixed (ran: `[[4,5,6,7],[8,9,10,11],[0,1,2,3]]`) - a subtle bug that doesn't error, just weakens shuffling.
- `.cache()` (in-memory or to a file) after a map step that's expensive but produces the same result every epoch (static preprocessing, not random augmentation) avoids redoing that work every epoch — do **not** cache after a step containing random augmentation, or every epoch replays the exact same "random" augmentation from epoch 1 (ran: `map(tf.random.uniform).cache()` gave `[0.8, 0.265, 0.47]` on both passes; without `cache` the passes differed).

## 2. TFRecord vs on-the-fly decoding
- Decoding raw images/files (JPEG decode, CSV parse) on every read can become the bottleneck at scale, especially with many small files on networked/cloud storage where per-file open overhead dominates; **TFRecord** (TensorFlow's binary serialization format) packs many examples into fewer, larger files (a TFRecord writer, `interleave` over GZIP shards and `TFRecordDataset` all ran in the sharding test). The cloud-storage cost claim was not measured (gated: unconfirmed, source is paywalled or blocked).
- Converting to TFRecord is a one-time preprocessing cost; worth it once (a) the dataset is reused across many training runs/experiments, or (b) profiling shows I/O (not compute) is the bottleneck — don't reach for it reflexively on a dataset that already trains with high GPU utilization from plain file reads.
- `tf.data.experimental.service` (it exists in TF 2.21; not run here) can offload the entire input pipeline to separate machines/processes when the preprocessing itself (not just I/O) is too CPU-heavy for the training machine's spare cores — a more advanced step, worth it only once vertical scaling (just adding parallel calls on the training machine) is exhausted.

## 3. Diagnosing where the bottleneck actually is
- Simplest: time just the dataset iteration alone (`for _ in ds: pass`, no model call) versus the full training step; if iterating the dataset alone is already slow, the bottleneck is the input pipeline, not the model/GPU (ran: 20 elements took 1.03 s alone for a 50 ms-per-element map).
- TensorBoard's **Profiler** (`tf.profiler` trace, viewed as the "Input Pipeline Analyzer"; not run here (gated: unconfirmed, source is paywalled or blocked)) reports the percentage of step time spent waiting on input versus computing — use this instead of guessing from GPU utilization percentage alone, since GPU utilization dips from input-starvation and from a genuinely small/fast model look identical without the profiler's breakdown.
- A pipeline that's fast in isolation but slow when combined with the model (e.g. training fine for a few steps then stalling) often points to a `.shuffle` buffer that's too large for available memory causing swapping, or a `.cache()` to disk contending with checkpoint I/O on the same volume — check memory and disk I/O, not just CPU, when a pipeline degrades only over a long run.

## Verify
- [ ] `.prefetch(tf.data.AUTOTUNE)` is the last stage of the pipeline.
- [ ] `.shuffle()` is called before `.batch()`, not after.
- [ ] `.cache()` is placed only after deterministic (non-augmentation) steps, if used at all.
- [ ] Measured: dataset-iteration-only time vs full-training-step time, to confirm whether input or compute is actually the bottleneck.
- [ ] TensorBoard Profiler's input-pipeline breakdown checked before concluding the GPU itself needs upgrading.
- [ ] TFRecord conversion considered only after profiling shows I/O (not compute) is the limiting factor.
