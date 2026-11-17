---
id: computing-software.ai-ml-engineering.tensorflow-keras.keras-mixed-precision-policy-and-loss-scaling
name: keras-mixed-precision-policy-and-loss-scaling
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow, keras, mixed-float16, loss-scale-optimizer, mixed-precision, mixed-bfloat16]
level: practitioner
status: docs-checked
description: "Enable Keras mixed precision with mixed_float16 or mixed_bfloat16 policies, keep outputs in float32, and handle LossScaleOptimizer in custom training loops."
sources:
  - https://www.tensorflow.org/guide/mixed_precision
  - https://keras.io/api/mixed_precision/policy/
  - https://keras.io/api/mixed_precision/loss_scale_optimizer/
  - https://www.tensorflow.org/guide/gpu_performance_analysis
  - https://github.com/keras-team/keras/blob/master/keras/src/optimizers/loss_scale_optimizer.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keras mixed precision policy and loss scaling

## Enable
```python
keras.mixed_precision.set_global_policy("mixed_float16")   # NVIDIA GPUs with compute capability 7.0+ benefit most
# keras.mixed_precision.set_global_policy("mixed_bfloat16") # TPUs and CPUs; no loss scaling needed
```
Layers then compute in float16/bfloat16 while variables stay float32 (`layer.compute_dtype` vs `layer.variable_dtype`). Set the policy before building the model.

## Keep the output in float32
```python
x = layers.Dense(num_classes)(x)
outputs = layers.Activation("softmax", dtype="float32")(x)   # or Dense(..., dtype="float32")
```
Softmax/sigmoid and losses in float16 overflow or lose precision. With `from_logits=True` losses, cast logits: `layers.Activation("linear", dtype="float32")`.

## Loss scaling
- `model.fit` with `mixed_float16`: Keras wraps the optimizer in `LossScaleOptimizer` automatically (dynamic scaling).
- Custom training loop: do it yourself.
```python
opt = keras.mixed_precision.LossScaleOptimizer(keras.optimizers.Adam())
@tf.function
def step(x, y):
    with tf.GradientTape() as tape:
        loss = loss_fn(y, model(x, training=True))
        scaled = opt.scale_loss(loss)          # tf.keras 2.x: opt.get_scaled_loss(loss)
    grads = tape.gradient(scaled, model.trainable_variables)
    # Keras 3: apply() unscales internally; tf.keras 2.x: grads = opt.get_unscaled_gradients(grads)
    opt.apply_gradients(zip(grads, model.trainable_variables))
```
Steps with inf/NaN gradients are skipped and the scale lowered. bfloat16 does not need scaling.

## When it speeds up
- NVIDIA GPUs with compute capability 7.0 or higher (Tensor Cores) benefit most; older GPUs get no math speedup, although memory and bandwidth savings can help some models. Use `mixed_bfloat16` on TPUs and CPUs.
- Tensor Cores are used efficiently when fp16 input and output dimensions are divisible by 8.
- Input-bound pipelines see no gain; check the profiler.
- The TensorFlow guide says mixed precision can improve performance by up to 3x on TPUs, NVIDIA GPUs with compute capability 7.0+ and Intel CPUs with AMX.

## Pitfalls
- Custom layers that create tensors with a hardcoded dtype can mix dtypes; use `self.compute_dtype` or `keras.ops.cast(x, self.compute_dtype)`.
- Gradients can underflow in float16, which is why `mixed_float16` needs loss scaling; the model output (and any final softmax) should stay float32.

## Verify
`model.layers[i].compute_dtype` shows float16; the loss curve matches the float32 run; the profiler's GPU kernel stats show which kernels use Tensor Cores.

## Checked

Checked 2026-10-25 against tensorflow/docs master of 2026-10-20 and Keras source (master, 2026-10-23). Confirmed `mixed_float16` and `mixed_bfloat16`, `set_global_policy` and `set_dtype_policy` in `keras.mixed_precision`, float32 output layers (`Activation(..., dtype="float32")`), automatic loss scaling in `fit` for `mixed_float16` (`auto_scale_loss` in `compile`), `LossScaleOptimizer.scale_loss` and an `apply()` that unscales gradients, no scaling for bfloat16, skipped steps on Inf or NaN gradients, the compute capability 7.0 guidance and the up-to-3x statement (TensorFlow mixed precision guide), and the divisible-by-8 Tensor Core rule (GPU performance analysis guide). Removed the typical-speedup, epsilon, saved-model and kernel-name claims.

Method: documentation only; no commands were run.
