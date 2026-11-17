---
id: computing-software.ai-ml-engineering.tensorflow-keras.finding-nan-with-check-numerics
name: finding-nan-with-check-numerics
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow-keras, check-numerics, nan-debugging, debugger-v2, enable-check-numerics, inf, numerical-stability]
level: practitioner
status: verified
description: "Locate the first op producing NaN or Inf in TensorFlow with tf.debugging.enable_check_numerics and Debugger V2 dumps, then fix the usual causes in Keras models."
sources:
  - https://www.tensorflow.org/api_docs/python/tf/debugging/enable_check_numerics
  - https://www.tensorflow.org/tensorboard/debugger_v2
  - https://www.tensorflow.org/api_docs/python/tf/debugging/experimental/enable_dump_debug_info
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Finding NaN with check_numerics

## Fastest: enable_check_numerics
```python
tf.debugging.enable_check_numerics()     # call at program start, before building/tracing
model.fit(ds, epochs=1)
```
Every float op output (eager and inside tf.function) is checked; the first NaN/Inf raises `InvalidArgumentError` (ran on `tf.math.log([1,0,-1])` in a tf.function: `Detected Infinity or NaN in output 0 of graph op "Log"`, with the node, the Python stack of the op's creation and the input tensor). Slows training a lot: reproduce on a few steps only.

Keras-level helpers: `keras.callbacks.TerminateOnNaN()` stops training but does not localise. `tf.debugging.check_numerics(t, "msg")` asserts a specific tensor.

## Deeper: Debugger V2
```python
tf.debugging.experimental.enable_dump_debug_info("/tmp/tfdbg2", tensor_debug_mode="FULL_HEALTH", circular_buffer_size=-1)   # signature checked; call disable_dump_debug_info() when done
# run until NaN, then
# tensorboard --logdir /tmp/tfdbg2  -> Debugger V2 tab
```
The Debugger V2 TensorBoard tab shows alerts (first NaN/Inf op), the graph execution timeline and source code (per the TensorFlow Debugger V2 guide; not opened here, the dump call itself ran). Good when the failing op is generic (e.g. `Mul`) and you need upstream context.

## Usual causes and fixes
| First bad op | Cause | Fix |
|---|---|---|
| `Log`, `Xlogy`, custom cross-entropy | log(0) | use `from_logits=True` losses; clip `tf.math.log(x + eps)` |
| `Softmax`/`Exp` | large logits overflow (float16) | keep logits float32 (`dtype="float32"` on last layer), stable losses |
| `RealDiv`, normalisation | divide by zero / tiny variance | add epsilon, check empty batches/masks |
| `Sqrt`, `Pow` | negative inputs or gradient at 0 | clamp, add eps inside sqrt |
| Gradients only | exploding gradients | lower LR, `clipnorm` in optimizer, warm-up |
| Mixed precision only | float16 overflow | loss scaling (`compile` has `auto_scale_loss=True` by default in Keras 3.15), or use bfloat16 |
| From the first batch | bad data | `tf.debugging.assert_all_finite` on inputs; check for NaN in source data |

## Workflow
1. Reproduce with a fixed seed and small number of steps.
2. Check inputs and labels for NaN.
3. Enable check_numerics, get the op and stack.
4. If in the backward pass, inspect gradients per variable (`tape.gradient` then `tf.math.reduce_any(tf.math.is_nan(g))`).
5. Fix, then turn check_numerics off with `tf.debugging.disable_check_numerics()` (it stays active for the process otherwise; both functions exist in TF 2.21).
