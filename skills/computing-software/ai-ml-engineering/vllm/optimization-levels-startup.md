---
id: computing-software.ai-ml-engineering.vllm.optimization-levels-startup
name: optimization-levels-startup
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [optimization-levels, kv-cache-memory, vllm-cache-root, enforce-eager, faster-startup]
level: practitioner
status: docs-checked
description: "Choose -O0 to -O3 and cut repeated startup time with the compile cache, --kv-cache-memory and --enforce-eager."
sources:
  - https://docs.vllm.ai/en/latest/configuration/optimization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: trade startup time against steady-state performance, and shorten repeat boots.

Optimization levels (`-O0` to `-O3`):
- `-O0`: no optimizations, fastest startup, lowest performance.
- `-O1`: simple compilation, fast fusions, PIECEWISE cudagraphs.
- `-O2`: the default; more compilation ranges and fusions, FULL_AND_PIECEWISE cudagraphs.
- `-O3`: currently equal to `-O2`, may gain time-consuming or experimental optimizations later.

Faster startup for the same (model, config, hardware):
1. Reuse the compile cache. torch.compile artifacts live under `VLLM_CACHE_ROOT` (default `~/.cache/vllm`) and can be copied between machines or baked into an image. Set `VLLM_FORCE_AOT_LOAD=1` to fail loudly instead of silently recompiling. Any change to the model, config, relevant `VLLM_*` variables, torch build or GPU model invalidates it.
2. Skip memory profiling with `--kv-cache-memory`. vLLM logs the exact value that reproduces the current allocation at startup; pass it next boot to skip profiling and CUDA-graph memory estimation. A conservative value caps concurrency; an optimistic one fails at allocation. It is valid only on the same GPU with the same initial free memory; remove the flag to re-profile after an OOM.
3. `--enforce-eager` skips compilation and CUDA-graph capture, fastest boot but slower decode; useful in development loops.

Docker: mount a named volume at the cache root (`-v vllm-cache:/root/.cache/vllm`) so later containers reuse the artifacts.

## Checked

2026-11-03. Confirmed against the Optimization and Tuning page (docs.vllm.ai/en/latest/): -O0 to -O3 definitions, compile cache, VLLM_FORCE_AOT_LOAD, --kv-cache-memory and --enforce-eager.

Method: documentation only; no commands were run.
