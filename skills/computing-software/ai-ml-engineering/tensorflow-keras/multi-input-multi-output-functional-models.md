---
id: computing-software.ai-ml-engineering.tensorflow-keras.multi-input-multi-output-functional-models
name: multi-input-multi-output-functional-models
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow, keras, multi-output-model, functional-api, multi-input, loss-weights, keras-functional-api]
level: practitioner
status: verified
description: "Build Keras functional models with several inputs and outputs, name them, set per-output losses, loss_weights and metrics, and feed tf.data dicts correctly."
sources:
  - https://keras.io/guides/functional_api/
  - https://keras.io/api/models/model_training_apis/
  - https://www.tensorflow.org/guide/keras/functional_api
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-input / multi-output functional models

## Build with named inputs and outputs
```python
import keras
from keras import layers
title = keras.Input(shape=(None,), dtype="int64", name="title")
body = keras.Input(shape=(None,), dtype="int64", name="body")
tags = keras.Input(shape=(num_tags,), name="tags")
t = layers.GlobalAveragePooling1D()(layers.Embedding(vocab, 64)(title))
b = layers.GlobalAveragePooling1D()(layers.Embedding(vocab, 64)(body))
x = layers.concatenate([t, b, tags])
priority = layers.Dense(1, name="priority")(x)                      # regression
department = layers.Dense(num_depts, name="department")(x)          # logits
model = keras.Model(inputs=[title, body, tags], outputs={"priority": priority, "department": department})
```
Output layer `name`s become dict keys for losses, metrics and logged metric names (ran on Keras 3.15 with `outputs={...}`: history keys were `department_accuracy, department_loss, loss, priority_loss, priority_mae`).

## Compile per output
```python
model.compile(
    optimizer="adam",
    loss={"priority": keras.losses.MeanSquaredError(),
          "department": keras.losses.SparseCategoricalCrossentropy(from_logits=True)},
    loss_weights={"priority": 1.0, "department": 0.2},
    metrics={"priority": ["mae"], "department": ["accuracy"]})
```
- Total loss = weighted sum. Losses on different scales (MSE in thousands vs CE ~2) make one dominate; normalise targets or tune `loss_weights` so contributions are comparable at the start.
- Use `None` as a loss for an output you only want to predict, not train (ran: `loss={"priority": mse, "department": None}` compiled and fit).

## Feed data
```python
ds = tf.data.Dataset.from_tensor_slices((
    {"title": T, "body": B, "tags": G},
    {"priority": P, "department": D})).shuffle(10_000).batch(64).prefetch(tf.data.AUTOTUNE)
model.fit(ds, epochs=10)
```
Dict keys must match input/output names exactly (ran: a misspelt key raised `ValueError: Missing data for input "tags"`). With lists, arrays pair by position and nothing checks the meaning: swapping two same-shaped inputs `[B, A]` for `[A, B]` trained without any error, and list targets for a dict-output model were accepted too. Prefer dicts over lists.

## Shared layers and branches
- Reuse a layer object on two inputs to share weights (siamese towers).
- Get intermediate outputs for feature extraction: `keras.Model(model.input, model.get_layer("concatenate").output)`.
- `keras.utils.plot_model(model, show_shapes=True)` to check wiring.

## Sample weights per output
Pass a weight (or `None`) for every output: `sample_weight={"priority": None, "department": w}` in `fit` or `{"priority": ones, "department": w}` as the third element of the dataset tuple. A partial dict `{"department": w}` raised `ValueError: You should provide one sample_weight array per output in y` for arrays and `KeyError: 'p'` in a tf.data dataset (ran on Keras 3.15).

## Verify
`model.summary()` shows both outputs; `history.history` contains `priority_loss`, `department_loss` and `loss`; check their magnitudes in the first epoch. `model.get_layer("concatenate")` and `keras.utils.plot_model` both exist (the first ran; `plot_model` was only checked for presence, it needs Graphviz).
