---
id: computing-software.ai-ml-engineering.tensorflow-keras.mirroredstrategy-single-host-multi-gpu
name: mirroredstrategy-single-host-multi-gpu
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow, keras, mirrored-strategy-scope, mirroredstrategy, tf-distribute, multi-gpu]
level: practitioner
status: docs-checked
description: "Train Keras models on several GPUs of one host with tf.distribute.MirroredStrategy: scope placement, global batch size, dataset distribution and custom loop loss scaling."
sources:
  - https://www.tensorflow.org/guide/distributed_training
  - https://www.tensorflow.org/tutorials/distribute/keras
  - https://www.tensorflow.org/tutorials/distribute/custom_training
  - https://www.tensorflow.org/tutorials/distribute/save_and_load
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MirroredStrategy on one host

Synchronous data parallelism: a replica per GPU, gradients all-reduced (NCCL by default) each step. In Keras 3 with the JAX backend use `keras.distribution.DataParallel` instead; this skill is for TF / tf.keras.

## Keras fit
```python
strategy = tf.distribute.MirroredStrategy()                 # all visible GPUs
print("replicas:", strategy.num_replicas_in_sync)
GLOBAL_BATCH = 64 * strategy.num_replicas_in_sync
with strategy.scope():                                       # create model, optimizer, metrics inside
    model = build_model()
    model.compile(optimizer=keras.optimizers.Adam(1e-3),
                  loss="sparse_categorical_crossentropy", metrics=["accuracy"])
ds = make_dataset().batch(GLOBAL_BATCH).prefetch(tf.data.AUTOTUNE)
model.fit(ds, epochs=10)                                     # fit itself can be outside scope
```
- Batch the dataset with the **global** batch; Keras splits it across replicas.
- Create the model, optimizer and metrics inside `strategy.scope()` so their variables are mirrored.
- Loading a saved model for continued training: call `load_model` inside the scope.

## Custom training loop
```python
dist_ds = strategy.experimental_distribute_dataset(ds)
with strategy.scope():
    loss_obj = keras.losses.SparseCategoricalCrossentropy(reduction="none")
def compute_loss(y, logits):
    per_ex = loss_obj(y, logits)
    return tf.nn.compute_average_loss(per_ex, global_batch_size=GLOBAL_BATCH)   # divide by GLOBAL batch
@tf.function
def train_step(inputs):
    def step_fn(x, y):
        with tf.GradientTape() as tape:
            loss = compute_loss(y, model(x, training=True))
        opt.apply_gradients(zip(tape.gradient(loss, model.trainable_variables), model.trainable_variables))
        return loss
    per_replica = strategy.run(step_fn, args=inputs)
    return strategy.reduce(tf.distribute.ReduceOp.SUM, per_replica, axis=None)
```
Dividing by the per-replica batch instead of the global batch multiplies gradients by the replica count.

## Tuning
- Restrict GPUs: `MirroredStrategy(devices=["/gpu:0", "/gpu:1"])` or `CUDA_VISIBLE_DEVICES`.
- Override cross-device communication with `cross_device_ops`: `tf.distribute.HierarchicalCopyAllReduce()` or `tf.distribute.ReductionToOneDevice()` are the alternatives to the default `tf.distribute.NcclAllReduce`.
- Input pipeline must keep up with N GPUs: parallel map, prefetch, cache.
- Tune the learning rate for the larger global batch (the Keras tutorial notes that larger batches allow a larger learning rate, within limits).

## Verify
`nvidia-smi` shows all GPUs busy; steps per epoch drop by the replica count; accuracy is comparable to a single-GPU run with the same effective batch size and learning rate.

## Checked

Checked 2026-10-25 against tensorflow/docs master of 2026-10-20. Confirmed that `MirroredStrategy()` uses all visible GPUs with NCCL, `devices=[...]`, the `cross_device_ops` alternatives to `NcclAllReduce`, model building and compiling inside `strategy.scope()`, global-batch scaling of the loss with `tf.nn.compute_average_loss`, `strategy.run`, `strategy.reduce(ReduceOp.SUM, ..., axis=None)`, and loading saved models inside a strategy scope. Removed the square-root learning-rate scaling, the Windows NCCL claim and the unconfirmed error text.

Method: documentation only; no commands were run.
