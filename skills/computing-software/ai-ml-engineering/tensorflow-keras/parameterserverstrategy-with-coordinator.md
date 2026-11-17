---
id: computing-software.ai-ml-engineering.tensorflow-keras.parameterserverstrategy-with-coordinator
name: parameterserverstrategy-with-coordinator
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow, keras, parameterserverstrategy, parameter-server, coordinator, asynchronous-training]
level: practitioner
status: docs-checked
description: "Run asynchronous TensorFlow training with ParameterServerStrategy: chief/worker/ps TF_CONFIG, variable partitioning, dataset_creator and ClusterCoordinator schedule."
sources:
  - https://www.tensorflow.org/tutorials/distribute/parameter_server_training
  - https://www.tensorflow.org/api_docs/python/tf/distribute/experimental/ParameterServerStrategy
  - https://www.tensorflow.org/api_docs/python/tf/distribute/coordinator/ClusterCoordinator
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ParameterServerStrategy with a coordinator

Asynchronous data parallelism: variables live on parameter servers and workers read and update them independently without synchronising with each other. The TensorFlow tutorials point to MultiWorkerMirroredStrategy for synchronous multi-worker training without TPUs.

## Cluster
TF_CONFIG roles: `chief` (runs your program, the coordinator), `worker` (execute steps), `ps` (hold variables), optionally `evaluator`.
```python
# workers and ps run a standard server and block:
server = tf.distribute.Server(cluster_resolver.cluster_spec(), job_name=task_type, task_index=task_id,
                              protocol="grpc", start=True)
server.join()
```

## Chief program
```python
resolver = tf.distribute.cluster_resolver.TFConfigClusterResolver()
partitioner = tf.distribute.experimental.partitioners.MinSizePartitioner(min_shard_bytes=256 << 10, max_shards=NUM_PS)
strategy = tf.distribute.ParameterServerStrategy(resolver, variable_partitioner=partitioner)
with strategy.scope():
    model = build_model(); model.compile(optimizer="adam", loss=..., steps_per_execution=10)
def dataset_fn(input_context):
    bs = input_context.get_per_replica_batch_size(GLOBAL_BATCH)
    return make_dataset().shard(input_context.num_input_pipelines, input_context.input_pipeline_id).batch(bs).repeat()
model.fit(tf.keras.utils.experimental.DatasetCreator(dataset_fn), epochs=5, steps_per_epoch=1000)
```
- The dataset must be created per worker via a function (`DatasetCreator` or `coordinator.create_per_worker_dataset`), and repeated infinitely with `steps_per_epoch` set.
- Variable partitioning splits large variables (embeddings) across PS tasks to balance load.

## Custom loop with ClusterCoordinator
```python
coordinator = tf.distribute.coordinator.ClusterCoordinator(strategy)
per_worker_ds = coordinator.create_per_worker_dataset(dataset_fn)
it = iter(per_worker_ds)
for _ in range(steps):
    coordinator.schedule(train_step, args=(it,))   # async: returns a RemoteValue
coordinator.join()                                 # wait for all scheduled steps
```

## Fault tolerance
- Worker failure: both `Model.fit` and the `ClusterCoordinator` custom loop have built-in fault tolerance; when a worker recovers the coordinator re-creates the datasets on it.
- Parameter server failure: the coordinator raises `UnavailableError` or `AbortedError` immediately; restart the coordinator. Use the `BackupAndRestore` callback with `Model.fit`, or checkpoints in a custom loop, so progress is not lost.

## Trade-offs
- Visitation guarantees: `schedule` and `join` do not support visitation guarantees or exactly-once semantics by default, so with infinite datasets an "epoch" is defined by `steps_per_epoch`.
- Evaluation: inline distributed evaluation scheduled on workers, or sidecar evaluation (`tf.keras.utils.SidecarEvaluator`) with a dedicated evaluator task that reads checkpoints and gives exactly-once evaluation.

## Verify
Kill and restart a worker in a test: training on the chief should continue and the worker should rejoin.

## Checked

Checked 2026-10-25 against tensorflow/docs master of 2026-10-20. Confirmed the chief, worker, ps and evaluator task types, `tf.distribute.Server(..., protocol="grpc")` with `server.join()`, `MinSizePartitioner(min_shard_bytes=256 << 10, max_shards=...)`, `steps_per_execution` in `compile`, `tf.keras.utils.experimental.DatasetCreator`, `Dataset.repeat` with `steps_per_epoch`, `create_per_worker_dataset`, `schedule` and `join`, worker and parameter server failure behaviour, the lack of visitation guarantees, and sidecar evaluation (parameter server training tutorial). Removed the suitability claim, the stale-gradient claim and the throughput expectation.

Method: documentation only; no commands were run.
