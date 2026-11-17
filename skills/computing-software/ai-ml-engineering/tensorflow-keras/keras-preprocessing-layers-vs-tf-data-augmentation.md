---
id: computing-software.ai-ml-engineering.tensorflow-keras.keras-preprocessing-layers-vs-tf-data-augmentation
name: keras-preprocessing-layers-vs-tf-data-augmentation
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow, keras, keras-preprocessing-layers, data-augmentation, normalization-adapt, stringlookup, textvectorization, tf-data]
level: practitioner
status: verified
description: "Decide where Keras preprocessing runs: augmentation and adapt() layers inside the model vs in tf.data, export consequences, and avoiding train/serve skew."
sources:
  - https://keras.io/api/layers/preprocessing_layers/
  - https://www.tensorflow.org/tutorials/images/data_augmentation
  - https://keras.io/api/layers/preprocessing_layers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keras preprocessing layers vs tf.data preprocessing

**Goal:** put each preprocessing step where it is fastest during training and still present at serving time.

## Two placements
1. **Inside the model** (`model = keras.Sequential([layers.RandomFlip(), layers.Rescaling(1/255), backbone])`):
   - Runs as part of the model on whatever device the model uses, synchronously with it.
   - Exported with the model, so serving receives raw inputs; no train/serve skew.
2. **In the tf.data pipeline** (`ds.map(lambda x, y: (aug(x, training=True), y), num_parallel_calls=AUTOTUNE)`):
   - Runs asynchronously on CPU, overlapped with training via `prefetch`.
   - Not part of the saved model; serving must reproduce it.

Rule of thumb: **augmentation** (random flips, crops, rotations, `RandomContrast`) goes in tf.data or in the model - it is training-only either way. **Deterministic normalisation/lookup** (`Normalization`, `StringLookup`, `TextVectorization`, `Rescaling`) should end up in the exported model so clients send raw data.

A common pattern: apply them in tf.data while training, then build an inference model that wraps them (ran with `TextVectorization`; the serving model took `tf.constant(['hello foo'])` and reloaded from `.keras`):
```python
inputs = keras.Input(shape=(), dtype="string")
x = vectorizer(inputs)          # same adapted layer object
outputs = trained_model(x)
serving_model = keras.Model(inputs, outputs)
```

## adapt()
```python
norm = layers.Normalization()
norm.adapt(train_ds.map(lambda x, y: x))       # training split only
lookup = layers.StringLookup(num_oov_indices=1, max_tokens=50_000)
lookup.adapt(train_ds.map(lambda x, y: x["city"]))
```
- Adapt on the **training** split only; adapting on all data leaks validation statistics.
- `StringLookup` puts the OOV token first (`['[UNK]', 'a', 'b', 'c']`, `vocabulary_size() == 4`; an unseen string mapped to index 0, no error). `max_tokens` is an upper bound that includes OOV and mask slots: `max_tokens=3` on a, a, a, b, b, c kept only `['[UNK]', 'a', 'b']`. With `mask_token=''` the vocabulary started `['', '[UNK]', ...]`. Ran on Keras 3.15.
- Adapted state is saved with the layer (ran: a `TextVectorization` + model reloaded from `.keras` gave identical output on a raw string), so the vocabulary/statistics are frozen at export time; re-adapt and re-export when data shifts.

## Augmentation layer behaviour
- Random augmentation layers are identity with `training=False` and inside `model.predict` (ran: `predict` twice gave identical output; `RandomFlip(img, training=False)` never changed the input). Called directly with no `training` argument, `RandomFlip` still flipped (9 of 10 calls differed), so in a tf.data map pass `training=True` explicitly to make the intent clear (ran: the map produced `(8, 8, 3)` images).
- Where the work runs is a performance question: measure the step time with augmentation inside the model against in tf.data on your hardware.

## Verify
- [ ] Saved model accepts raw serving inputs and produces the same predictions as the training pipeline on a sample.
- [ ] `adapt()` called on training data only.
- [ ] Augmentation absent at inference (`model(x, training=False)` deterministic).
