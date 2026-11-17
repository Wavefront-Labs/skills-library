---
id: computing-software.ai-ml-engineering.llama-cpp.server-load-modes-mmap-numa
name: server-load-modes-mmap-numa
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, mmap, mlock, numa, load-mode]
level: advanced
status: docs-checked
description: "Pick how model weights are loaded with -lm and tune NUMA, threads and lazy loading."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md", "https://github.com/ggml-org/llama.cpp/blob/master/docs/development/token_generation_performance_tips.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Load modes, NUMA and threads

`-lm, --load-mode MODE` selects how weights are read: `auto`, `none`, `mmap`, `mlock`, `mmap+mlock`, or `dio`. `auto` (default) uses mmap unless a device does not support it; `dio` uses DirectIO if available. Env `LLAMA_ARG_LOAD_MODE` takes the same values.

- `-lzm, --lazy-mode on|auto|off`: read the rows of certain tensors (for example per-layer embeddings) from disk on demand instead of keeping them resident; requires mmap. `auto` (default) does this only for tensors larger than 4 GiB.
- `--numa distribute|isolate|numactl`: NUMA optimization. `distribute` spreads across all nodes, `isolate` uses only the node where execution started, `numactl` follows the CPU map given by `numactl`. If you ran without it before, the README recommends dropping the system page cache first.
- `-t, --threads N`: generation threads; `-tb, --threads-batch N`: prompt/batch threads (defaults to `-t`).
- `-C, --cpu-mask`, `-Cr, --cpu-range`, `--cpu-strict`, `--prio`, `--poll` tune CPU affinity and scheduling.
- `--threads-http N`: HTTP threads.

The performance-tips doc recommends setting `-t` to the number of physical cores, and notes `-t 1` is a diagnostic to detect thread oversaturation.

## Checked

2026-11-08. Confirmed in the llama.cpp server README: --load-mode values and defaults, --lazy-mode, --numa types, -t, -tb, the CPU affinity and priority flags and --threads-http; in the performance-tips doc the physical-cores advice and the -t 1 diagnostic. Removed: the old mmap, mlock and direct-io flag names, the drop_caches command and the LoRA and memory-mapping sentence (none stated in the pages).

Method: docs-only read of cited pages, 2026-11-08
