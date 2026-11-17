---
id: computing-software.ai-ml-engineering.vllm.kv-cache-offloading
name: kv-cache-offloading
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [kv-offloading, offloading-connector, cpu-bytes-to-use, tiering-offloading-spec, canonical-layout]
level: advanced
status: docs-checked
description: "Offload KV blocks to CPU memory and secondary tiers with OffloadingConnector."
sources:
  - https://docs.vllm.ai/en/latest/features/kv_offloading_usage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: extend the prefix cache by moving completed KV blocks to slower, larger tiers; hits are promoted back to GPU on demand.

`OffloadingConnector` supports CUDA, ROCm and XPU only. Pick a spec with `spec_name` in `kv_connector_extra_config`:
- `CPUOffloadingSpec` (default): one CPU tier of pinned host memory.
- `TieringOffloadingSpec`: CPU primary tier plus ordered `secondary_tiers`. Only the CPU tier touches the GPU; everything else is staged through it.

Single tier:

```bash
vllm serve <model> --kv-transfer-config '{"kv_connector":"OffloadingConnector","kv_role":"kv_both","kv_connector_extra_config":{"block_size":64,"cpu_bytes_to_use":1000000000}}'
```

Key settings:
- `cpu_bytes_to_use`: required; total host bytes across all workers, not per worker.
- `block_size`: offloaded block size in tokens, a multiple of the GPU block size; exclusive with `blocks_per_chunk`.
- `eviction_policy`: `lru` (default) or `arc`.
- `offload_prompt_only`: default true, skipping decode blocks.
- `canonical_layout`: true stores a common representation, enabling sharing across tensor-parallel sizes and one copy of replicated KV.

A secondary tier entry looks like `{"type":"fs","root_dir":"/path/to/kv_cache","n_read_threads":32,"n_write_threads":16}`. Secondary tiers are not yet supported when workers span several nodes; startup fails.

Per request, `kv_transfer_params` with `max_load_tokens` caps loading from offloaded storage; `0` disables external loading while GPU prefix reuse remains. It is experimental.

## Checked
2026-11-09. Confirmed against the vLLM KV Offloading Usage Guide (docs/features/kv_offloading_usage.md in vllm-project/vllm, source of the page above): CUDA, ROCm and XPU support; `CPUOffloadingSpec` default and `TieringOffloadingSpec`; the single-tier command and its keys; `cpu_bytes_to_use` required and total across workers; `block_size` multiple of the GPU block size and exclusive with `blocks_per_chunk`; `eviction_policy` `lru` default or `arc`; `offload_prompt_only` default true; `canonical_layout`; the `fs` tier keys `root_dir`, `n_read_threads`, `n_write_threads`; secondary tiers failing at startup on multi-node engines; `max_load_tokens` in `kv_transfer_params`, `0` semantics and the experimental warning. Nothing removed.
Method: documentation only; no commands were run.
