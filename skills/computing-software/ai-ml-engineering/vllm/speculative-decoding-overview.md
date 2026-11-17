---
id: computing-software.ai-ml-engineering.vllm.speculative-decoding-overview
name: speculative-decoding-overview
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [speculative-decoding, speculative-config, num-speculative-tokens, draft-tensor-parallel-size, rejection-sample-method]
level: practitioner
status: docs-checked
description: "Choose a speculation method and set --speculative-config keys such as method, model and num_speculative_tokens."
sources:
  - https://docs.vllm.ai/en/latest/features/speculative_decoding/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reduce inter-token latency for medium-to-low QPS, memory-bound workloads.

Model-based methods (EAGLE, MTP, draft model, PARD) give the best latency reduction; n-gram and suffix decoding give modest speedups without extra load at peak traffic. Docs table: EAGLE and MTP high gain at low QPS; draft model medium at high QPS; n-gram and suffix low to medium.

Pass settings as JSON:

```bash
vllm serve <target-model> --speculative-config '{"method": "draft_model", "model": "<draft-model>", "num_speculative_tokens": 5}'
```

Python uses `LLM(..., speculative_config={...})`. The old `--speculative-model` and `--num-speculative-tokens` flags are deprecated. In YAML config files use a nested mapping, not an escaped JSON string.

Common keys:
- `method`: `draft_model`, `ngram`, `suffix`, `mtp`, `eagle3`, `dflash`; inferred when omitted if possible.
- `model`: draft or head; often omitted for ngram, suffix, mtp.
- `num_speculative_tokens`: integer greater than 0.
- `draft_tensor_parallel_size` (not `tensor_parallel_size`), `max_model_len`.
- `parallel_drafting` (default false; EAGLE and draft-model only).
- `rejection_sample_method`: `standard` (default), `synthetic`, `block`, or lossy `fly`.
- `draft_sample_method`: `greedy` (default) or `probabilistic`.
- `use_heterogeneous_vocab` (default false): draft model with a different vocabulary via Token-Level Intersection; draft-model method only, greedy draft sampling only.

Sampling settings such as `temperature` and `top_p` are not speculative-config keys. Custom speculators register as a method from a plugin and need the V2 model runner.

## Checked

2026-11-03. Confirmed against the Speculative Decoding page (docs.vllm.ai/en/latest/): method table, common keys, defaults and YAML/TP/sampling notes. Removed an unconfirmed 'experimental' label.

Method: documentation only; no commands were run.
