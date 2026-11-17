---
id: computing-software.ai-ml-engineering.tensorflow-keras.gpu-memory-growth-and-device-placement
name: gpu-memory-growth-and-device-placement
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow, keras, memory-growth, tf-device-placement, gpu-memory, visible-devices]
level: practitioner
status: docs-checked
description: "Control TensorFlow GPU memory with set_memory_growth or memory limits, select visible GPUs, place ops on devices and debug placement and OOM."
sources:
  - https://www.tensorflow.org/guide/gpu
  - https://www.tensorflow.org/api_docs/python/tf/config/experimental/set_memory_growth
  - https://www.tensorflow.org/api_docs/python/tf/debugging/set_log_device_placement
  - https://www.tensorflow.org/guide/gpu_performance_analysis
  - https://www.tensorflow.org/install/docker
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPU memory growth and device placement

By default TensorFlow maps nearly all memory of every visible GPU at startup. Fine for one dedicated job; bad when sharing a GPU with other processes, notebooks or a PyTorch job.

## Memory growth or a hard limit
Must run before any GPU is initialised (top of the program):
```python
gpus = tf.config.list_physical_devices("GPU")
for g in gpus:
    tf.config.experimental.set_memory_growth(g, True)          # allocate as needed, never release
# or a fixed cap per process:
tf.config.set_logical_device_configuration(gpus[0], [tf.config.LogicalDeviceConfiguration(memory_limit=4096)])
```
Env var alternative: `TF_FORCE_GPU_ALLOW_GROWTH=true`. Error "Physical devices cannot be modified after being initialized" means some TF op ran first.
Growth never returns memory to the system during the process; fragmentation can still OOM.

## Choose GPUs
- `CUDA_VISIBLE_DEVICES=1,2 python train.py` limits the GPUs visible to the process.
- In code: `tf.config.set_visible_devices(gpus[1], "GPU")` before initialisation.
- Split one GPU into logical devices for testing distribution code: two `LogicalDeviceConfiguration`s on one physical GPU.

## Placement
```python
tf.debugging.set_log_device_placement(True)       # logs device of every op
with tf.device("/CPU:0"):
    table = tf.lookup.StaticHashTable(...)        # keep big lookup tables on CPU
tf.config.set_soft_device_placement(True)         # let TF pick an existing, supported device if the requested one does not exist
```
Common surprise: ops without a GPU kernel run on the CPU, and ops outside a `tf.function` also run on the host, so tensors are copied back and forth between devices (see the TensorFlow GPU performance analysis guide).

## Debug OOM
- `ResourceExhaustedError: OOM when allocating tensor with shape [...]`: reduce batch size, use mixed precision, gradient checkpointing (`tf.recompute_grad`), or a smaller model.
- `tf.config.experimental.get_memory_info("GPU:0")` returns current and peak bytes; `reset_memory_stats` between experiments.
- Without memory growth each process maps nearly all memory of its visible GPUs, so `nvidia-smi` shows the GPU full.
- Docker: GPUs need `--gpus all`; check `tf.config.list_physical_devices("GPU")` is non-empty and versions of CUDA/cuDNN match the TF build (`tf.sysconfig.get_build_info()`).

## Verify
Run two processes on one GPU with growth enabled; both should start. Log `get_memory_info` peak to size batches.

## Checked

Checked 2026-10-25 against tensorflow/docs master of 2026-10-20 and TensorFlow source (master, 2026-10). Confirmed `set_memory_growth` (memory is not released), `TF_FORCE_GPU_ALLOW_GROWTH`, `LogicalDeviceConfiguration(memory_limit=...)`, `set_visible_devices`, the error strings for changing devices after initialisation (TensorFlow source, `context.py`), `set_soft_device_placement`, `get_memory_info` returning `current` and `peak`, `reset_memory_stats`, `tf.recompute_grad`, `tf.sysconfig.get_build_info`, and `--gpus all` in the Docker install guide. Removed the claim that soft placement is the eager default and the unconfirmed profiler memcpy and `nvidia-smi` statements.

Method: documentation only; no commands were run.
