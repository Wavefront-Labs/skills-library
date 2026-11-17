---
id: computing-software.ai-ml-engineering.tensorflow-keras.custom-keras-layers-build-call-get-config
name: custom-keras-layers-build-call-get-config
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow, keras, custom-keras-layer, get-config, add-weight, serialization, model-subclassing]
level: practitioner
status: verified
description: "Write Keras custom layers with __init__, build, call and get_config, create weights with add_weight, handle training and masks, and make them serialisable."
sources:
  - https://keras.io/guides/making_new_layers_and_models_via_subclassing/
  - https://keras.io/guides/serialization_and_saving/
  - https://keras.io/api/layers/base_layer/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom Keras layers

## Template
```python
import keras
from keras import ops

@keras.saving.register_keras_serializable(package="my_layers")
class ScaledDense(keras.layers.Layer):
    def __init__(self, units, scale_init=1.0, **kwargs):
        super().__init__(**kwargs)                      # passes name, dtype, trainable
        self.units, self.scale_init = units, scale_init

    def build(self, input_shape):                       # weights sized from the input
        self.w = self.add_weight(shape=(input_shape[-1], self.units), initializer="glorot_uniform", name="w")
        self.b = self.add_weight(shape=(self.units,), initializer="zeros", name="b")
        self.scale = self.add_weight(shape=(), initializer=keras.initializers.Constant(self.scale_init),
                                     name="scale")

    def call(self, x, training=None):
        y = ops.matmul(x, self.w) + self.b
        return y * self.scale

    def get_config(self):
        return {**super().get_config(), "units": self.units, "scale_init": self.scale_init}
```

## Rules
- Create weights in `build` (lazy, input-shape dependent) or `__init__` if shapes are known. Never in `call`.
- Use `keras.ops` (Keras 3) instead of `tf.*` to stay backend-agnostic; `tf.*` works only on the TF backend.
- `training` argument: Keras passes it automatically when you declare it; use it for dropout/noise. Don't read a global.
- Sublayers assigned as attributes in `__init__` are tracked automatically (weights, saving).
- Non-trainable state: `add_weight(..., trainable=False)` and update with `self.v.assign(...)`.
- Masking: set `self.supports_masking = True` to pass masks through, or implement `compute_mask`.
- Add losses from inside a layer (activity regularisation): `self.add_loss(...)`.

## Serialisation
- If you override `get_config`, it must return every `__init__` argument; Keras rebuilds with `cls(**config)`. If you do not override it, Keras 3 generates the config automatically from the `__init__` call (ran: a layer with `k=5.0` and no `get_config` reloaded with 5.0), but only for simple arguments. Objects (initializers, sublayers) need `keras.saving.serialize_keras_object` / `deserialize_keras_object`.
- `register_keras_serializable` lets `keras.models.load_model("m.keras")` find the class without `custom_objects`. Without either, Keras 3.15 raises `TypeError: Could not locate class 'Unreg'. Make sure custom classes and functions are decorated with @keras.saving.register_keras_serializable()`; `custom_objects={'Unreg': Unreg}` fixes it.
- If `build` creates weights depending on the input, Keras 3 records the build shape (`build_config` in the saved config); implement `build_from_config`/`get_build_config` only for unusual cases (both exist on `keras.layers.Layer`).

## Common errors
- `ValueError: Layer 'x' was never built and thus it doesn't have any variables` is a load-time error (Keras 3 source): the weights file lists variables for a layer whose parent `build()` did not create its state. Build children in the parent's `build()` or implement `build_from_config`. (Reading `layer.weights` on an unbuilt layer just returns `[]` and `layer.built` is `False`.)
- `Could not locate class` on load: not registered and not in `custom_objects`.
- Loaded model gives different outputs: a config field omitted from an overridden `get_config` so the default was used (ran: `k=5.0` came back as 1.0).

## Verify
```python
layer = ScaledDense(8); y = layer(keras.random.normal((2, 4)))
clone = ScaledDense.from_config(layer.get_config())
m = keras.Sequential([keras.Input((4,)), layer]); m.save("t.keras"); keras.models.load_model("t.keras")
```
