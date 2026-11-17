---
id: computing-software.ai-ml-engineering.vllm.eagle-speculation
name: eagle-speculation
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [eagle, eagle3, draft-model, speculative-decoding-eagle]
level: practitioner
status: docs-checked
description: "Configure EAGLE and EAGLE3 drafters in speculative_config, including draft tensor parallel size."
sources:
  - https://docs.vllm.ai/en/latest/features/speculative_decoding/eagle/
  - https://docs.vllm.ai/en/latest/features/speculative_decoding/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: speculate tokens with an EAGLE (Extrapolation Algorithm for Greater Language-model Efficiency) drafter.

EAGLE drafter:

```python
llm = LLM(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    tensor_parallel_size=4,
    speculative_config={
        "model": "yuhuili/EAGLE-LLaMA3-Instruct-8B",
        "draft_tensor_parallel_size": 1,
        "num_speculative_tokens": 2,
        "method": "eagle",
    },
)
```

EAGLE3 drafter: same shape with `"model": "RedHatAI/Llama-3.1-8B-Instruct-speculator.eagle3"`, `"method": "eagle3"`, `tensor_parallel_size=2` and `"draft_tensor_parallel_size": 2`.

Notes from the pages:
- `draft_tensor_parallel_size` sets the draft's TP independently of the target (1 in the first example while the target uses 4). Do not use `tensor_parallel_size` inside `speculative_config`; it is not a valid key.
- Pre-trained EAGLE drafters are on the Hugging Face hub in the RedHatAI/speculator-models collection and under yuhuili.
- With `vllm<0.7.0`, convert the speculative model with the linked gist script and set `"model": "path/to/modified/eagle/model"`.
- A detailed offline example, including extracting request-level acceptance rate, is `examples/features/speculative_decoding/spec_decode_offline.py`.

Overview table: EAGLE is a strong general-purpose model-based method, high gain at low QPS and medium to high gain at high QPS. To train your own draft models see vllm-project/speculators. The overview says pipeline parallelism is not composable with speculative decoding as of `vllm<=0.15.0`.

## Checked

Method: 2026-11-08 read the EAGLE page and the speculative decoding overview in full. Code examples and notes matched. Removed the unsupported line about reading generated text, added the overview-sourced table summary, the invalid tensor_parallel_size key warning and the pipeline-parallelism incompatibility.
