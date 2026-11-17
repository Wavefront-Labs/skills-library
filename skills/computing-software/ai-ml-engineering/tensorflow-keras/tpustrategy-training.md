---
id: computing-software.ai-ml-engineering.tensorflow-keras.tpustrategy-training
name: tpustrategy-training
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow, keras, tpustrategy, tpu, cloud-tpu, xla]
level: practitioner
status: docs-checked
description: "Train on Cloud TPUs with tf.distribute.TPUStrategy: resolver setup, static shapes and drop_remainder, steps_per_execution, GCS data and bfloat16."
sources:
  - https://www.tensorflow.org/guide/tpu
  - https://www.tensorflow.org/guide/mixed_precision
  - https://github.com/openxla/xla/blob/main/docs/tf2xla/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TPUStrategy training

## Connect
```python
resolver = tf.distribute.cluster_resolver.TPUClusterResolver(tpu="local")   # "local" is the Colab address; on GCE pass your Cloud TPU name
tf.config.experimental_connect_to_cluster(resolver)
tf.tpu.experimental.initialize_tpu_system(resolver)
strategy = tf.distribute.TPUStrategy(resolver)
print(strategy.num_replicas_in_sync)      # number of TPU cores
```
The TPU initialisation code has to be at the beginning of the program. With TPU Nodes all data files read by the `Dataset` must be in Google Cloud Storage buckets; with TPU VMs you can store data wherever you like.

## Model and compile
```python
keras.mixed_precision.set_global_policy("mixed_bfloat16")    # all Cloud TPUs support bfloat16
with strategy.scope():
    model = build_model()
    model.compile(optimizer="adam", loss=..., metrics=[...], steps_per_execution=64)
```
`steps_per_execution` reduces Python overhead; the TPU guide's example reports about 50% higher throughput with it. When it is greater than 1, pass `validation_steps` to `fit` and make sure the validation data yields at least that many full batches, otherwise TPU replicas can hang on EOF.

## Input pipeline
```python
ds = (tf.data.TFRecordDataset(tf.io.gfile.glob("gs://bucket/train-*.tfrec"), num_parallel_reads=tf.data.AUTOTUNE)
      .map(parse, num_parallel_calls=tf.data.AUTOTUNE)
      .shuffle(10_000).batch(GLOBAL_BATCH, drop_remainder=True).prefetch(tf.data.AUTOTUNE))
```
- **Static shapes**: use `drop_remainder=True` when batching, as the TPU guide does, and pad variable-length sequences to fixed lengths or a few buckets; XLA recompiles when input shapes change.
- For most cases the guide recommends converting data to TFRecord and reading it with `tf.data.TFRecordDataset` (not a hard requirement).

## Performance checks
- TPUs benefit from certain dimensions being multiples of 128 (TensorFlow mixed precision guide).

## Saving
Save to Cloud Storage with `model.save("gs://bucket/model.keras")`.

## Verify
First epoch is slow (compilation); later epochs should show stable step times. Compare loss curves with a small GPU run at the same effective batch.

## Checked

Checked 2026-10-25 against tensorflow/docs master of 2026-10-20 and openxla/xla main (2026-10). Confirmed `TPUClusterResolver`, `tf.config.experimental_connect_to_cluster`, `tf.tpu.experimental.initialize_tpu_system`, `TPUStrategy`, initialisation at the start of the program, the TPU Nodes versus TPU VMs storage rule, TFRecord with `drop_remainder=True`, `steps_per_execution` (about 50% throughput gain in the example) and the `validation_steps` warning, running several steps in a `tf.function` with `tf.range` (TPU guide), bfloat16 support on all Cloud TPUs and the multiples-of-128 note (mixed precision guide), and XLA recompilation on shape changes (XLA guide). The Google Cloud TPU pages cited previously are not in a public repository and were not read; removed the claims that depended on them (TPU VM creation flags, per-core batch sizes, op support lists, profiler terms).

Method: documentation only; no commands were run.
