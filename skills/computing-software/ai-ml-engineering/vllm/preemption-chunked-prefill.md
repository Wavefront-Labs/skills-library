---
id: computing-software.ai-ml-engineering.vllm.preemption-chunked-prefill
name: preemption-chunked-prefill
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [preemption, chunked-prefill, max-num-batched-tokens, gpu-memory-utilization]
level: advanced
status: docs-checked
description: "Diagnose KV-cache preemption and tune chunked prefill with max_num_batched_tokens in vLLM V1."
sources:
  - https://docs.vllm.ai/en/latest/configuration/optimization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reduce preemption and balance prefill against decode latency.

Preemption: when KV cache space cannot hold all batched requests, vLLM preempts requests and recomputes them later. In V1 the default mode is `RECOMPUTE`, not `SWAP`, because recomputation is cheaper there. The warning text says the sequence group "is preempted by PreemptionMode.RECOMPUTE mode because there is not enough KV cache space". Remedies listed:
- Increase `gpu_memory_utilization` (more pre-allocated KV cache).
- Decrease `max_num_seqs` or `max_num_batched_tokens`.
- Increase `tensor_parallel_size` (more KV room per GPU, more synchronization overhead).
- Increase `pipeline_parallel_size` (latency penalty).
Watch the Prometheus preemption counter, or log cumulative preemptions with `disable_log_stats=False`.

Chunked prefill is on by default in V1 whenever possible. The scheduler batches all pending decodes first, then schedules prefills within the `max_num_batched_tokens` budget, chunking a prefill that does not fit.

Tuning `max_num_batched_tokens`:
- Smaller (for example 2048): better inter-token latency.
- Larger: better time to first token.
- For throughput the docs recommend `> 8192`, especially for small models on large GPUs.
- Equal to `max_model_len` is almost the old V0 policy, though decodes are still prioritized.

Warning: with chunked prefill disabled, `max_num_batched_tokens` must exceed `max_model_len`, otherwise vLLM may crash at start-up.

```python
llm = LLM(model="meta-llama/Llama-3.1-8B-Instruct", max_num_batched_tokens=16384)
```

Decode priority gives better inter-token latency and puts compute-bound prefill and memory-bound decode in the same batch for better GPU use. The page's quoted warning is from a V0-era log line and also advises raising `gpu_memory_utilization` or `tensor_parallel_size`.

## Checked

Method: 2026-11-08 read the vLLM Optimization and Tuning page (docs source markdown), Preemption and Chunked Prefill sections in full and the rest skimmed.
Changes: added the scheduling benefits and a note that the quoted warning shows an older log format. The remedies, defaults and tuning guidance were unchanged and match the page.
