---
id: computing-software.ai-ml-engineering.tensorflow-keras.keras-3-pytorch-backend
name: keras-3-pytorch-backend
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow-keras, keras-torch-backend, keras-3, pytorch, multi-backend, keras-backend]
level: practitioner
status: docs-checked
description: "Run Keras 3 on the PyTorch backend: KERAS_BACKEND=torch, using Keras models as nn.Modules in torch loops, data inputs, device handling and known gaps."
sources:
  - https://keras.io/getting_started/
  - https://keras.io/guides/writing_a_custom_training_loop_in_torch/
  - https://keras.io/keras_3/
  - https://keras.io/guides/distribution/
  - https://github.com/keras-team/keras/blob/master/keras/src/trainers/trainer.py
  - https://github.com/keras-team/keras/blob/master/keras/src/callbacks/tensorboard.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Keras 3 with the PyTorch backend

**Why:** reuse Keras model code and KerasHub presets inside a PyTorch ecosystem (torch DataLoader, custom torch loops, FSDP/serving tooling).

## Select the backend
```bash
export KERAS_BACKEND=torch      # before importing keras; or set "backend" in ~/.keras/keras.json
```
```python
import keras; print(keras.backend.backend())   # 'torch'
```
The backend cannot change after import within a process.

## Use fit() as usual
`model.fit` accepts NumPy arrays, `torch.utils.data.DataLoader`, `tf.data.Dataset` or Python generators on any backend.

## Use the model in a native torch loop
With the torch backend, a Keras `Model`/`Layer` is a `torch.nn.Module`:
```python
import torch, keras
model = keras.Sequential([keras.layers.Dense(64, activation="relu"), keras.layers.Dense(10)])
model.build((None, 32))
opt = torch.optim.AdamW(model.parameters(), lr=1e-3)
loss_fn = torch.nn.CrossEntropyLoss()
for x, y in loader:
    logits = model(x.cuda())
    loss = loss_fn(logits, y.cuda())
    model.zero_grad(); loss.backward(); opt.step()
```
Call `model.build` (or run one forward) before `model.parameters()` so weights exist. The Keras guide clears gradients with `model.zero_grad()` before `loss.backward()`.

## Devices
In your own loop, make sure inputs and the model's variables are on the same torch device (the example moves inputs with `.cuda()`); check the Keras torch-loop guide for device placement behaviour.

## Gaps and gotchas
- Performance: with `jit_compile="auto"` the torch backend runs eagerly; `jit_compile=True` runs with `torch.compile` using the `inductor` backend.
- Saving: models trained on one backend can be loaded with `keras.saving.load_model` under another backend (the Keras 3 guide shows loading a model trained on PyTorch, JAX or TensorFlow under the OpenVINO backend).
- Mixed precision: `keras.mixed_precision.set_dtype_policy("mixed_bfloat16")` works across backends.
- Distributed: the `keras.distribution` guide says the API is implemented for the JAX backend only; use PyTorch's own tooling for multi-device torch training.
- Profiling: `keras.callbacks.TensorBoard(profile_batch=...)` raises a ValueError on the torch backend (profiling is only available on JAX and TensorFlow).

## Verify
- [ ] Save a `.keras` model trained on torch, load with `KERAS_BACKEND=jax`, and compare predictions.

## Checked

Checked 2026-10-25 against Keras 3 (keras-team/keras master of 2026-10-23, keras-io of 2026-09-23). Confirmed backend selection, the Keras-model-is-a-torch-Module statement and the native torch loop pattern (`model.parameters()`, `model.zero_grad()`, `loss.backward()`), accepted `fit` inputs, `jit_compile="auto"` eager default and `torch.compile` with `inductor` on the torch backend (`trainer.py` docstring), cross-backend loading, the JAX-only `keras.distribution` status, `keras.mixed_precision.set_dtype_policy`, and the TensorBoard profiling restriction. Removed the unconfirmed default-device claim and the JAX-fastest remark.

Method: documentation only; no commands were run.
