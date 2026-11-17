---
id: computing-software.ai-ml-engineering.vllm.suffix-decoding
name: suffix-decoding
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [suffix-decoding, suffix, suffix-decoding-max-tree-depth, adaptive-verification, speculative-decoding]
level: advanced
status: docs-checked
description: "Configure method suffix: GPU corpus matching of prompt and prior responses, its keys, shared-corpus caveat and adaptive verification."
sources:
  - https://docs.vllm.ai/en/latest/features/speculative_decoding/suffix/
  - https://docs.vllm.ai/en/latest/features/speculative_decoding/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: speculate from the prompt and earlier responses, best for repetitive work such as code editing, agentic loops (self-reflection, self-consistency) and RL rollouts.

Like n-gram, suffix decoding drafts by pattern-matching the last generated tokens. Unlike n-gram it (1) matches against the request's own prompt and output and the responses of previous requests, and (2) uses frequency counts to propose the most likely continuations. No draft model is needed.

```python
llm = LLM(
    model="Qwen/Qwen3-8B",
    tensor_parallel_size=1,
    speculative_config={"method": "suffix", "num_speculative_tokens": 8},
)
```

How it works (current docs): it runs on the GPU, works with async scheduling and builds on `ngram_gpu`.
- Each request matches its own prompt and output by longest matching suffix, up to `suffix_decoding_max_tree_depth` tokens.
- Finished responses go into a GPU corpus (`suffix_decoding_corpus_tokens`, 1M tokens by default, oldest evicted first). Each step a request looks up positions by its last 2 and last 4 tokens and extends to the longest suffix match, so corpus matching needs a max tree depth of at least 2. The continuation is chosen by how often each next token follows the matches.
- The draft always has `num_speculative_tokens` tokens; unmatched slots are filled with the last sampled token. Without adaptive verification every slot is verified, so keep the value moderate (default 8).

Keys from the overview page:
- `suffix_decoding_max_tree_depth` (24).
- `suffix_decoding_max_cached_requests` (10000; 0 disables the cross-request corpus).
- `suffix_decoding_corpus_tokens` (1048576; 0 matches only within each request).
- `suffix_decoding_max_spec_factor` (1.0) and `suffix_decoding_min_token_prob` (0.1) are deprecated and have no effect.

Seeded sampling is not reproducible with suffix decoding (drafts come from finished requests; with adaptive verification the verified slots depend on the batch). For reproducible seeded sampling set `suffix_decoding_corpus_tokens: 0` and leave adaptive verification off.

The corpus is shared by all requests whatever their `cache_salt` or LoRA adapter. Drafts never change the output distribution, but acceptance shows in decode speed. Where requests must not influence each other, set `suffix_decoding_corpus_tokens: 0`.

Adaptive verification: add `"enable_adaptive_verification": True` to the config. At high concurrency, verifying every slot can make suffix decoding slower than no speculation; the speculator then reports a per-slot acceptance estimate (learned online by draft source, match length and position) and the scheduler verifies only slots worth their cost. It requires full CUDA graphs and an attention backend that replays variable-length decode batches, for example `TRITON_ATTN` or FlashAttention 3.

Overview table: low to medium gain at low QPS, medium gain at high QPS.

## Checked

Method: 2026-11-08 read the suffix page and the speculative decoding overview in full. Rewrote the draft: it described an older design (Arctic Inference install, V1 versus V2 runner split, num_speculative_tokens 32, adaptive tokens per request, max_spec_factor and min_token_prob as live V1 keys) that the current pages do not state; those claims were dropped and the two keys are now marked deprecated. Corpus-sharing, seeded-sampling and adaptive-verification claims were confirmed.
