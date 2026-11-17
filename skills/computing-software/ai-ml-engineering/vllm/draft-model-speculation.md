---
id: computing-software.ai-ml-engineering.vllm.draft-model-speculation
name: draft-model-speculation
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [draft-model, use-heterogeneous-vocab, speculative-config, token-level-intersection]
level: practitioner
status: docs-checked
description: "Speculate with a smaller draft model, serve it online, and use a different-vocabulary draft via heterogeneous vocab."
sources:
  - https://docs.vllm.ai/en/latest/features/speculative_decoding/draft_model/
  - https://docs.vllm.ai/en/latest/features/speculative_decoding/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use a small separate model to propose tokens that the target verifies.

Offline, speculating 5 tokens at a time:

```python
llm = LLM(
    model="Qwen/Qwen3-8B",
    speculative_config={
        "model": "Qwen/Qwen3-0.6B",
        "num_speculative_tokens": 5,
        "method": "draft_model",
    },
)
```

Online equivalent:

```bash
vllm serve Qwen/Qwen3-4B-Thinking-2507 --host 0.0.0.0 --port 8000 --seed 42 -tp 1 \
    --max-model-len 2048 --gpu-memory-utilization 0.8 \
    --speculative-config '{"model": "Qwen/Qwen3-0.6B", "num_speculative_tokens": 5, "method": "draft_model"}'
```

Clients are unchanged.

Heterogeneous vocabularies: by default the draft and target must share a vocabulary. `use_heterogeneous_vocab: true` enables Token-Level Intersection (TLI): vLLM maps the two vocabularies by normalising token strings, constrains draft logits to the shared tokens, and translates sampled IDs to the target vocabulary before rejection sampling. It currently requires `draft_sample_method='greedy'` (the default), and `use_local_argmax_reduction` is also unsupported with it.

```python
speculative_config={"method": "draft_model", "model": "HuggingFaceTB/SmolLM2-135M-Instruct",
                    "num_speculative_tokens": 3, "use_heterogeneous_vocab": True}
```

Docs example sets `gpu_memory_utilization=0.5` to leave room for both models. Gemma 4 assistant checkpoints are not generic draft models; use `"method": "mtp"`.

## Checked

2026-11-03. Confirmed against the Draft Models and Speculative Decoding pages (docs.vllm.ai/en/latest/): offline and online configs, heterogeneous vocabulary rules and the Gemma 4 note. Removed a trailing generic sentence and quoted the mtp method as the page does.

Method: documentation only; no commands were run.
