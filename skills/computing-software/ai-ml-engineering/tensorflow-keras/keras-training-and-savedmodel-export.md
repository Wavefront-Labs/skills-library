---
id: computing-software.ai-ml-engineering.tensorflow-keras.keras-training-and-savedmodel-export
name: keras-training-and-savedmodel-export
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow, keras, keras-3, tf-keras, tf-data, prefetch, autotune, model-fit, callbacks, modelcheckpoint, earlystopping, reducelronplateau, savedmodel, model-export, keras-format, serving-signatures, exportarchive, tensorflow-serving, tf-serving, saved-model-cli, deep-learning, model-deployment]
level: practitioner
status: gated
description: "Train with Keras 3 and tf.data (prefetch AUTOTUNE, callbacks), save .keras for training, export a SavedModel with serving signatures, and serve it with TensorFlow Serving."
sources:
  - https://keras.io/api/
  - https://www.tensorflow.org/guide/data_performance
  - https://www.tensorflow.org/guide/saved_model
  - https://www.tensorflow.org/tfx/guide/serving
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keras Training and SavedModel Export — from fit() to a served endpoint

**Goal:** train efficiently with Keras and tf.data, keep a resumable training artefact, and ship a SavedModel that TensorFlow Serving can load with a known signature.

## 1. Know which Keras you have
- **Keras 3** is multi-backend (TensorFlow, JAX, PyTorch). From TensorFlow 2.16, `import tensorflow as tf; tf.keras` resolves to Keras 3 (TF 2.16.1 release notes: "Keras 3.0 will be the default Keras version"; ran on TF 2.21.0 with Keras 3.15.1).
- Legacy **Keras 2** lives on as the `tf_keras` package; setting the environment variable `TF_USE_LEGACY_KERAS=1` makes `tf.keras` point to it (TF 2.16.1 release notes; ran: `tf.keras.Model.__module__` was `tf_keras.src.engine.training`; needs `pip install tf_keras`). Use this only to keep old code running.
- Gotcha: tutorials before 2024 use Keras 2 behaviour — `model.save("dir")` writing a SavedModel no longer works in Keras 3 (ran: `ValueError: Invalid filepath extension for saving. Please add either a .keras extension ... or a .h5 extension. Use model.export(filepath) if you want to export a SavedModel`). Check `keras.__version__` first.

## 2. Input pipeline with tf.data
```python
AUTOTUNE = tf.data.AUTOTUNE
ds = (tf.data.Dataset.from_tensor_slices((x, y))
      .shuffle(10_000, reshuffle_each_iteration=True)
      .map(preprocess, num_parallel_calls=AUTOTUNE)
      .batch(256)
      .prefetch(AUTOTUNE))
```
- Order: `cache()` after expensive deterministic work and before random augmentation; `shuffle` before `batch`; `prefetch` last.
- `shuffle(buffer)` only shuffles within the buffer — a buffer smaller than the dataset on sorted files gives badly mixed batches. Shuffle file lists too (`list_files(..., shuffle=True)`, `interleave`).
- Do not `.repeat()` without `steps_per_epoch`, or `fit` never ends an epoch (documented behaviour for infinite datasets; not run). (gated: unconfirmed, source is paywalled or blocked)
- Profile with the TensorBoard profiler; an input-bound step shows the GPU idle between steps.

## 3. Compile, fit, callbacks
```python
model.compile(optimizer=keras.optimizers.AdamW(1e-3),
              loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])
callbacks = [
  keras.callbacks.ModelCheckpoint("ckpt/best.keras", monitor="val_loss", save_best_only=True),
  keras.callbacks.EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True),
  keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=2),
  keras.callbacks.TensorBoard(log_dir="logs"),
]
model.fit(train_ds, validation_data=val_ds, epochs=50, callbacks=callbacks)
```
- `from_logits=True` must match a final layer with no softmax; mismatches train but poorly.
- `EarlyStopping` has `restore_best_weights=False` by default (checked), which leaves you with the last epoch's weights.
- For long jobs on preemptible machines add `keras.callbacks.BackupAndRestore("backup")` so a restarted `fit` resumes mid-training.
- Mixed precision: `keras.mixed_precision.set_global_policy("mixed_bfloat16")` (or `"mixed_float16"` on older GPUs, where Keras wraps the optimizer with loss scaling (gated: unconfirmed, source is paywalled or blocked)). Keep the final layer in float32 (`dtype="float32"`) for stable softmax.

## 4. Two artefacts, two jobs
| Format | Call | Use for |
|---|---|---|
| `.keras` (zip: config + weights) | `model.save("m.keras")`, `keras.models.load_model` | resuming training, sharing within Python/Keras |
| SavedModel (directory) | `model.export("export/1")` | inference serving: TF Serving, TFLite conversion, other languages |

`model.export()` writes an inference-only SavedModel (TensorFlow backend) with a `serve` endpoint (ran: the directory held `assets`, `fingerprint.pb`, `saved_model.pb`, `variables`, and `tf.saved_model.load` listed signatures `['serve', 'serving_default']`); you cannot resume training from it (`keras.models.load_model` on it raised `File format not supported ... Keras 3 only supports V3 .keras files, legacy H5 format files`). Custom layers need `@keras.saving.register_keras_serializable()` (or `custom_objects`) or `.keras` loading fails with `Could not locate class`; Keras 3 auto-generates `get_config` only when you do not override it.

## 5. Serving signatures
For explicit names and preprocessing, use `keras.export.ExportArchive`:
```python
archive = keras.export.ExportArchive()
archive.track(model)
archive.add_endpoint(name="serve", fn=model.call,
    input_signature=[tf.TensorSpec([None, 28, 28], tf.float32, name="image")])
archive.write_out("export/1")
```
(Ran on Keras 3.15: wrote `export/2` and `tf.saved_model.load(...).serve(tf.ones((2,28,28)))` returned shape `(2, 10)`; the endpoint also lists optional `training` and `mask` arguments because `model.call` was passed.) Inspect with `saved_model_cli show --dir export/1 --all` (the executable ships with TensorFlow) and confirm input names, dtypes and shapes. Use `None` for the batch dimension. Putting tokenisation or normalisation inside the exported function removes training/serving skew — a frequent source of production accuracy loss (see computing-software.ai-ml-engineering.mlops.production-model-monitoring).

## 6. TensorFlow Serving
TF Serving expects `<MODEL_BASE>/<model_name>/<integer_version>/saved_model.pb`; the TF Serving basic guide says to use a larger integer for a newer version of the same model, and by default the server serves the latest version. (gated: unconfirmed, source is paywalled or blocked) The Docker commands below were not run (no Docker here).
```bash
docker run -p 8501:8501 \
  -v "<PROJECT_ROOT>/export:/models/mnist" -e MODEL_NAME=mnist tensorflow/serving
curl -d '{"instances": [[...]]}' localhost:8501/v1/models/mnist:predict
```
Port 8501 is REST, 8500 gRPC (TF Serving Docker docs: "Port 8500 exposed for gRPC, Port 8501 exposed for the REST API"; `MODEL_NAME` defaults to `model`). Pin the serving image tag to a TF version no older than the one you trained with; newer ops are not supported by older servers. A missing version directory (exporting straight into `/models/mnist`) is the classic "no versions found" error (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] `keras.__version__` is known and the code uses Keras 3 or explicitly `tf_keras`.
- [ ] The tf.data pipeline ends with `prefetch(AUTOTUNE)` and the profiler shows no input-bound gap.
- [ ] `load_model("m.keras")` reproduces validation metrics exactly.
- [ ] `saved_model_cli show` lists a `serve`/`serving_default` signature with the expected input names and a `None` batch dimension.
- [ ] A curl to the TF Serving REST endpoint returns predictions matching in-Python predictions on the same inputs.
