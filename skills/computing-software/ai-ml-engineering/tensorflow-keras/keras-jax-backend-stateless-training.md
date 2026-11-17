---
id: computing-software.ai-ml-engineering.tensorflow-keras.keras-jax-backend-stateless-training
name: keras-jax-backend-stateless-training
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [keras, keras-3, keras-jax-backend, jax, stateless-call, stateless-apply, jit, custom-training-loop]
level: practitioner
status: docs-checked
description: "Write custom training loops for Keras 3 on JAX: stateless_call, optimizer.stateless_apply, jax.value_and_grad with jit, syncing state back, and train_step overrides."
sources:
  - https://keras.io/guides/writing_a_custom_training_loop_in_jax/
  - https://keras.io/guides/custom_train_step_in_jax/
  - https://docs.jax.dev/en/latest/jit-compilation.html
  - https://docs.jax.dev/en/latest/gpu_memory_allocation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stateless training with the Keras JAX backend

**Goal:** write a fast `jax.jit`-compiled training step for a Keras model, which requires passing all state explicitly because JAX functions must be pure.

## Training loop
```python
import os; os.environ["KERAS_BACKEND"] = "jax"
import jax, keras

model = build_model()
optimizer = keras.optimizers.AdamW(1e-3)
loss_fn = keras.losses.SparseCategoricalCrossentropy(from_logits=True)
optimizer.build(model.trainable_variables)

def compute_loss(trainable, non_trainable, x, y):
    logits, non_trainable = model.stateless_call(trainable, non_trainable, x, training=True)
    return loss_fn(y, logits), non_trainable

grad_fn = jax.value_and_grad(compute_loss, has_aux=True)

@jax.jit
def train_step(state, x, y):
    trainable, non_trainable, opt_vars = state
    (loss, non_trainable), grads = grad_fn(trainable, non_trainable, x, y)
    trainable, opt_vars = optimizer.stateless_apply(opt_vars, grads, trainable)
    return loss, (trainable, non_trainable, opt_vars)

state = ([v.value for v in model.trainable_variables],
         [v.value for v in model.non_trainable_variables],
         [v.value for v in optimizer.variables])
for x, y in dataset:
    loss, state = train_step(state, x, y)

# write the trained values back into the Keras model before saving
trainable, non_trainable, _ = state
for v, val in zip(model.trainable_variables, trainable): v.assign(val)
for v, val in zip(model.non_trainable_variables, non_trainable): v.assign(val)
model.save("model.keras")
```
- `stateless_call` returns updated non-trainable state (BatchNorm moving stats, RNG seeds); forgetting to thread it through means BN statistics never update.
- Metrics are also stateful: use `metric.stateless_update_state(metric_vars, y, pred)` inside the jitted step, or compute metrics outside it.

## Overriding train_step instead (keeps fit())
On JAX, `Model.train_step(self, state, data)` receives the state tuple `(trainable_variables, non_trainable_variables, optimizer_variables, metrics_variables)` and returns `(logs, state)`; implement it with `self.stateless_call` and `self.optimizer.stateless_apply`, then `fit()` handles jit, callbacks and logging.

## Gotchas
- Python side effects (such as appending to a list) inside the jitted step are not captured by JAX: they run at trace time only.
- Don't call `model(x)` (stateful) inside the jitted function; always use `stateless_call`.
- Memory: JAX preallocates 75% of GPU memory by default; set `XLA_PYTHON_CLIENT_PREALLOCATE=false` or lower `XLA_PYTHON_CLIENT_MEM_FRACTION` when sharing a GPU.

## Verify
- [ ] Loss decreases and matches a `fit()` run on the same data/seed closely.
- [ ] Non-trainable variables (BN stats) change during training.
- [ ] Saved model after write-back reproduces the jitted predictions.

## Checked

Checked 2026-10-25 against Keras 3 (keras-team/keras master of 2026-10-23, keras-io of 2026-09-23) and the JAX docs (jax-ml/jax master, 2026-10). Confirmed `stateless_call`, `jax.value_and_grad(..., has_aux=True)`, `optimizer.build`, `optimizer.variables`, `optimizer.stateless_apply`, writing values back with `variable.assign`, `metric.stateless_update_state` and the `train_step(self, state, data)` state tuple and `(logs, state)` return (both Keras JAX guides); side effects not captured by `jax.jit` and the 75% GPU preallocation with its two environment variables (JAX documentation). Removed the unconfirmed recompilation bullet.

Method: documentation only; no commands were run.
