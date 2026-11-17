---
id: computing-software.ai-ml-engineering.vllm.prefix-caching
name: prefix-caching
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [prefix-caching, enable-prefix-caching, apc, prefix-match-unit, mamba-shared-prefix-checkpoint]
level: practitioner
status: docs-checked
description: "Enable automatic prefix caching and tune hybrid Mamba prefix checkpoints."
sources:
  - https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reuse the KV cache of earlier queries that share a prefix, so shared prompt text is not recomputed.

Automatic Prefix Caching (APC) caches the KV cache of existing queries; a new query with the same prefix skips computing the shared part. Enable it with `enable_prefix_caching=True` in the engine.

Workloads where it pays off:
- Long document query: the same long document (manual, annual report) queried repeatedly with different questions is processed only once.
- Multi-round conversation: chat history is reused across rounds instead of reprocessed.

Limits: APC only reduces prefill time. It does not speed up decoding, so there is no gain when most time goes to generating long answers, or when new queries share no prefix with existing ones. It generally does not reduce vLLM performance.

Hybrid Mamba models: Mamba state is stored only on the Mamba block grid, so a hit can resume only at a block boundary. `--enable-mamba-shared-prefix-checkpoint` also stores a checkpoint at the shared-prefix junction, helping when many requests share a long system prompt and then diverge. It is off by default and takes effect only when prefix caching is on, EAGLE/MTP speculative decoding runs on the Mamba group, `--prefix-match-unit` is smaller than the Mamba block size, and the model does not use multi-module MTP.

```bash
vllm serve <hybrid-model> --prefix-match-unit 64 --enable-mamba-shared-prefix-checkpoint
```

`--prefix-match-unit` is required for this and sets the granularity of prefix-cache keys. Unset, it defaults to the greatest common divisor of the prefix-cacheable KV cache group block sizes, which for hybrid Mamba models is the block size itself, so the flag has no effect. Pick a value that divides every prefix-cacheable group's block size and, for models with a per-state compression ratio (such as sparse MLA), is a multiple of it; vLLM validates both at startup and names the offending sizes. Read the served block size from the startup log. 64 is a reasonable start.

FlashInfer ReplaySSM (Mamba2 decoding, off by default) caches recent inputs to reduce full-state writes and works with prefix caching on Model Runners V1 and V2, including MTP speculation. Limits: `align` mode needs BF16 model inputs; the replay buffer is at most 16 tokens and at least `1 + num_speculative_tokens` when speculating; pipeline parallelism, microbatching and KV connectors are unsupported.

## Checked

Method: 2026-11-08 read the automatic prefix caching page in full. APC, workloads, limits and Mamba checkpoint claims matched. Corrected the prefix-match-unit description (default is the GCD of block sizes, compression-ratio rule) and added the ReplaySSM limits.
