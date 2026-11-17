---
id: computing-software.ai-ml-engineering.seldon-core-2.performance-infrastructure-cpu-gpu
name: performance-infrastructure-cpu-gpu
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, performance, cpu, gpu, thread-affinity, omp-num-threads, kmp-affinity, profiling, memory]
level: advanced
status: docs-checked
description: "Pick CPU or GPU for Seldon Core 2 models, profile before moving to GPU, add parallel workers for CPU bottlenecks, set OpenMP thread affinity, and add RAM for memory-heavy models."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/performance-tuning/models/infrastructure-setup.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Infrastructure setup for model performance

## CPU or GPU
- CPUs are generally enough for lightweight models: tree-based models, regression, small neural networks.
- GPUs are recommended for deep learning, large neural networks and LLMs where low latency matters, particularly transformers and CNNs with heavy matrix computation.
- When cost matters, start on CPUs and use a profiler such as py-spy or scalene to find CPU bottlenecks, then move to GPUs if needed.

## CPU specifications
With many concurrent requests a single CPU can bottleneck processing, so raise the parallel workers in your serving solution (for MLServer, see the inference tuning skill). Keep the number of workers from going significantly above the available CPU cores to reduce contention; each worker runs in its own process, which matters most for synchronous models.

For finer control, set thread affinity through environment variables that bind threads to physical processors. For technologies using OpenMP, `KMP_AFFINITY` and `OMP_NUM_THREADS` are examples.

## Memory
More RAM can improve memory-intensive models, such as those with large parameter counts, high-dimensional data processing or complex intermediate computations.

## Checked
Method: docs-checked 2026-11-09 against docs-gb/performance-tuning/models/infrastructure-setup.md (read in full). Dropped an unsupported podSpec note and corrected the worker guidance.
