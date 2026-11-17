---
id: computing-software.ai-ml-engineering.tensorflow-keras.tf-data-service-disaggregated-preprocessing
name: tf-data-service-disaggregated-preprocessing
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow-keras, tf-data-service, distributed-preprocessing, dispatcher, worker, input-pipeline]
level: practitioner
status: docs-checked
description: "Offload tf.data preprocessing to remote CPU workers with tf.data service: dispatcher and workers, distribute(), processing modes, sharding policies and sizing."
sources:
  - https://www.tensorflow.org/api_docs/python/tf/data/experimental/service
  - https://www.tensorflow.org/tutorials/distribute/input#tfdata_service
  - https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/data/experimental/ops/data_service_ops.py
  - https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/data/experimental/service/server_lib.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# tf.data service

When accelerators wait for input and the host CPU is maxed out, run preprocessing on a pool of CPU machines and stream ready batches to the trainers.

## Components
```python
# dispatcher (one)
d = tf.data.experimental.service.DispatchServer(
        tf.data.experimental.service.DispatcherConfig(port=5050, work_dir="gs://bucket/dispatcher", fault_tolerant_mode=True))
# workers (many CPU VMs)
w = tf.data.experimental.service.WorkerServer(
        tf.data.experimental.service.WorkerConfig(dispatcher_address="dispatcher:5050", worker_address="this-host:5051", port=5051))
d.join() / w.join()
```
## Trainer side
```python
ds = build_pipeline()              # list_files -> interleave -> map(decode/augment) -> batch
ds = ds.apply(tf.data.experimental.service.distribute(
        processing_mode=tf.data.experimental.service.ShardingPolicy.OFF,
        service="grpc://dispatcher:5050", job_name="train-run-17"))
ds = ds.prefetch(tf.data.AUTOTUNE)
```
Everything before `distribute` runs on workers; everything after runs locally.

## Processing modes
- `ShardingPolicy.OFF` (the string `"parallel_epochs"`): no sharding, each worker produces the entire dataset; shuffle the dataset non-deterministically so workers differ. Restarted or newly joined workers start from the beginning.
- `ShardingPolicy.DYNAMIC` (the string `"distributed_epoch"`): splits are handed out dynamically at runtime and data is produced non-deterministically. The guarantee is at-most-once visitation: no example repeats, but some may be missed if a worker restarts while processing a file. Works well with clusters of varying size.
- `FILE` / `DATA` / `FILE_OR_DATA` / `HINT` (static sharding): require a fixed worker list (`DispatcherConfig(worker_addresses=...)`) and each client reading only from its local worker. `FILE` needs at least as many files as workers (a runtime error otherwise); `DATA` needs the dataset to produce elements in a deterministic order.
- 
## Sizing
Measure the throughput (elements/s) of the pipeline up to `distribute` on one host, compare it with the rate the trainers need, and add workers until step time stops improving.

## Gotchas
- Preprocessed elements move over the network; `compression` defaults to `"AUTO"` (the service runtime decides), with `"SNAPPY"` to force snappy and `None` for no compression.
- Data is produced non-deterministically with OFF and DYNAMIC; for evaluation where order or exact coverage matters, consider static sharding.
- `job_name` lets multiple datasets (for example several trainers) share one job; `fault_tolerant_mode=True` on the dispatcher requires `work_dir`.

## Checked

Checked 2026-10-25 against TensorFlow source (master, 2026-10). Checked against the TensorFlow source docstrings: the `ShardingPolicy` members and semantics (OFF, DYNAMIC at-most-once, static FILE, DATA, FILE_OR_DATA, HINT and their fixed-worker-list requirement), the mapping of `parallel_epochs` to OFF and `distributed_epoch` to DYNAMIC, `compression` values and the `"AUTO"` default, `job_name` sharing, and `DispatcherConfig` (`port`, `work_dir`, `fault_tolerant_mode` requiring `work_dir`, `worker_addresses`) and `WorkerConfig`. Corrected DYNAMIC from exactly-once to at-most-once and removed the OFF default claim, the worker-count multiplier, the serialisation rule and the BackupAndRestore remark.

Method: documentation only; no commands were run.
