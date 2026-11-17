---
id: computing-software.ai-ml-engineering.tensorflow-keras.keras-learning-rate-schedules
name: keras-learning-rate-schedules
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow-keras, learning-rate-schedule-keras, cosinedecay, warmup, learningratescheduler, reducelronplateau]
level: practitioner
status: gated
description: "Schedule learning rates in Keras: LearningRateSchedule objects (CosineDecay with warmup, PiecewiseConstantDecay), the LearningRateScheduler callback and step vs epoch semantics."
sources:
  - https://keras.io/api/optimizers/learning_rate_schedules/
  - https://keras.io/api/callbacks/learning_rate_scheduler/
  - https://keras.io/api/optimizers/learning_rate_schedules/cosine_decay/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Keras learning-rate schedules

**Two mechanisms:**
1. `LearningRateSchedule` object passed as `learning_rate` to the optimizer: evaluated **every optimizer step**, saved with the optimizer.
2. `LearningRateScheduler` / `ReduceLROnPlateau` callbacks: change the LR **per epoch** (or on plateau) from outside.

Prefer schedule objects for warmup and cosine decay (per-step granularity).

## Warmup + cosine
```python
import keras
steps_per_epoch = len(train_ds)          # or ceil(n / batch)
total = steps_per_epoch * epochs
sched = keras.optimizers.schedules.CosineDecay(
    initial_learning_rate=0.0, decay_steps=total - 1000,
    warmup_target=3e-4, warmup_steps=1000, alpha=0.1)   # alpha = final lr fraction of warmup_target
opt = keras.optimizers.AdamW(learning_rate=sched, weight_decay=0.05)
```
Ran the call above with `decay_steps=9000`: LR was 0 at step 0, 1.5e-4 at 500, 3e-4 at 1000, 1.88e-4 at 5000 and 3e-5 (= alpha x warmup_target) at step 10000. Others (all exist in `keras.optimizers.schedules`): `PiecewiseConstantDecay(boundaries=[10000, 20000], values=[1e-3, 1e-4, 1e-5])`, `ExponentialDecay`, `CosineDecayRestarts`, `PolynomialDecay`.

## Custom schedule
```python
@keras.saving.register_keras_serializable()
class InverseSqrt(keras.optimizers.schedules.LearningRateSchedule):
    def __init__(self, d_model, warmup=4000): self.d, self.w = d_model, warmup
    def __call__(self, step):
        step = keras.ops.cast(step + 1, "float32")
        return self.d ** -0.5 * keras.ops.minimum(step ** -0.5, step * self.w ** -1.5)
    def get_config(self): return {"d_model": self.d, "warmup": self.w}
```

## Callbacks
- `keras.callbacks.LearningRateScheduler(lambda epoch, lr: lr * 0.5 if epoch in (30, 60) else lr)` works only when the optimizer LR is a plain float; with a schedule object Keras 3.15 raised `TypeError: This optimizer was created with a LearningRateSchedule object as its learning_rate constructor argument, hence its learning rate is not settable`. With a float LR and `lambda e, lr: lr*.5 if e == 1 else lr`, `history.history["learning_rate"]` was `[0.001, 0.0005, 0.0005]`.
- `ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=3, min_lr=1e-6)`: also float LRs only; with a schedule object it raised the same `TypeError` once it tried to reduce (ran with `patience=0`).

## Gotchas
- Gradient accumulation changes what a "step" is: the schedule counts optimizer iterations (`optimizer.iterations`; ran: 3 batches gave `iterations == 3`).
- Resuming training: the schedule continues correctly only if the optimizer state (iterations) is restored (use full-model `.keras` checkpoints or `BackupAndRestore`) (gated: unconfirmed, source is paywalled or blocked). Resume behaviour was not run here.

## Verify
- [ ] Log the LR each epoch with a small callback reading `float(keras.ops.convert_to_numpy(model.optimizer.learning_rate))` and plot it.
