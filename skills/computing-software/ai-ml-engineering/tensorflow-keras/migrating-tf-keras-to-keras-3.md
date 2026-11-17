---
id: computing-software.ai-ml-engineering.tensorflow-keras.migrating-tf-keras-to-keras-3
name: migrating-tf-keras-to-keras-3
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow, keras, keras-3, keras3-migration, tf-keras, tf-use-legacy-keras, model-export]
level: practitioner
status: gated
description: "Migrate tf.keras (Keras 2) code to Keras 3: what TF 2.16+ changed, tf_keras fallback, saving/export changes, keras.ops replacements and custom layer fixes."
sources:
  - https://keras.io/guides/migrating_to_keras_3/
  - https://keras.io/keras_3/
  - https://github.com/keras-team/tf-keras
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating tf.keras code to Keras 3

**Goal:** move a Keras 2 codebase onto Keras 3 (or deliberately pin Keras 2) without broken saves and silent behaviour changes.

## What changed under you
- From **TensorFlow 2.16**, `tf.keras` resolves to Keras 3 (TF 2.16.1 release notes: "Keras 3.0 will be the default Keras version. You may need to update your script to use Keras 3.0"). Code that ran on TF 2.15 may break on upgrade.
- To stay on Keras 2 for now: `pip install tf_keras` and set `TF_USE_LEGACY_KERAS=1` before importing TensorFlow (or `import tf_keras as keras`); the release notes give both routes and ran here: `tf.keras.Model.__module__` became `tf_keras.src.engine.training`. Use this as a bridge, not a destination.

## Saving and exporting
| Keras 2 | Keras 3 |
|---|---|
| `model.save("dir")` -> SavedModel | `model.save("model.keras")` (extension required, `.h5` legacy; ran: a bare name raised `ValueError: Invalid filepath extension for saving`) |
| SavedModel for serving | `model.export("dir")` (SavedModel with inference signature) or `keras.export.ExportArchive` for custom signatures |
| `tf.keras.models.load_model("dir")` on SavedModel | raises `File format not supported` in Keras 3.15 (ran); use `keras.layers.TFSMLayer("dir", call_endpoint="serving_default")` for inference (ran on a tf_keras SavedModel) |

## Code changes that bite
- **TF ops in layers:** `tf.*` calls inside custom layers work only on the TF backend. For backend-agnostic code, replace with `keras.ops` (`ops.matmul`, `ops.softmax`, `ops.where`, ...). `tf.keras.backend.*` functions largely move to `keras.ops`.
- **Custom layers:** `add_weight(shape=..., initializer=..., name=...)` - pass arguments by keyword (the form ran in the custom-layer test). Decorate with `@keras.saving.register_keras_serializable(package="my_pkg")` so `.keras` files reload (unregistered layers raised `Could not locate class`) and implement `get_config()` when `__init__` arguments are not simple.
- **Optimizers:** Keras 3 optimizers only; `keras.optimizers.legacy.Adam()` raised `ImportError: keras.optimizers.legacy is not supported in Keras 3` (ran), with a message to install `tf_keras`. Learning-rate schedules are `keras.optimizers.schedules`.
- **`Model.fit` with TF-specific features:** `tf.distribute` strategies still work on the TF backend. Custom `train_step` overriding using `tf.GradientTape` remains TF-only. `self.compiled_loss` / `self.compiled_metrics` still run in Keras 3.15 but emit deprecation warnings; use `self.compute_loss(y=y, y_pred=y_pred)` and per-metric `update_state` (ran).
- **`jit_compile`** defaults to `"auto"` (XLA where the model supports it, per the Keras `compile` docs; `inspect.signature(Model.compile)` in 3.15 shows `jit_compile='auto'`); if you see different numerics or slow first steps, compare with `jit_compile=False`.
- Estimators, `tf.compat.v1` layers and `tf.feature_column` have no Keras 3 equivalent; replace with preprocessing layers (`StringLookup`, `Normalization` and friends ran). (gated: unconfirmed, source is paywalled or blocked)

## Migration procedure
1. Pin versions; run the test suite on TF 2.15/Keras 2 to get a baseline (predictions on a fixed batch saved to disk).
2. Upgrade, set `KERAS_BACKEND=tensorflow`, fix import/saving errors.
3. Re-save models as `.keras`; re-export serving SavedModels with `model.export`.
4. Compare predictions with the baseline (tolerance ~1e-5 float32).
5. Optional: port `tf.*` ops to `keras.ops` and try other backends.

## Verify
- [ ] Baseline predictions match after migration.
- [ ] `.keras` files reload in a fresh process with custom objects registered.
- [ ] Serving SavedModel signatures unchanged for clients.
