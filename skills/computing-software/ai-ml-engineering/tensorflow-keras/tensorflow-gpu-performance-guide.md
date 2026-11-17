---
id: computing-software.ai-ml-engineering.tensorflow-keras.tensorflow-gpu-performance-guide
name: tensorflow-gpu-performance-guide
category: computing-software
field: ai-ml-engineering
product: tensorflow-keras
tags: [tensorflow-keras, tf-gpu-performance, gpu-threads, host-overhead, tf-profiler, input-bound, xla]
level: practitioner
status: docs-checked
description: "Apply the TensorFlow GPU performance guide: profile first, fix input bottlenecks, GPU thread mode, NHWC layout, mixed precision, XLA and reducing host overhead."
sources:
  - https://www.tensorflow.org/guide/gpu_performance_analysis
  - https://www.tensorflow.org/guide/profiler
  - https://www.tensorflow.org/guide/mixed_precision
  - https://www.tensorflow.org/guide/data_performance
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# TensorFlow GPU performance guide

## 1. Profile before tuning
```python
tf.profiler.experimental.start("logs/prof"); train_some_steps(); tf.profiler.experimental.stop()
# or keras.callbacks.TensorBoard(log_dir="logs", profile_batch=(10, 20))
```
TensorBoard Profile tab: **Overview** (step-time breakdown, input %), **Input pipeline analyzer**, **Trace viewer**, **GPU kernel stats**, **TF op stats**. The overview gives a recommendation; start there.

## 2. Input bound (most common)
If the profiler shows the program is input bound: `prefetch(AUTOTUNE)`, parallel `map` and `interleave`, `cache()`, and vectorised mapping (batch before `map`), as described in the tf.data performance guide.

## 3. GPU idle between kernels (host overhead)
Trace viewer shows gaps between GPU kernels while the host thread is busy.
- Ensure training runs in `tf.function` (Keras does); set `steps_per_execution` in `compile` for small models so several steps run per Python call.
- GPU thread mode: `TF_GPU_THREAD_MODE=gpu_private` launches GPU kernels from dedicated threads so they do not queue behind `tf.data` work; it defaults to 2 threads, which `TF_GPU_THREAD_COUNT` changes.
- XLA (`jit_compile=True`) fuses ops, cutting kernel count.

## 4. Device side
- Mixed precision (`mixed_float16` on GPUs): Tensor Cores are used efficiently when fp16 input and output dimensions are divisible by 8.
- GPU kernel stats show which ops are Tensor Core eligible and which kernels actually use Tensor Cores.

## 5. Multi-GPU
- MirroredStrategy: scale global batch with replicas; check all-reduce time in the trace. `NcclAllReduce` is the default cross-device op.
- Use `tf.data` sharding/`experimental_distribute_dataset` so each replica gets distinct data without host bottleneck.

## 6. Avoid hidden syncs and copies
- Metric calculations, Keras callbacks and ops outside a `tf.function` run on the host, and some ops run on the CPU and copy tensors back and forth from the GPU; `tf.debugging.set_log_device_placement(True)` logs where ops run.

## Verify
Record steps/s and GPU utilisation before and after each change, one change at a time.

## Checked

Checked 2026-10-25 against tensorflow/docs master of 2026-10-20. Confirmed the profiler tools and `tf.profiler.experimental.start` (profiler guide), host-side gaps and `TF_GPU_THREAD_MODE=gpu_private` with a default of 2 threads and `TF_GPU_THREAD_COUNT`, `steps_per_execution`, Tensor Core eligibility (fp16 and dimensions divisible by 8) and the GPU kernel stats page, NCCL as the default `MirroredStrategy` all-reduce (GPU performance analysis guide), and prefetch, interleave, parallel map, cache and vectorised mapping (tf.data performance guide). Removed the input-percentage threshold, NHWC claim, hidden-sync claims and the `nvidia-smi dmon` command.

Method: documentation only; no commands were run.
