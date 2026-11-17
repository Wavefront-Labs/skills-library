---
id: computing-software.ai-ml-engineering.tensorflow-keras.debugging-tf-function-run-functions-eagerly
name: debugging-tf-function-run-functions-eagerly
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow-keras, run-functions-eagerly, tf-print, tf-function, debugging, autograph]
level: practitioner
status: verified
description: "Debug code inside tf.function and Keras fit: run_functions_eagerly, run_eagerly=True, tf.print vs print, AutoGraph conversion errors and graph-only bugs."
sources:
  - https://www.tensorflow.org/guide/function#debugging
  - https://www.tensorflow.org/api_docs/python/tf/config/run_functions_eagerly
  - https://www.tensorflow.org/guide/autograph
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Debugging tf.function

**Problem:** breakpoints and prints do not behave inside graph code; errors point at generated AutoGraph code.

## Switch to eager temporarily
```python
tf.config.run_functions_eagerly(True)     # every tf.function runs as plain Python
# ... reproduce the bug with pdb / prints / .numpy()
tf.config.run_functions_eagerly(False)
```
For Keras: `model.compile(..., run_eagerly=True)`. If the bug disappears in eager mode, it is a graph-only issue (Python side effects, retracing, shape inference, control flow).

## Printing
- `print(x)` inside tf.function runs once at trace time and shows a symbolic tensor (ran: the second call printed nothing; under `run_functions_eagerly(True)` it printed real values).
- `tf.print(x, summarize=-1, output_stream=sys.stderr)` runs every call and prints values.
- `tf.debugging.assert_shapes`, `tf.debugging.assert_all_finite(x, "msg")`, `tf.debugging.assert_equal` check at runtime in graphs.

## AutoGraph errors
- `OperatorNotAllowedInGraphError: Using a symbolic tf.Tensor as a Python bool is not allowed`: a Python `if tensor:` in code AutoGraph did not convert. Reproduced with `@tf.function(autograph=False)` and with a helper decorated `@tf.autograph.experimental.do_not_convert`. A plain `if`/`else` inside `try/except` was still converted and worked. Use `tf.cond` or make sure the function is converted. A one-armed `if x>0: return x` in a traced function raises `ValueError: the else branch must also...`.
- Loops over Python lists are unrolled at trace time; loops over tensors (`tf.range`) become `tf.while_loop`.
- Inspect the converted code: `print(tf.autograph.to_code(fn.python_function))`.
- `tf.autograph.set_verbosity(3, True)` logs conversion decisions (very verbose: it also dumps Keras internals during `fit`).

## Shapes
Graph mode may have unknown static shapes (`None`); use `tf.shape(x)` (dynamic) instead of `x.shape` (static) for runtime sizes.

## Verify
- [ ] The fixed function produces the same results with `run_functions_eagerly(True)` and `False`.
