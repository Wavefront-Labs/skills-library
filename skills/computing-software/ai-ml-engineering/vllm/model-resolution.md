---
id: computing-software.ai-ml-engineering.vllm.model-resolution
name: model-resolution
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [model-resolution, hf-overrides, architectures, config-json]
level: practitioner
status: docs-checked
description: "Fix failed architecture lookup by overriding config.json fields with hf_overrides."
sources:
  - https://docs.vllm.ai/en/latest/configuration/model_resolution/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make vLLM load a model whose architecture it cannot resolve on its own.

vLLM loads HuggingFace-compatible models by reading the `architectures` field of the repository's `config.json` and finding the registered implementation. Resolution can fail when:
- `config.json` has no `architectures` field.
- An unofficial repository refers to a model by an alternative name vLLM has not recorded.
- The same architecture name is used for several models, making the choice ambiguous.

Fix: name the architecture explicitly by passing `config.json` overrides through the `hf_overrides` option:

```python
from vllm import LLM

llm = LLM(
    model="cerebras/Cerebras-GPT-1.3B",
    hf_overrides={"architectures": ["GPT2LMHeadModel"]},  # GPT-2
)
```

Here the repository is a GPT-2 style model, so the override points vLLM at the GPT-2 implementation class.

To choose a valid architecture name, consult the supported models list in the docs, which shows the architecture names vLLM recognises.

## Checked

Method: 2026-11-08 read the model resolution page in full. Failure causes and the hf_overrides example matched. Dropped the trailing Engine Arguments paragraph, which no cited page supports.
