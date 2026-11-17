---
id: computing-software.ai-ml-engineering.tensorflow-keras.custom-training-loops-and-callbacks
name: custom-training-loops-and-callbacks
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow, keras, custom-training-loop, gradienttape, train-step, callbacks, tf-function, graph-mode, mixed-precision, early-stopping, model-checkpoint, custom-callback]
level: advanced
status: verified
description: "Write a custom Keras training loop with GradientTape or an overridden train_step, and callbacks (EarlyStopping, ModelCheckpoint) correctly, avoiding the eager/graph-mode traps."
sources:
  - https://www.tensorflow.org/guide/keras/writing_a_training_loop_from_scratch
  - https://www.tensorflow.org/guide/keras/writing_your_own_callbacks
  - https://www.tensorflow.org/guide/function
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom Keras training loops, `train_step`, and callbacks

**Goal:** drop below `model.fit()` when you need custom loss computation, multiple optimizers, or non-standard metrics — without the graph-mode/`tf.function` traps that make a custom loop silently slower or behave differently than eager debugging suggested.

## 1. Two ways to customize, and when each is right
- **Override `train_step`** (keep `model.fit()`'s outer loop, callbacks, progress bar — override only what happens per batch): the right choice when you need a custom loss/gradient computation but still want `fit()`'s callback system, validation loop, and distribution-strategy integration for free.
```python
class CustomModel(tf.keras.Model):
    def train_step(self, data):
        x, y = data
        with tf.GradientTape() as tape:
            y_pred = self(x, training=True)
            loss = self.compute_loss(y=y, y_pred=y_pred)
        grads = tape.gradient(loss, self.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.trainable_variables))
        for m in self.metrics:
            if m.name == "loss":
                m.update_state(loss)
            else:
                m.update_state(y, y_pred)
        return {m.name: m.result() for m in self.metrics}
```
- **Full custom loop with `GradientTape`** (write the `for epoch / for batch` loop yourself): needed for genuinely unusual control flow — multiple optimizers for different model parts (GAN-style alternating updates), custom multi-stage losses that don't fit `compiled_loss`, or manual gradient accumulation. You lose `fit()`'s callbacks/validation/progress-bar machinery and must reimplement what you need (or call `tf.keras.callbacks.CallbackList(callbacks, model=model)` manually: `on_train_begin()` and `on_epoch_end(epoch, logs)` ran).

## 2. The `tf.function`/graph-mode traps
- `compiled_loss` and `compiled_metrics` still ran in Keras 3.15 but emit a `UserWarning` that they are deprecated in favour of `compute_loss` and per-metric `update_state`; the `train_step` above ran and returned `loss` and `accuracy`.
- Wrap the per-step function in `@tf.function` for performance: without it, a hand-written loop runs eagerly, one op at a time with no graph optimisation, and is usually slower (measure on your model).
- **Python-side side effects inside a `@tf.function`-decorated step run only on the first trace**, not every call — a Python `print()`, a Python list `.append()`, or incrementing a plain Python counter inside the traced function executes once during tracing and never again during actual graph execution (ran: three calls gave one `py print`, `len(log)==1`, `cnt==1`, but `tf.print` fired three times). Use `tf.print` for logging inside a traced function, and `tf.Variable` (not a Python int) for any counter that must update every call.
- **Retracing**: `tf.function` retraces (recompiles the graph) whenever it's called with a new input signature (different shape, different Python-value argument) — passing a Python scalar (like a loop index) as an argument instead of a `tf.Tensor` causes a retrace on every distinct value (ran: 4 Python ints traced 4 times, 4 tensors traced once), silently destroying the performance benefit `tf.function` was supposed to provide. Use `input_signature` or pass genuinely dynamic values as tensors, not Python values, if they vary per call.
- Debugging a traced function is harder than eager code — if a custom `train_step` or loop misbehaves, temporarily remove `@tf.function` to debug in eager mode with normal Python debugging tools, then re-add it once correct; don't try to debug graph-mode tracing issues by reading error messages alone.

## 3. Callbacks: writing your own and the ones everyone should use
- Built-ins worth defaulting to: `EarlyStopping(monitor="val_loss", patience=N, restore_best_weights=True)` — `restore_best_weights` defaults to `False` (checked), so by default training stops with the *last* epoch's weights, not the best ones.
- `ModelCheckpoint(save_best_only=True, monitor="val_...")` — picking the wrong `monitor` (e.g. training loss instead of a validation metric) saves checkpoints that look good on the metric that's always improving with more training, not the metric that reflects generalization.
- A custom callback subclasses `tf.keras.callbacks.Callback` and overrides the hooks it needs (`on_epoch_end`, `on_train_batch_end`, etc.) — inside `on_epoch_end(self, epoch, logs=None)`, `logs` is the dict of metric values for that epoch; mutating it in place is how custom callbacks (e.g. a custom LR schedule logger) add their own values to what gets passed to subsequent callbacks and to history — declare `logs=None` as a default; in Keras 3.15 `on_train_begin` received an empty dict `{}` (not `None`) and `on_epoch_end` received `['loss', 'val_loss']`, but older versions or other hooks may pass `None`, so guard for it.
- If using a custom full training loop (not `train_step`), callbacks aren't invoked automatically — you must call them yourself (`callback_list.on_epoch_end(epoch, logs)` etc.) at the right points, or reimplement the behavior directly; a common bug is silently losing early stopping/checkpointing entirely when migrating from `fit()` to a fully custom loop.

## Verify
- [ ] Custom `train_step`/loop decorated with `@tf.function` where performance matters, and confirmed not retracing on every call (check with a trace count or timing before/after).
- [ ] No Python-side-effect logging/counting left inside a traced function; `tf.print`/`tf.Variable` used instead.
- [ ] `EarlyStopping` uses `restore_best_weights=True` if "best" weights are actually expected to be kept.
- [ ] `ModelCheckpoint`/`EarlyStopping` monitor a validation metric, not a training-only metric.
- [ ] If callbacks were migrated from `fit()` to a custom loop, each one's behavior (checkpointing, early stopping, logging) was re-verified to actually still fire.
