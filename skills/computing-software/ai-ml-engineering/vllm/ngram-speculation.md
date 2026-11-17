---
id: computing-software.ai-ml-engineering.vllm.ngram-speculation
name: ngram-speculation
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [ngram, prompt-lookup-max, prompt-lookup-min, speculative-decoding-ngram]
level: intro
status: docs-checked
description: "Enable prompt-lookup n-gram speculative decoding with method ngram and its lookup window keys."
sources:
  - https://docs.vllm.ai/en/latest/features/speculative_decoding/n_gram/
  - https://docs.vllm.ai/en/latest/features/speculative_decoding/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: speculate tokens by matching n-grams in the prompt, with no draft model.

```python
llm = LLM(
    model="Qwen/Qwen3-8B",
    tensor_parallel_size=1,
    speculative_config={
        "method": "ngram",
        "num_speculative_tokens": 5,
        "prompt_lookup_max": 4,
    },
)
```

Keys (n-gram specific):
- `prompt_lookup_max`: maximum n-gram window size, integer >= 1.
- `prompt_lookup_min`: minimum window size, integer >= 1.
- Defaults: both are `5` if both are omitted; if only one is given, the other mirrors it.
- `num_speculative_tokens`: tokens proposed per step.
- `model` can be omitted for `ngram`.

CLI form:

```bash
vllm serve <target-model> --speculative-config '{
  "method": "ngram", "num_speculative_tokens": 4,
  "prompt_lookup_min": 2, "prompt_lookup_max": 5 }'
```

Selection guidance from the overview: n-gram is lightweight and easy to enable, with low to medium gain at low QPS and medium gain at high QPS. Simple methods like this give modest speedups without increasing workload during peak traffic. The overview also notes `model` can be omitted for `ngram_gpu`.

Suffix decoding is the related method with no extra draft model and dynamic speculation depth.

## Checked

2026-11-03. Confirmed against the N-Gram Speculation and Speculative Decoding pages (docs.vllm.ai/en/latest/): example config, prompt_lookup keys and defaults, gain table. Replaced an unconfirmed comparison with suffix decoding by the page's wording.

Method: documentation only; no commands were run.
