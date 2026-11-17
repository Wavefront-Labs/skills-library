---
id: computing-software.ai-ml-engineering.tensorflow-keras.tf-function-retracing-and-input-signature
name: tf-function-retracing-and-input-signature
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow-keras, retracing, input-signature, tf-function, reduce-retracing, autograph]
level: practitioner
status: verified
description: "Stop tf.function retracing from killing performance: what triggers traces, input_signature and reduce_retracing, Python-value pitfalls and detecting retraces."
sources:
  - https://www.tensorflow.org/guide/function
  - https://www.tensorflow.org/api_docs/python/tf/function
  - https://www.tensorflow.org/guide/intro_to_graphs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# tf.function retracing and input_signature

**Symptom:** `WARNING: 5 out of the last 5 calls to <function> triggered tf.function retracing`, and step times are slow and erratic.

## What causes a new trace
- A new input **shape** or **dtype** (ran on TF 2.21: four tensors of length 2, 3, 4, 5 gave `experimental_get_tracing_count() == 4`; a float64 input after float32 added a fifth trace).
- A different **Python value** argument (ran: `f(x, 0)`, `f(x, 1)`, `f(x, 2)` gave 3 traces; Python ints are baked in as constants).
- A new Python object identity passed as argument (e.g. creating a new model each call). A fresh list of tensors with the same structure did not retrace (ran: count 1 over 3 calls).

## Fixes
1. Pass tensors, not Python scalars: `train_step(x, tf.constant(step))` (ran: three `tf.constant(float(s))` steps gave 1 trace; note a Python-int tensor would need the dtype to match `x`).
2. Declare a signature with unknown dims:
```python
@tf.function(input_signature=[tf.TensorSpec([None, None], tf.int32), tf.TensorSpec([None], tf.int32)])
def train_step(x, y): ...
```
3. Or let TF generalize: `@tf.function(reduce_retracing=True)` traces a shape-relaxed version after seeing varying shapes (ran: the same four lengths gave 2 traces instead of 4).
4. Bucket or pad sequences to a few fixed lengths (also required for XLA efficiency).
5. Do not create `tf.Variable`s inside the function on each call; create once outside (or guard with `if self.v is None`). Ran: a function creating a local `tf.Variable` raised `ValueError: tf.function only supports singleton tf.Variables created on the first call`, while the `if self.v is None` guard worked on repeated calls.

## Detect
```python
print(train_step.experimental_get_tracing_count())   # ran on TF 2.21
```
A signature of `[TensorSpec([None, None], tf.int32), TensorSpec([None], tf.int32)]` kept the count at 1 over inputs of sizes 2, 3 and 4 (ran).
Put a Python `print("tracing")` inside the function: it runs only at trace time (use `tf.print` for every execution).

## Python side effects
Python code (list appends, prints, random from `random`/`numpy`) runs only during tracing (ran: `tf.constant(random.random())` returned the same value on every call). Use `tf.print`, `tf.random`, `tf.TensorArray` and TF control flow (AutoGraph converts `if`/`for` on tensors) for runtime behaviour.

## Verify
- [ ] Tracing count stays at 1-2 over an epoch with variable batch contents.
- [ ] Step time after the first step is stable.
