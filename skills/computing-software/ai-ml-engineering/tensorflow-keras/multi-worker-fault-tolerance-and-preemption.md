---
id: computing-software.ai-ml-engineering.tensorflow-keras.multi-worker-fault-tolerance-and-preemption
name: multi-worker-fault-tolerance-and-preemption
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow-keras, multi-worker-fault-tolerance, backupandrestore, preemption, multiworkermirroredstrategy, checkpointmanager]
level: practitioner
status: docs-checked
description: "Survive worker failures and preemption in multi-worker TF training: BackupAndRestore, CheckpointManager, PreemptionCheckpointHandler and restart semantics."
sources:
  - https://www.tensorflow.org/tutorials/distribute/multi_worker_with_keras#fault_tolerance
  - https://www.tensorflow.org/api_docs/python/tf/keras/callbacks/BackupAndRestore
  - https://www.tensorflow.org/api_docs/python/tf/distribute/experimental/PreemptionCheckpointHandler
  - https://github.com/keras-team/keras/blob/master/keras/src/callbacks/backup_and_restore.py
  - https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/distribute/failure_handling/failure_handling.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Multi-worker fault tolerance and preemption

**Reality:** with MultiWorkerMirroredStrategy, if a worker is interrupted the whole cluster pauses until that worker is restarted; the other workers also restart and every worker reloads the last saved state. Fault tolerance means restarting from recent state, not continuing with fewer workers.

## Keras fit: BackupAndRestore
```python
callbacks = [keras.callbacks.BackupAndRestore(backup_dir="gs://bucket/job1/backup", save_freq=500)]
model.fit(dist_ds, epochs=20, steps_per_epoch=1000, callbacks=callbacks)
```
- Saves model + optimizer + epoch/step state; on restart with the same `backup_dir`, training resumes at the saved step.
- `save_freq="epoch"` (default) or an integer step count for mid-epoch resume.
- `backup_dir` is where the callback keeps a temporary checkpoint; by default (`delete_checkpoint=True`) it is deleted when training finishes.
- Do not reuse `backup_dir` to store other checkpoints: the callback's checkpoint-tracking file would collide.

## Custom loops: CheckpointManager
```python
ckpt = tf.train.Checkpoint(model=model, optimizer=opt, step=tf.Variable(0))
mgr = tf.train.CheckpointManager(ckpt, directory=write_dir, max_to_keep=3)
ckpt.restore(mgr.latest_checkpoint)
```
All workers must call save (collective), but only the chief should write to the real path; non-chief workers write to temporary dirs that are then deleted (the multi-worker tutorial's `write_filepath` helper pattern).

## Preemption notices
`tf.distribute.experimental.PreemptionCheckpointHandler(cluster_resolver, checkpoint_manager)` watches for a termination signal and saves a checkpoint, with all workers participating, at an agreed step before termination. It only handles terminations with advance notice; it recognises them for CPU, GPU and TPU on Google Borg and CPU and GPU on Google Cloud Platform, and other platforms configure detection with `tf.distribute.experimental.TerminationConfig`:
```python
handler = tf.distribute.experimental.PreemptionCheckpointHandler(resolver, mgr)
for step in range(handler.total_run_calls, num_steps):
    handler.run(distributed_train_step, it)
```

## Orchestration
- Restart policy is external to TensorFlow: your cluster orchestrator or a supervisor script restarts the workers, with the same TF_CONFIG as before.
- Choose `save_freq` as a trade-off between lost work and time spent saving.

## Verify
- [ ] Kill one worker mid-epoch in a test; after restart, the step counter resumes from the last backup, not zero.

## Checked

Checked 2026-10-25 against tensorflow/docs master of 2026-10-20 and TensorFlow source (master, 2026-10). Confirmed the cluster-pauses-and-restarts behaviour, `BackupAndRestore(backup_dir, save_freq="epoch" or int)`, `delete_checkpoint=True` default and the do-not-reuse-`backup_dir` note (multi-worker tutorial and Keras source), all workers calling save with only the chief writing the real path, and `PreemptionCheckpointHandler(cluster_resolver, checkpoint_or_checkpoint_manager, ...)` with `run` and `total_run_calls` and its platform note (TensorFlow source docstring). Removed the Kubernetes and Vertex AI restart claims and the shared-storage requirement.

Method: documentation only; no commands were run.
