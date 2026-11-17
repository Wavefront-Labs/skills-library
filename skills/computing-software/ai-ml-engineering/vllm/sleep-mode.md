---
id: computing-software.ai-ml-engineering.vllm.sleep-mode
name: sleep-mode
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [sleep-mode, enable-sleep-mode, wake-up, rlhf, release-kv-cache-memory]
level: practitioner
status: docs-checked
description: "Release GPU memory between workloads with sleep levels, tagged wake-up, preserved parameters and CUDA graph offload."
sources:
  - https://docs.vllm.ai/en/latest/features/sleep_mode/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: free most GPU memory without stopping the server or unloading the container, for RLHF, training or cost saving.

Enable with `enable_sleep_mode=True` on `LLM`, or `--enable-sleep-mode` on the server. Supported on CUDA, ROCm and XPU. Works with tensor and pipeline parallelism.

Levels:
- Level 1: offload model weights to CPU RAM and discard the KV cache. Use it to run the same model again; ensure enough CPU memory for the weights.
- Level 2: discard the parameters and KV cache, and back up the rest of what the model allocated on the GPU at load (such as rope scaling tensors) to CPU memory. Use it to update weights (RLHF) or when CPU memory cannot hold the weights. Parameters are not backed up, so restore them after wake-up with `collective_rpc("reload_weights")`.

After a level-2 wake, parameters are undefined (unless preserved), other load-time allocations are kept at the same address, tensors derived from weights keep old values until post-load processing refreshes them, and KV cache and workspace contents are undefined. If you send weights to a sleeping engine, send every parameter not selected by `sleep_preserve_parameter_names`, including unchanged ones.

```python
llm.sleep(level=1)
llm.wake_up()
```

Level 2 with tagged wake-up, which avoids out-of-memory during weight updates:

```python
llm.sleep(level=2)
llm.wake_up(tags=["weights"])
llm.collective_rpc("reload_weights")
llm.wake_up(tags=["kv_cache"])
```

`is_sleeping` reports true until all components are awake.

Frozen weights: `--sleep-preserve-parameter-names` takes glob patterns (matched against `model.named_parameters()`, not checkpoint names or `requires_grad`) for weights that stay frozen, such as `draft.*` for a speculative drafter or an Engram table pattern. Level-2 sleep backs them up to CPU memory and wake restores them in place; level 1 is unchanged. The trainer must omit them from updates; the option does not filter updates. Without a draft pattern, level-2 sleep discards draft weights and speculation accepts no tokens after `reload_weights` (vLLM logs a warning).

`release_kv_cache_memory()` discards only KV cache memory, keeping weights resident, after `llm.sleep(level=0, mode="keep")` completes. It needs the default `cumem` backend with managed allocations; full sleep, partial wake-up and repeated release are rejected.

KV connector cache: discarding KV cache (any sleep level or release) also resets a configured connector's cache. Pass `reset_connector=False` to keep it, but block hashes do not cover weights, so use a per-weight-version `cache_salt` if weights may change.

`sleep_mode_offload_cudagraph=True` (`--sleep-mode-offload-cudagraph`, off by default) backs CUDA graphs up to CPU so they are replayed, not recaptured. It needs the `cumem` backend, CUDA or ROCm, and CUDA graphs; costs pinned host memory and about 3% decode latency at batch size 1 for custom allreduce copies. `enable_nccl_comm_suspend=True` (experimental, off by default) also releases NCCL communicator memory; it needs NCCL 2.29.7 or newer.

Online serving: set `VLLM_SERVER_DEV_MODE=1` plus `--enable-sleep-mode`; the dev endpoints must not be exposed to users. Endpoints: `POST /sleep?level=N`, `POST /wake_up` (optional `tags`), `POST /collective_rpc`, `POST /release_kv_cache_memory`, `GET /is_sleeping`.

ROCm: sleep allocates in chunks sized by `VLLM_ROCM_SLEEP_MEM_CHUNK_SIZE` (MB, default 256, power of 2 recommended); reduce it if you hit OOM.

An experimental CUDA checkpoint executor exists (level 1 only, single-node TP, Linux, many restrictions); see the page before using it.

## Checked

Method: 2026-11-08 read the sleep mode page in full. Levels, tagged wake-up, preserve-names, KV release and CUDA graph claims matched. Corrected platform support (CUDA, ROCm and XPU), the level-2 definition (it also backs up non-parameter load-time state), and added connector reset, NCCL suspend, endpoints, ROCm chunk size and the experimental executor pointer.
