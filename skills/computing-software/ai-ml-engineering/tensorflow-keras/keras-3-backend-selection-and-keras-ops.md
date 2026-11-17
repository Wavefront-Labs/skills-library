---
id: computing-software.ai-ml-engineering.tensorflow-keras.keras-3-backend-selection-and-keras-ops
name: keras-3-backend-selection-and-keras-ops
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [keras, keras-3, multi-backend, keras-backend, keras-ops, jax, pytorch, backend-agnostic-layers]
level: practitioner
status: docs-checked
description: "Pick and switch the Keras 3 backend (JAX, PyTorch, TensorFlow), write backend-agnostic layers with keras.ops and keras.random, and know what stays backend-specific."
sources:
  - https://keras.io/getting_started/
  - https://keras.io/keras_3/
  - https://keras.io/api/ops/
  - https://keras.io/guides/distribution/
  - https://keras.io/api/random/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keras 3 backends and keras.ops

**Goal:** write a model once and train it on JAX, PyTorch or TensorFlow, choosing the backend for speed or ecosystem reasons.

## Selecting the backend
```bash
export KERAS_BACKEND=jax        # or torch / tensorflow; must be set before `import keras`
```
or `~/.keras/keras.json` -> `"backend": "jax"`. Check with `keras.config.backend()`. The backend cannot be switched within a running process after import.

## Choosing
- **JAX:** in the Keras team's benchmarks it typically gives the best training and inference performance on GPU, TPU and CPU, but results vary by model.
- **PyTorch:** interoperates with PyTorch code and libraries; Keras models are `torch.nn.Module`s and can sit inside a PyTorch training loop.
- **TensorFlow:** use it for `tf.distribute`; non-XLA TensorFlow is occasionally faster on GPU; Keras 3 models can be exported as a TensorFlow SavedModel.
Benchmark your model; there is no universal winner.

## Backend-agnostic layers
```python
import keras
from keras import ops

@keras.saving.register_keras_serializable(package="demo")
class GatedDense(keras.layers.Layer):
    def __init__(self, units, **kw):
        super().__init__(**kw); self.units = units
        self.seed_gen = keras.random.SeedGenerator(1337)
    def build(self, input_shape):
        self.w = self.add_weight(shape=(input_shape[-1], 2 * self.units), initializer="glorot_uniform", name="w")
    def call(self, x, training=False):
        h = ops.matmul(x, self.w)
        a, g = ops.split(h, 2, axis=-1)
        if training:
            a = keras.random.dropout(a, 0.1, seed=self.seed_gen)
        return a * ops.sigmoid(g)
    def get_config(self):
        return {**super().get_config(), "units": self.units}
```
- `keras.ops` mirrors NumPy (`ops.mean`, `ops.einsum`, `ops.take`) plus NN ops (`ops.softmax`, `ops.conv`).
- Randomness: use `keras.random.*` with a `keras.random.SeedGenerator` (created in `__init__`, e.g. `self.seed_gen = keras.random.SeedGenerator(1337)`), not backend RNGs - JAX needs explicit seed state.
- Avoid Python-side data-dependent control flow on tensor values; JAX tracing requires `ops.cond`/`ops.where`.

## Data pipelines
`fit()` accepts NumPy arrays, `tf.data.Dataset`, PyTorch `DataLoader` and `keras.utils.PyDataset` on any backend. A tf.data pipeline that does not use Keras layers feeds `fit` on all backends.

## What stays backend-specific
Custom `train_step` overrides (GradientTape vs `jax.value_and_grad` vs `loss.backward()`), distribution APIs (the `keras.distribution` guide says it is implemented for the JAX backend only; TF uses `tf.distribute`; PyTorch uses its own DDP tooling), and export paths.

## Verify
- [ ] Model trains on at least two backends with matching loss curves (within noise).
- [ ] No `tf.`/`torch.`/`jnp.` calls inside model code.
- [ ] Saved `.keras` file loads under another backend.

## Checked

Checked 2026-10-25 against Keras 3 (keras-team/keras master of 2026-10-23, keras-io of 2026-09-23). Confirmed `KERAS_BACKEND` and `~/.keras/keras.json` (must be set before import and cannot change afterwards), `keras.config.backend()`, the benchmark statement and the model-as-PyTorch-Module statement in the Keras 3 announcement, the accepted `fit()` input types, and the JAX-only status of `keras.distribution`. Removed the TFX and LiteRT export claims and the CPU-only TensorFlow remark.

Method: documentation only; no commands were run.
