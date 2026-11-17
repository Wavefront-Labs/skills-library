---
id: computing-software.ai-ml-engineering.tensorflow-keras.keras-dtype-policies-and-quantize
name: keras-dtype-policies-and-quantize
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow-keras, keras-quantize, dtype-policy, int8-quantization, float8, mixed-precision, keras-3]
level: practitioner
status: gated
description: "Use Keras 3 dtype policies and model.quantize('int8' / 'int4' / 'float8') for post-training weight quantization, with saving, LoRA interplay and accuracy checks."
sources:
  - https://keras.io/guides/int8_quantization_in_keras/
  - https://keras.io/api/mixed_precision/policy/
  - https://keras.io/guides/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Keras 3 dtype policies and model.quantize()

## Dtype policies
A policy sets **variable dtype** and **compute dtype** per layer.
```python
keras.config.set_dtype_policy("mixed_bfloat16")   # vars float32, compute bfloat16 (training; ran on CPU: kernel float32, output bfloat16)
keras.config.set_dtype_policy("bfloat16")          # vars and compute bfloat16 (inference / memory; ran: both bfloat16)
layer = keras.layers.Dense(10, dtype="float32")    # override per layer (e.g. output logits; ran: the layer reported policy float32 with float32 variables and compute)
print(layer.dtype_policy, layer.variable_dtype, layer.compute_dtype)
```
Quantized layers carry policies named `<mode>_from_<original policy>`; ran on Keras 3.15: `int8_from_float32`, `int8_from_mixed_bfloat16`, `int4/128_from_float32` and `float8_from_float32` (printed as `QuantizedDTypePolicy`, `Int4DTypePolicy`, `QuantizedFloat8DTypePolicy`).

## Post-training quantization
```python
model = keras_hub.models.CausalLM.from_preset("gemma2_2b_en", dtype="bfloat16")
model.quantize("int8")             # also "int4" or "float8"
model.save("gemma_int8.keras")
```
The Gemma preset download was not run here (`keras_hub.models.CausalLM.from_preset` exists) (gated: unconfirmed, source is paywalled or blocked). The same `quantize` calls ran on a small Dense model: `quantize("int8")`, `"int4"` and `"float8"` all worked in Keras 3.15 (`Model.quantize(mode=None, config=None, filters=None, **kwargs)`), int8 output differed from float32 by at most 0.008 on random data, and the `.keras` file reloaded with the same policies and outputs (int8 kernels stored as `int8`, biases as `float32`).
- Applies to supported layers (`Dense`, `EinsumDense`, `Embedding`): weights stored as int8 with per-channel scales, computed with dequantize-on-the-fly or int8 matmul depending on backend.
- Weight memory: a 1024x1024 Dense held 4,198,400 bytes of weights in float32 and 1,056,768 bytes after `quantize("int8")` (computed from `model.weights`), i.e. about 4x vs float32, so about 2x vs bf16. The int4 and speed figures were not measured (gated: unconfirmed, source is paywalled or blocked).
- `"float8"` sets up FP8 scaling for training/inference on Hopper/Ada GPUs; differs from int8 PTQ (it uses delayed scaling and needs fine-tuning to calibrate) (gated: unconfirmed, source is paywalled or blocked) (the call itself ran on CPU).

## With LoRA
Quantize the base, then enable LoRA to train adapters on top of int8 weights (QLoRA-style). Ran on a quantized Dense layer: `layer.enable_lora(rank=4)` added `lora_kernel_a` and `lora_kernel_b` as the trainable kernel weights (signature `enable_lora(rank, lora_alpha=None, a_initializer='he_uniform', b_initializer='zeros')`) and `fit` ran; the KerasHub `model.backbone.enable_lora(rank=4)` form was not run. Merge only if you re-quantize afterwards (not tested). (gated: unconfirmed, source is paywalled or blocked)

## Saving / loading
`.keras` stores the quantized weights and policies and loading restores them without re-quantizing (ran: same policies and outputs). Weights-only files require building the model with the same quantization first (ran: `load_weights` of a quantized `.weights.h5` into an unquantized model raised `ValueError ... expected 2 variables`).

## Accuracy checks
- Compare logits or task metrics (perplexity on held-out text, accuracy on eval set) before vs after.
- Typical int8 weight-only loss is small for LLMs; int4 more noticeable on small models (gated: unconfirmed, source is paywalled or blocked). Keep first/last layers higher precision if quality drops: calling `layer.quantize("int8")` on only the first layer left the second as `float32` (ran), and re-quantizing a quantized layer raised `already quantized`.

## Limits
- Custom layers need `quantize` support implemented (subclass hooks) or stay in float (not tested) (gated: unconfirmed, source is paywalled or blocked).
- For mobile deployment use LiteRT converter quantization; for TF Serving / TensorRT use their own toolchains. `model.quantize` is mainly for Keras-native inference and fine-tuning memory reduction.
