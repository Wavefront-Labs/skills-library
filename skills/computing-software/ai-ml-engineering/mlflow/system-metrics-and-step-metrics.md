---
id: computing-software.ai-ml-engineering.mlflow.system-metrics-and-step-metrics
name: system-metrics-and-step-metrics
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, experiment-tracking, system-metrics, log-metric, step-metrics, async-logging, gpu-utilization]
level: practitioner
status: gated
description: "Log CPU/GPU/memory system metrics and per-step training metrics in MLflow: enabling sampling, step and timestamp semantics, async/batch logging and keeping metric volume sane."
sources:
  - https://mlflow.org/docs/latest/system-metrics/index.html
  - https://mlflow.org/docs/latest/tracking/tracking-api.html
  - https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.log_metrics
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# System metrics and step-wise metric logging

## System metrics
```python
import mlflow
mlflow.enable_system_metrics_logging()            # or env MLFLOW_ENABLE_SYSTEM_METRICS_LOGGING=true
mlflow.set_system_metrics_sampling_interval(10)   # seconds between samples
mlflow.set_system_metrics_samples_before_logging(3)
with mlflow.start_run(log_system_metrics=True):
    train()
```
Requires `psutil` (without it `start_run(log_system_metrics=True)` raises `Failed to start system metrics monitoring as package psutil is not installed`; tested); GPU metrics need `nvidia-ml-py` (pynvml) and visible NVIDIA devices. Logged as `system/cpu_utilization_percentage`, `system/system_memory_usage_megabytes`, `system/system_memory_usage_percentage`, `system/disk_*` and `system/network_*` keys (all tested on a CPU host); the GPU keys `system/gpu_0_utilization_percentage` and `system/gpu_0_memory_usage_megabytes` were not run (no GPU) (gated: unconfirmed, source is paywalled or blocked). `MLFLOW_ENABLE_SYSTEM_METRICS_LOGGING=true` also enabled logging (tested). In multi-node training, call `mlflow.set_system_metrics_node_id(f"node-{rank}")` on each node so series are prefixed per node instead of interleaving (tested: keys became `system/node-0/cpu_utilization_percentage`).

Use them to spot data-loader bottlenecks (low GPU util, high CPU), memory leaks (rising RAM over epochs) and OOM headroom.

## Step metrics
```python
for step, batch in enumerate(loader):
    loss = train_step(batch)
    if step % 50 == 0:
        mlflow.log_metrics({"train/loss": loss, "lr": sched.get_last_lr()[0]}, step=step, synchronous=False)
mlflow.log_metric("val/auc", auc, step=epoch)
```
- `step` is the x-axis you choose (global step or epoch) - be consistent per key; mixing epoch and step values on one key produces nonsense charts.
- Logging every step of a million-step run means a million DB rows per key; sample every N steps.
- `synchronous=False` (present in the 3.17.1 `log_metrics` signature; the 2.8 introduction version was not checked (gated: unconfirmed, source is paywalled or blocked)) queues logging in a background thread so training is not blocked by tracking-server latency; call `mlflow.flush_async_logging()` or end the run to drain.
- Metric names allow `/` for grouping in the UI; keys are case-sensitive.
- Retried/resumed training: continue logging with the same run id (`mlflow.start_run(run_id=...)`) and true global steps so curves stay continuous.

## Verify
- [ ] Run page shows system metrics charts with GPU series on a GPU job.
- [ ] Training throughput with logging enabled is within a few percent of logging disabled.
