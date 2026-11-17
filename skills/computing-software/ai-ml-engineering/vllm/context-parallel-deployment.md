---
id: computing-software.ai-ml-engineering.vllm.context-parallel-deployment
name: context-parallel-deployment
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [context-parallel, decode-context-parallel, dcp, kv-cache-duplication, prefill-context-parallel-size]
level: advanced
status: docs-checked
description: "Shard long-context KV cache with decode context parallel (-dcp) and know prefill context parallel strategies."
sources:
  - https://docs.vllm.ai/en/latest/serving/context_parallel_deployment/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: serve long-context requests: control TTFT in prefill, KV capacity in decode.

Prefill context parallel: split a request of `T` new tokens into `N` chunks across `N` GPUs. Two strategies: partial query with full key/value (gather KV from all GPUs; for moderately long requests) and partial query with partial key/value using ring-attention (when full KV does not fit). Both are under active development.

Decode context parallel (DCP): decode must attend a few query tokens against a large paged KV cache, so the question is how to shard that cache. For a model with `H` kv-heads, a request of `T` tokens stores `H * T` key/value tensors.
1. If one GPU holds them, no parallelism.
2. Otherwise shard along `H` with plain tensor parallelism, `-tp <num_gpus>`.
3. Beyond `tp_size > H`, KV is duplicated `tp_size / H` times. Add `-dcp <size>` to shard along `T`. It does not add GPUs; it reduces duplication. Valid range is `[1, tp_size/H]`; larger values cut duplication but raise communication.

KV cache is sharded by interleaving so future tokens shard naturally.

Case studies from the page:
- DeepSeek-R1 (1 kv-head with MLA): `-tp 8` duplicates 8x; add `-dcp 8`.
- Kimi-K2 at `-tp 16`: `-dcp 16` removes duplication; `-dcp 8` leaves 2x with communication inside one node.
- Qwen3-235B-A22B (4 kv-heads) at `-tp 8`: 2x duplication; add `-dcp 2`.

Rule: raise `-tp` until performance is satisfactory, then add `-dcp`. dcp is capped at `tp_size / H` for simplicity; to accelerate decode further raise `tp_size` first. Supported for MLA and GQA models; some attention backends also combine DCP with MTP.

`cache_config.effective_attention_block_size` (also gRPC `Control.GetServerInfo.effective_attention_block_size`) reports the full-attention block size in tokens including DCP: a 16-token physical block with DCP=4 is 64 tokens. It is `None` or absent when there is no common size, the scheduler does not expose it, or the engine is older.

## Checked

Method: 2026-11-08 read the context parallel deployment page in full. DCP reasoning, ranges and case studies matched. Removed the --prefill-context-parallel-size flag, which the page never names, and added the dcp cap and effective block size notes.
