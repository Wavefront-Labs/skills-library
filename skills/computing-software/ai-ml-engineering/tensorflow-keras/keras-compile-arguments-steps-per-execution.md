---
id: computing-software.ai-ml-engineering.tensorflow-keras.keras-compile-arguments-steps-per-execution
name: keras-compile-arguments-steps-per-execution
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow-keras, model-compile, steps-per-execution, jit-compile, loss-weights, keras-metrics]
level: practitioner
status: verified
description: "Configure Keras compile() fully: losses and loss_weights for multi-output, metrics per output, steps_per_execution for small steps, jit_compile and run_eagerly for debugging."
sources:
  - https://keras.io/api/models/model_training_apis/
  - https://keras.io/guides/training_with_built_in_methods/
  - https://www.tensorflow.org/guide/keras/training_with_built_in_methods
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# compile() arguments

**Goal:** set up `fit()` so it computes the right losses/metrics and runs fast.

## Full signature (Keras 3)
```python
model.compile(
    optimizer=keras.optimizers.AdamW(learning_rate=1e-3, weight_decay=1e-4),
    loss={"cls": keras.losses.SparseCategoricalCrossentropy(from_logits=True),
          "box": keras.losses.Huber()},
    loss_weights={"cls": 1.0, "box": 0.5},
    metrics={"cls": ["accuracy"], "box": [keras.metrics.MeanAbsoluteError()]},
    weighted_metrics=None,
    run_eagerly=False,
    steps_per_execution=32,
    jit_compile="auto",
)
```
- Dict keys must match output layer names or output dict keys (ran with a model whose outputs were a dict `{"cls": ..., "box": ...}`; the full call above ran on Keras 3.15).
- `from_logits=True` when the last layer has no softmax/sigmoid (preferred for numerical stability).
- Sparse vs categorical crossentropy: integer labels vs one-hot.

## steps_per_execution
Runs N batches inside one compiled function call, cutting per-step Python/host overhead; the Keras docs say it can greatly improve performance on TPUs or small models with large Python overhead, runs at most one epoch per execution, and is not supported on the PyTorch backend. Callbacks' `on_batch_*` then fire every N batches (ran with 256 samples, batch 8: `steps_per_execution=1` gave batch indices 0..31, `=8` gave `[7, 15, 23, 31]`). Try values like 8 or 32 and measure.

## jit_compile
- `"auto"` (default): on the JAX and TensorFlow backends XLA is enabled if the model supports it and disabled otherwise; on the torch backend `"auto"` means eager and `True` uses `torch.compile` with inductor (Keras docs).
- `jit_compile=False` if a layer is XLA-incompatible (some string ops, dynamic shapes).

## run_eagerly
`run_eagerly=True` runs Python line by line so you can set breakpoints and print tensors. Much slower; only for debugging.

## weighted_metrics
Metrics that should respect `sample_weight`/`class_weight` go in `weighted_metrics`; plain `metrics` ignore weights.

## Verify
- [ ] History keys show every output's loss and metrics (ran the signature above with a dict-output model: `box_loss, box_mean_absolute_error, cls_accuracy, cls_loss, loss`; `model.metrics_names` was only `['loss', 'compile_metrics', 'cls_loss', 'box_loss']` in Keras 3.15, so read the history keys instead).
- [ ] Compare step time with `steps_per_execution=1` vs 32 on the real hardware.
