---
id: computing-software.ai-ml-engineering.tensorflow-keras.keras-distribution-api-data-model-parallel
name: keras-distribution-api-data-model-parallel
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow-keras, keras-distribution-api, dataparallel, modelparallel, layout-map, jax-backend, device-mesh]
level: practitioner
status: docs-checked
description: "Distribute Keras 3 training with keras.distribution: DataParallel, ModelParallel with DeviceMesh and LayoutMap sharding rules, and backend support limits."
sources:
  - https://keras.io/guides/distribution/
  - https://keras.io/api/distribution/
  - https://github.com/keras-team/keras/blob/master/keras/src/distribution/distribution_lib.py
  - https://github.com/keras-team/keras-hub/blob/master/keras_hub/src/models/gemma/gemma_backbone.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Keras distribution API

Keras 3 provides a backend-level distribution API (`keras.distribution`). The Keras guide states it is only implemented for the **JAX** backend for now, so on TensorFlow or PyTorch use `tf.distribute` or PyTorch's own tooling instead.

## Data parallel
```python
import keras
devices = keras.distribution.list_devices()          # e.g. 8 GPUs / TPU cores
keras.distribution.set_distribution(keras.distribution.DataParallel(devices=devices))
model = build_model(); model.compile(...); model.fit(ds, epochs=3)   # unchanged training code
```
Weights (and optimizer, RNG and metric state) are replicated on every device; the dataset passed to `fit` is split evenly on the batch dimension.

## Model parallel (sharding)
```python
mesh = keras.distribution.DeviceMesh(shape=(2, 4), axis_names=("batch", "model"), devices=devices)
layout_map = keras.distribution.LayoutMap(mesh)
layout_map["d1/kernel"] = (None, "model")       # shard the kernel's second dimension over "model"
layout_map["d1/bias"] = ("model",)
layout_map["d2/output"] = ("batch", None)       # layout for a layer output
dist = keras.distribution.ModelParallel(layout_map, batch_dim_name="batch")
keras.distribution.set_distribution(dist)
# build the model after set_distribution; KerasHub ships ready-made maps, e.g.
# keras_hub.models.GemmaBackbone.get_layout_map(mesh) for Gemma models
```
- Keys are regexes matched against `variable.path`; values are per-dimension mesh axis names or `None` (replicated on that dimension); a tuple or list is converted to a `TensorLayout`.
- Mesh shape `(2, 4)` with axes `("batch", "model")`: 2-way data parallel x 4-way model parallel.
- If several keys match a path a `ValueError` is raised; if none match, no layout is found and the variable is replicated.

## Order matters
Call `set_distribution` before creating the model so its variables are created under the distribution (the guide notes that all weights created after `set_distribution` follow it).

## Multi-host
Call `keras.distribution.initialize()` on every process before any computation (arguments `job_addresses`, `num_processes`, `process_id`, or the environment variables `KERAS_DISTRIBUTION_JOB_ADDRESSES`, `KERAS_DISTRIBUTION_NUM_PROCESSES`, `KERAS_DISTRIBUTION_PROCESS_ID`); in a distributed setting `list_devices()` returns global devices. Distribution classes shard the dataset among processes by default (`auto_shard_dataset=True`).

## When to use what
| Situation | Use |
|---|---|
| Keras 3 + JAX, LLM fine-tuning across TPU/GPU | keras.distribution (ModelParallel) |
| Keras 3 + TF backend | tf.distribute strategies |
| Keras 3 + PyTorch backend | PyTorch's own distributed tooling |

## Gotchas
- Regexes that match nothing fall back to replication without an error; inspect the resulting variable shardings (for example `variable.value.sharding` on JAX).

## Checked

Checked 2026-10-25 against Keras 3 (keras-team/keras master of 2026-10-23, keras-io of 2026-09-23). Confirmed `DataParallel`, `DeviceMesh`, `LayoutMap` (regex keys matched against `variable.path`, tuple shortcut, ValueError on multiple matches, None when nothing matches), `ModelParallel(layout_map, batch_dim_name=...)`, `set_distribution`, the JAX-only statement in the guide, `keras.distribution.initialize` and its environment variables, `auto_shard_dataset` (all in the Keras guide and `distribution_lib.py`), and KerasHub's `GemmaBackbone.get_layout_map`. Replaced the hand-written Gemma regexes (which did not match KerasHub's own map) with the guide's example; removed the `jax.distributed.initialize`, `distribute_dataset` and divisibility claims.

Method: documentation only; no commands were run.
