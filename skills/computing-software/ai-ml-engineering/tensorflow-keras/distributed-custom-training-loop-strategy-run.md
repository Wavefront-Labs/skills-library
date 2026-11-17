---
id: computing-software.ai-ml-engineering.tensorflow-keras.distributed-custom-training-loop-strategy-run
name: distributed-custom-training-loop-strategy-run
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow-keras, tf-distribute, strategy-run, distribute-dataset, custom-training-loop, global-batch-size]
level: practitioner
status: docs-checked
description: "Write a custom training loop under tf.distribute: distribute_datasets_from_function, global vs per-replica batch, loss scaling by global batch, strategy.run and reduce."
sources:
  - https://www.tensorflow.org/tutorials/distribute/custom_training
  - https://www.tensorflow.org/tutorials/distribute/input
  - https://www.tensorflow.org/guide/tpu
  - https://www.tensorflow.org/api_docs/python/tf/distribute/Strategy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom training loops with strategy.run

**Goal:** a hand-written loop that scales across GPUs/TPUs with correct loss scaling and input sharding.

## Input
```python
strategy = tf.distribute.MirroredStrategy()
GLOBAL_BATCH = 64 * strategy.num_replicas_in_sync

def dataset_fn(ctx):
    bs = ctx.get_per_replica_batch_size(GLOBAL_BATCH)
    ds = make_ds().shard(ctx.num_input_pipelines, ctx.input_pipeline_id)
    return ds.batch(bs, drop_remainder=True).prefetch(tf.data.AUTOTUNE)

dist_ds = strategy.distribute_datasets_from_function(dataset_fn)
# simpler: dist_ds = strategy.experimental_distribute_dataset(ds.batch(GLOBAL_BATCH))
```
`experimental_distribute_dataset` is the recommended API when you have no specific sharding needs: it splits each global batch across replicas. `distribute_datasets_from_function` calls your function on the CPU of each worker and leaves batching and sharding to you.

## Model, loss, step
```python
with strategy.scope():
    model = build_model()
    opt = keras.optimizers.Adam(1e-3)
    loss_obj = keras.losses.SparseCategoricalCrossentropy(from_logits=True, reduction="none")
    train_acc = keras.metrics.SparseCategoricalAccuracy()

def compute_loss(y, logits):
    per_ex = loss_obj(y, logits)
    return tf.nn.compute_average_loss(per_ex, global_batch_size=GLOBAL_BATCH)  # divide by GLOBAL batch
    # add regularization: + tf.nn.scale_regularization_loss(tf.add_n(model.losses))

@tf.function
def train_step(it):
    def step_fn(x, y):
        with tf.GradientTape() as tape:
            logits = model(x, training=True)
            loss = compute_loss(y, logits)
        grads = tape.gradient(loss, model.trainable_variables)
        opt.apply_gradients(zip(grads, model.trainable_variables))
        train_acc.update_state(y, logits)
        return loss
    per_replica = strategy.run(step_fn, args=next(it))
    return strategy.reduce(tf.distribute.ReduceOp.SUM, per_replica, axis=None)

it = iter(dist_ds)
for step in range(num_steps):
    loss = train_step(it)
```

## Rules
- Divide by the global batch size: per-replica loss terms are scaled by 1/num_replicas_in_sync and their gradients are summed across replicas, which matches non-distributed training on the global batch. Averaging by the per-replica batch instead makes the summed gradients N times too big.
- Pass `reduction="none"` (or `NONE`) to the loss object and check the loss shape: the loss classes already reduce the last dimension.
- Create variables (model, optimizer, metrics) inside `strategy.scope()`.
- Loop multiple steps inside one `tf.function` (`for _ in tf.range(k): train_step_inner(it)`) to cut host overhead, especially on TPU.
- Use SUM reduce for the already-globally-averaged loss.

## Verify
- [ ] One replica vs N replicas with the same global batch give matching loss curves.

## Checked

Checked 2026-10-25 against tensorflow/docs master of 2026-10-20. Confirmed `distribute_datasets_from_function` with `InputContext.get_per_replica_batch_size` and shard arguments, the recommended status of `experimental_distribute_dataset`, `tf.nn.compute_average_loss` with `global_batch_size`, `tf.nn.scale_regularization_loss`, the 1/num_replicas_in_sync scaling explanation, `strategy.reduce` with `ReduceOp.SUM`, and running several steps per `tf.function` with `tf.range` (TPU guide).

Method: documentation only; no commands were run.
