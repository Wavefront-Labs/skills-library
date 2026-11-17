---
id: computing-software.ai-ml-engineering.tensorflow-keras.loading-legacy-h5-and-savedmodel-in-keras-3
name: loading-legacy-h5-and-savedmodel-in-keras-3
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow-keras, tfsmlayer, h5-format, keras-3, savedmodel, legacy-models, tf-keras]
level: practitioner
status: gated
description: "Load old Keras 2 models in Keras 3: .h5 loading rules, TFSMLayer for SavedModels, tf_keras fallback, custom_objects, and converting to the .keras format."
sources:
  - https://keras.io/guides/migrating_to_keras_3/
  - https://keras.io/api/layers/backend_specific_layers/tfsm_layer/
  - https://keras.io/api/models/model_saving_apis/model_saving_and_loading/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Loading legacy H5 and SavedModel files in Keras 3

**Context:** Keras 3 saves and loads the `.keras` zip format natively. Older artifacts need specific paths.

## Decision table
| You have | Do |
|---|---|
| `model.h5` (Keras 2 full model) | `keras.models.load_model("model.h5", custom_objects={...}, compile=False)`: Keras 3 supports legacy H5 for standard layers; custom layers need `custom_objects` and Keras-3-compatible code (ran: an H5 saved by tf_keras 2 with a custom layer failed with `ValueError: Unknown layer: 'MyL'` until `custom_objects={'MyL': MyL}` was passed, then matched the Keras 2 output to 1e-6) |
| `weights.h5` only | rebuild the architecture in code, then `model.load_weights("weights.h5")` (ran with a Keras 3 `save_weights`; Keras 3 requires the name to end in `.weights.h5`, `save_weights('w.h5')` raised `The filename must end in .weights.h5`) |
| TF SavedModel directory (from `model.save("dir")` in TF2) | inference only: `keras.layers.TFSMLayer("dir", call_endpoint="serving_default")` (TF backend; ran on a Keras 2 SavedModel: output matched the Keras 2 model; `keras.models.load_model("dir")` raised `File format not supported`) |
| Anything that fails | install `tf_keras` (Keras 2 package) and set `TF_USE_LEGACY_KERAS=1` before importing TensorFlow, load there, then rebuild/convert (ran: this is how the legacy test files were created) |

## TFSMLayer
```python
import keras
layer = keras.layers.TFSMLayer("saved_model_dir", call_endpoint="serving_default")
inputs = keras.Input(shape=(224, 224, 3))
outputs = layer(inputs)
wrapped = keras.Model(inputs, outputs)
```
Treat it as inference-only (the reloaded variables were still marked trainable in Keras 3.15, so freeze it explicitly if you wrap it) and it needs the TensorFlow backend. The output was a dict keyed by the signature output name (`{'dense_1': ...}` for the Keras 2 model, `{'output_0': ...}` for a Keras 3 export).

## Converting to .keras
1. Load with whichever path works (possibly `tf_keras`).
2. Rebuild the model with Keras 3 code (port custom layers to `keras.ops`).
3. Transfer weights layer by layer: `new.get_layer(n).set_weights(old.get_layer(n).get_weights())`.
4. `new.save("model.keras")` and validate predictions.

## Gotchas
- `model.save("name")` without extension in Keras 3 raises `ValueError: Invalid filepath extension for saving` (ran); give `.keras` or `.h5`, or use `model.export()` for SavedModel.
- Custom objects must be registered (`@keras.saving.register_keras_serializable`) or passed in `custom_objects`.
- Lambda layers store Python function bytecode; loading one with a Python lambda raised `Requested the deserialization of a Lambda layer whose function is a Python lambda ... disallowed by default`, and `load_model(..., safe_mode=False)` loaded it (ran, `.keras` file). Only use `safe_mode=False` on files you trust, and replace Lambdas with proper layers. (H5 bytecode portability across Python versions was not tested.) (gated: unconfirmed, source is paywalled or blocked)

## Verify
- [ ] Predictions from the converted `.keras` model match the legacy model on a fixed batch.
