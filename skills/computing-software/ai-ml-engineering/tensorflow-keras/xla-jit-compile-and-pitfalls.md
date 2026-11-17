---
id: computing-software.ai-ml-engineering.tensorflow-keras.xla-jit-compile-and-pitfalls
name: xla-jit-compile-and-pitfalls
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow, keras, jit-compile, xla, tf-function, recompilation]
level: practitioner
status: docs-checked
description: "Use XLA in TensorFlow/Keras via jit_compile=True on compile or tf.function, know its speedups and pitfalls with dynamic shapes, unsupported ops and recompiles."
sources:
  - https://github.com/openxla/xla/blob/main/docs/tf2xla/index.md
  - https://github.com/openxla/xla/blob/main/docs/hlo_dumps.md
  - https://github.com/keras-team/keras/blob/master/keras/src/trainers/trainer.py
  - https://keras.io/api/models/model_training_apis/#compile-method
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# jit_compile=True and XLA pitfalls

XLA compiles TF graphs (or parts of them) ahead of execution into fused kernels.

## Turn it on
```python
model.compile(optimizer="adam", loss="mse", jit_compile=True)   # Keras: compiles train/test/predict steps
@tf.function(jit_compile=True)
def train_step(x, y): ...
```
In Keras 3 `jit_compile="auto"` is the default for `compile`: on the JAX and TensorFlow backends it enables XLA if the model supports it; on the TensorFlow backend it stays off on CPU-only machines and under `tf.distribute`; on the torch backend it means eager execution, and `jit_compile=True` runs `torch.compile` with the `inductor` backend. Auto-clustering for a whole TF program on GPU: `TF_XLA_FLAGS=--tf_xla_auto_jit=2` (add `--tf_xla_cpu_global_jit` for CPU).

## Pitfalls
- **New shapes recompile**: the XLA guide's `recompiled_on_launch` example shows a `jit_compile=True` function being recompiled when the input shape changes. Use `drop_remainder=True` and pad to fixed lengths or a small set of buckets.
- **Must-compile semantics**: either the whole function compiles or an `errors.InvalidArgumentError` is raised. Functions whose tensor dimensions cannot be inferred without running the computation, such as `tf.unique`, cannot compile; move such ops out of the compiled function.
- **Nesting**: a function is compiled if at least one function in its call stack has `jit_compile=True`.
- **Python side effects** run only at trace time (same as any tf.function).

## Inspect
```bash
XLA_FLAGS="--xla_dump_to=DIRECTORY_PATH" python train.py                           # dump HLO
XLA_FLAGS="--xla_dump_hlo_as_text --xla_dump_to=DIRECTORY_PATH" python train.py   # as text
```

## Verify
Benchmark steps/s with and without `jit_compile` after the first epoch (exclude compilation). Compare losses over a few hundred steps; they should match closely.

## Checked

Checked 2026-10-25 against openxla/xla main (2026-10) and Keras master (2026-10-23). Confirmed `tf.function(jit_compile=True)` and Keras `compile(jit_compile=True)`, must-compile semantics with `errors.InvalidArgumentError`, `tf.unique` as a non-compilable example, recompilation on new shapes, nesting behaviour, `TF_XLA_FLAGS=--tf_xla_auto_jit=2` with `--tf_xla_cpu_global_jit`, and `XLA_FLAGS` with `--xla_dump_to` and `--xla_dump_hlo_as_text` (XLA TF2XLA guide and HLO dump guide), and the `jit_compile="auto"` behaviour per backend (`trainer.py`). Removed the speedup range, the unsupported-op list and error string, memory and numerics remarks, and the unconfirmed compilation-cache logging flag.

Method: documentation only; no commands were run.
