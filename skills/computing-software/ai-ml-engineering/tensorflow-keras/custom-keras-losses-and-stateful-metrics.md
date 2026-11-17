---
id: computing-software.ai-ml-engineering.tensorflow-keras.custom-keras-losses-and-stateful-metrics
name: custom-keras-losses-and-stateful-metrics
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow, keras, custom-keras-metric, custom-loss, stateful-metric, reduction]
level: practitioner
status: verified
description: "Write Keras custom losses (functions or Loss subclasses) and stateful Metric subclasses with update_state, result and reset_state, including masking and sample weights."
sources:
  - https://keras.io/api/losses/
  - https://keras.io/api/metrics/
  - https://keras.io/guides/training_with_built_in_methods/#custom-losses
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom losses and stateful metrics

## Losses
Simple function (per-sample loss; Keras reduces):
```python
def huber_like(y_true, y_pred, delta=1.0):
    err = y_pred - y_true
    a = keras.ops.abs(err)
    return keras.ops.mean(keras.ops.where(a < delta, 0.5 * err**2, delta * (a - 0.5 * delta)), axis=-1)
```
Configurable and serialisable:
```python
@keras.saving.register_keras_serializable()
class FocalLoss(keras.losses.Loss):
    def __init__(self, gamma=2.0, name="focal", **kw):
        super().__init__(name=name, **kw); self.gamma = gamma
    def call(self, y_true, y_pred):                         # y_pred = probabilities
        y_pred = keras.ops.clip(y_pred, 1e-7, 1 - 1e-7)
        ce = -y_true * keras.ops.log(y_pred)
        return keras.ops.sum(((1 - y_pred) ** self.gamma) * ce, axis=-1)
    def get_config(self): return {**super().get_config(), "gamma": self.gamma}
```
- Return one value per sample (shape `(batch,)` or `(batch, ...)`); Keras applies `sample_weight` and the reduction (`sum_over_batch_size` default). Returning a scalar mean means weights cannot act per sample: with weights `[1,0,0,0,0,0]` the per-sample loss gave 0.140 while the scalar loss gave 0.292 (the scalar scaled by the mean weight 1/6), so the zero-weighted samples still counted.
- Prefer logits plus `from_logits=True`-style math for numerical stability over clipping probabilities.
- Losses that need extra inputs (e.g. a mask or a second target): pass them as part of `y_true` dict/tuple, or compute inside the model with `self.add_loss()`.

## Stateful metrics
Metrics accumulate across batches; per-batch averaging of a non-additive metric (F1, AUC, precision) is wrong.
```python
@keras.saving.register_keras_serializable()
class F1(keras.metrics.Metric):
    def __init__(self, threshold=0.5, name="f1", **kw):
        super().__init__(name=name, **kw); self.threshold = threshold
        self.tp = self.add_variable(shape=(), initializer="zeros", name="tp")
        self.fp = self.add_variable(shape=(), initializer="zeros", name="fp")
        self.fn = self.add_variable(shape=(), initializer="zeros", name="fn")
    def update_state(self, y_true, y_pred, sample_weight=None):
        y_pred = keras.ops.cast(y_pred > self.threshold, "float32"); y_true = keras.ops.cast(y_true, "float32")
        w = 1.0 if sample_weight is None else keras.ops.cast(sample_weight, "float32")
        self.tp.assign_add(keras.ops.sum(w * y_true * y_pred))
        self.fp.assign_add(keras.ops.sum(w * (1 - y_true) * y_pred))
        self.fn.assign_add(keras.ops.sum(w * y_true * (1 - y_pred)))
    def result(self):
        return 2 * self.tp / (2 * self.tp + self.fp + self.fn + keras.backend.epsilon())
    def reset_state(self):
        for v in (self.tp, self.fp, self.fn): v.assign(0.0)
```
Keras calls `reset_metrics()` (which resets each metric) at the start of each epoch in `fit` and at the start of `evaluate` (Keras 3 TensorFlow trainer source). Built-ins already exist for many: `keras.metrics.F1Score`, `AUC(curve="PR")`, `Precision`, `Recall`, `MeanIoU`.

## Gotchas
- In Keras 3 both `self.add_variable` and `self.add_weight` exist on `Metric` and ran without warnings; legacy tf-keras 2 only has `add_weight`.
- Metrics run on every batch: keep them cheap and on-device.
- `keras.metrics.F1Score` expects 2D `(batch, output_dim)` labels and predictions (1D `y` raised `ValueError`), so reshape binary labels to `(n, 1)`.

## Verify
Compare the metric after `model.evaluate` with sklearn on the full set of predictions (`sklearn.metrics.f1_score`); they should match (ran: the custom F1, built-in `F1Score` and sklearn all gave 0.28374 at threshold 0.5).
