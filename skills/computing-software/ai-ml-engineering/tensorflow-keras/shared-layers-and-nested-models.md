---
id: computing-software.ai-ml-engineering.tensorflow-keras.shared-layers-and-nested-models
name: shared-layers-and-nested-models
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow-keras, shared-layers, nested-models, siamese-network, functional-api, weight-sharing, keras]
level: practitioner
status: verified
description: "Reuse Keras layers and whole models across inputs with the functional API: siamese towers, nested models as layers, weight sharing checks and freezing nested parts."
sources:
  - https://keras.io/guides/functional_api/#shared-layers
  - https://keras.io/guides/functional_api/#all-models-are-callable-just-like-layers
  - https://keras.io/guides/transfer_learning/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Shared layers and nested models

## Shared layers
Calling the same layer instance on several inputs reuses its weights.
```python
emb = keras.layers.Embedding(20000, 128)
enc = keras.layers.LSTM(64)
a, b = keras.Input((None,), dtype="int32"), keras.Input((None,), dtype="int32")
va, vb = enc(emb(a)), enc(emb(b))                  # one set of weights, two call sites
sim = keras.layers.Dot(axes=1, normalize=True)([va, vb])
model = keras.Model([a, b], sim)
```
- `len(model.weights)` counts the shared weights once (ran: 4 for the shared model, 8 for the same model with separate Embedding and LSTM layers).
- Each call creates a separate node: in Keras 3.15 `enc._inbound_nodes` had length 2 and `get_output_at` no longer exists on the layer (it was Keras 2 API).

## Models are layers
```python
tower = keras.Sequential([keras.layers.Rescaling(1/255), base_cnn, keras.layers.GlobalAveragePooling2D(), keras.layers.Dense(128)], name="tower")
left, right = keras.Input((224, 224, 3)), keras.Input((224, 224, 3))
dist = keras.layers.Lambda(lambda t: keras.ops.abs(t[0] - t[1]))([tower(left), tower(right)])
siamese = keras.Model([left, right], keras.layers.Dense(1, activation="sigmoid")(dist))
```
- The nested model appears as one layer in `summary()` (`expand_nested=True` to see inside; ran, the expanded text contained `conv2d`).
- Reuse the trained tower alone afterwards: `tower.predict(images)` for embeddings (ran: `(2, 128)`).

## Freezing nested parts
- `tower.trainable = False` freezes all its weights recursively (ran: `len(tower.trainable_weights) == 0`).
- BatchNormalization inside a frozen nested model: setting `trainable=False` on BN also makes it run in inference mode (ran: a frozen BN's `moving_mean` stayed `[0,0,0]` after a `training=True` call and after two `fit` epochs inside a nested model, while an unfrozen BN moved to about 0.02 and the same nested BN moved after `trainable=True` and recompiling). When fine-tuning a pretrained base, call it as `base(x, training=False)` so BN statistics stay fixed even after unfreezing.
- Recompile after changing `trainable`.

## Multiple outputs from one nested model
Build an intermediate-feature extractor once and share it:
```python
feat = keras.Model(base.input, [base.get_layer("block3_pool").output, base.output])
```

## Gotchas
- Lambda layers with Python functions are refused on load by default (ran: `Requested the deserialization of a Lambda layer whose function is a Python lambda ... disallowed by default`); prefer small subclassed layers with `get_config` for saved models.
- Sharing a layer between inputs of different shapes fails if the layer builds weights from the first input's shape (ran: `Dense` built for 3 features then called with 5 raised `ValueError ... expected axis -1 of input shape to have value 3`).
- Subclassed models sharing a layer: just assign the layer once in `__init__` and call it twice in `call`.
