---
id: computing-software.ai-ml-engineering.tensorflow-keras.class-weight-and-sample-weight
name: class-weight-and-sample-weight
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow, keras, keras-class-weight, sample-weight, weighted-metrics, model-fit, class-imbalance]
level: practitioner
status: verified
description: "Weight classes and examples in Keras fit: class_weight dicts, per-sample weights via tf.data, weighted_metrics vs metrics, and limits with multi-output and sequence models."
sources:
  - https://keras.io/api/models/model_training_apis/
  - https://www.tensorflow.org/tutorials/structured_data/imbalanced_data
  - https://keras.io/guides/training_with_built_in_methods/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# class_weight and sample_weight in Keras

**Goal:** make the loss pay more attention to rare classes or trusted examples without breaking metrics or exports.

## class_weight
```python
neg, pos = np.bincount(y_train)
total = neg + pos
class_weight = {0: total / (2 * neg), 1: total / (2 * pos)}   # "balanced" weights
model.fit(train_ds, validation_data=val_ds, epochs=20, class_weight=class_weight)
```
- Keys are integer class indices; for sparse labels they match the label value, for one-hot labels they match the argmax index (ran both). With targets of rank 2 or more, y must be one-hot or have an explicit final dimension of 1 (Keras docs).
- The formula above makes the per-sample weights average to 1 (checked: 1.0000 on a 10% positive set, even though the two dict values average 2.4), which keeps the loss magnitude close to the unweighted run. Raw `1/freq` weights make the loss many times larger, which can destabilise the first steps.
- `class_weight` is applied to the training loss only. Validation loss is unweighted, so train and val losses are no longer comparable in scale.
- Multi-output models raise `ValueError: class_weight is only supported for Models with a single output` (Keras 3.15). Per-timestep labels of shape `(batch, steps, 1)` fail with an unhelpful `TypeError: only 0-dimensional arrays can be converted to Python scalars`; `(batch, steps)` labels ran without error, but use `sample_weight` for sequences.

## sample_weight
Two ways to pass it:
```python
model.fit(x, y, sample_weight=w)                      # NumPy arrays
ds = tf.data.Dataset.from_tensor_slices((x, y, w))      # tf.data: 3-tuples (x, y, sample_weight)
model.fit(ds.batch(256))
```
- For per-timestep weights (masking padded steps in seq2seq), give `w` shape `(batch, timesteps)`.
- For multi-output models pass a dict keyed by output name: `(x, {"a": ya, "b": yb}, {"a": wa, "b": wb})`. This worked only when the functional model's outputs are themselves a dict (`keras.Model(inp, {"a": a, "b": b})`); with list outputs `[a, b]` Keras 3.15 raised `KeyError: 0`. With a tf.data dataset, pass the weights as the third element; the `sample_weight=` argument is not supported there (Keras docs).
- Use cases beyond imbalance: down-weight noisy labels, up-weight recent data, importance weighting for covariate shift.

## Metrics
- `metrics=[...]` in `compile` ignores sample weights; `weighted_metrics=[...]` applies them (ran: with 50x weight on positives `evaluate` gave plain 0.475 vs weighted 0.614 accuracy). Report both if you weight training, and always report the business metric on the unweighted validation set.
- Weighting shifts predicted probabilities: a model trained with balanced weights over-predicts the minority class, so its probabilities are no longer calibrated. Either recalibrate on validation data or correct the threshold rather than reading `0.5` as meaningful.

## Alternative: output bias init
For a heavily imbalanced binary task, set the final `Dense` bias to `log(pos/neg)` (`keras.initializers.Constant`). This removes the first epochs spent learning the prior and often helps more than weights do.

## Gotchas
- `class_weight` together with a generator that already oversamples the minority class double-counts it.
- Weighted loss + `EarlyStopping(monitor="val_loss")` monitors unweighted val loss; consider monitoring `val_prc` (PR-AUC) instead.
- Weights are a `fit` argument, not part of the model, so they are not stored by `model.save`; reproduce them in retraining code.

## Verify
- [ ] Mean of the per-sample weights is ~1.
- [ ] Minority-class recall on validation rose and precision fell in a way you expected.
- [ ] Threshold or calibration adjusted after weighting; unweighted validation metrics reported.
