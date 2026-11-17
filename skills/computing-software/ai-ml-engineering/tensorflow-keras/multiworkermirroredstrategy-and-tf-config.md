---
id: computing-software.ai-ml-engineering.tensorflow-keras.multiworkermirroredstrategy-and-tf-config
name: multiworkermirroredstrategy-and-tf-config
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow, keras, multiworkermirroredstrategy, tf-config, multi-worker, fault-tolerance]
level: practitioner
status: docs-checked
description: "Run synchronous multi-machine TensorFlow training with MultiWorkerMirroredStrategy: TF_CONFIG per worker, auto-sharding, chief-only saving and BackupAndRestore."
sources:
  - https://www.tensorflow.org/tutorials/distribute/multi_worker_with_keras
  - https://www.tensorflow.org/guide/distributed_training#multiworkermirroredstrategy
  - https://www.tensorflow.org/tutorials/distribute/input
  - https://www.tensorflow.org/api_docs/python/tf/keras/callbacks/BackupAndRestore
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MultiWorkerMirroredStrategy and TF_CONFIG

## TF_CONFIG on each machine
```bash
export TF_CONFIG='{"cluster": {"worker": ["10.0.0.1:12345", "10.0.0.2:12345"]},
                   "task": {"type": "worker", "index": 0}}'      # index differs per machine
```
- Same `cluster` on every worker; only `task.index` changes. Worker 0 is the chief (saves checkpoints, writes summaries).
- Set it before creating the strategy, which must be created at program start (before other TF ops).

## Training
```python
strategy = tf.distribute.MultiWorkerMirroredStrategy(
    communication_options=tf.distribute.experimental.CommunicationOptions(
        implementation=tf.distribute.experimental.CommunicationImplementation.NCCL))
GLOBAL_BATCH = 64 * strategy.num_replicas_in_sync
with strategy.scope():
    model = build_and_compile()
callbacks = [tf.keras.callbacks.BackupAndRestore(backup_dir="gs://bucket/backup")]
model.fit(make_dataset(GLOBAL_BATCH), epochs=10, steps_per_epoch=500, callbacks=callbacks)
```

## Data sharding
- Default `AutoShardPolicy.AUTO` tries to shard by FILE and falls back to sharding by DATA when no file-based dataset is detected. FILE suits a number of files much larger than the number of workers with evenly sized data; with AUTO or FILE the per-step batch can be smaller than the global batch when files run out, and `DATA` avoids that.
- Set explicitly:
```python
opts = tf.data.Options()
opts.experimental_distribute.auto_shard_policy = tf.data.experimental.AutoShardPolicy.DATA
ds = ds.with_options(opts)
```
- Pass `steps_per_epoch`; for validation use a repeated dataset with a global batch size and set `validation_steps` (the tutorial's recommendation).

## Saving
All workers must call `model.save` (collective ops may run during save), but only the chief's path is the real one; others write to temp dirs and delete:
```python
task = json.loads(os.environ["TF_CONFIG"])["task"]
path = "gs://bucket/model" if task["index"] == 0 else f"/tmp/worker_{task['index']}"
model.save(path)
```

## Fault tolerance
`BackupAndRestore` saves state at epoch ends (or every `save_freq=N` steps). If a worker is interrupted the whole cluster pauses until it is restarted; the workers then reload the last backup and training continues (the distributed dataset iterator state is re-initialised, not restored).

## Failure modes
- `RuntimeError: Collective ops must be configured at program startup`: TensorFlow ops were created before the strategy; create `MultiWorkerMirroredStrategy` first.
- Workers must be started with the same `cluster` dict; only `task` differs.

## Verify
Each worker logs `num_replicas_in_sync` equal to the total number of GPUs across machines.

## Checked

Checked 2026-10-25 against tensorflow/docs master of 2026-10-20. Confirmed the TF_CONFIG `cluster` and `task` structure with worker 0 as chief, setting TF_CONFIG before the strategy and creating TensorFlow ops after it (and the Collective ops RuntimeError), `CommunicationOptions` with `CommunicationImplementation.NCCL`, the AutoShardPolicy behaviour and its `DATA` workaround, the `validation_steps` advice, chief-versus-temporary-directory saving, and `BackupAndRestore` with `save_freq` (multi-worker tutorial, distributed input guide, distributed training guide). Removed the Kubeflow and Vertex AI claims, the firewall and version-mismatch troubleshooting, and the scaling claim.

Method: documentation only; no commands were run.
