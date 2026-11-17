---
id: computing-software.ai-ml-engineering.tensorflow-keras.keras-evaluate-predict-performance
name: keras-evaluate-predict-performance
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow-keras, keras-predict, predict-on-batch, inference-performance, model-evaluate, keras]
level: practitioner
status: verified
description: "Make Keras evaluate and predict fast and correct: batch_size, steps, predict vs __call__ vs predict_on_batch, memory growth over loops, and exporting for serving."
sources:
  - https://keras.io/api/models/model_training_apis/#predict-method
  - https://keras.io/getting_started/faq/#whats-the-difference-between-model-methods-predict-and-call
  - https://www.tensorflow.org/guide/keras/training_with_built_in_methods
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# evaluate / predict performance

## Which call to use
| Call | Best for | Notes |
|---|---|---|
| `model.predict(x, batch_size=256)` | large arrays or datasets | batches, compiled loop, returns NumPy (ran: `numpy.ndarray`); overhead per call is high |
| `model(x, training=False)` | small inputs in a loop, inside tf.function | returns tensors (ran: `EagerTensor`), no batching, minimal overhead |
| `model.predict_on_batch(x)` | one batch, NumPy out | no batching, uses compiled predict function |
| `model.evaluate(ds)` | metrics over a dataset | uses compiled loss/metrics from `compile` |

Calling `predict()` in a tight loop on single samples is a classic slowdown (per-call setup cost; measure on your model): use `model(x, training=False)` or batch the inputs.

## Throughput settings
- `batch_size` for predict can be larger than for training (no gradients, no optimizer state); raise it until memory or throughput stops improving.
- Feed a `tf.data.Dataset` with `.batch().prefetch(tf.data.AUTOTUNE)`; pass `steps` only when the dataset is infinite.
- `steps_per_execution=N` reduces per-batch Python overhead for small models (Keras docs); `jit_compile` is a `compile` argument that Keras documents for XLA, measure whether it helps predict.
- With a mixed precision policy, outputs are float16/bfloat16 unless the last layer is float32 (keep `dtype="float32"` on the output layer). Speed-ups depend on GPU hardware, which was not tested here.

## Correctness
- Dropout/BatchNorm: `predict` and `evaluate` run with `training=False` automatically; when calling `model(x)` pass `training=False` explicitly.
- Keras metrics are stateful and accumulate over the whole epoch (ran: a custom F1 matched sklearn's F1 on `predict` outputs to 6 digits), while custom losses with `reduction` quirks may differ from your offline computation. Recompute key metrics with scikit-learn on `predict` outputs to confirm.
- Ordering: `predict` on a shuffled dataset returns predictions in shuffled order, and a `shuffle()` with default `reshuffle_each_iteration` gave a different order on each `predict` call (ran: `[0 1 3 6 5 2 7 4]` then `[7 3 1 5 6 0 2 4]`). Disable shuffle for inference datasets.

## Memory
- `predict` concatenates all outputs in host memory; for huge datasets iterate: `for xb in ds: yb = model(xb, training=False)` and write results incrementally.
- Repeated `fit`/`predict` in a loop creating new models: call `keras.backend.clear_session()` between models.

## Serving path
For a service, export instead of calling Keras per request: `model.export("export_dir")` (ran; writes a SavedModel with a serving signature) for TF Serving, or convert to LiteRT/ONNX. Benchmark p50/p99 latency at realistic batch sizes, not just throughput.
