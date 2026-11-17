---
id: computing-software.ai-ml-engineering.vllm.embedding-models
name: embedding-models
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [embeddings, pooling, llm-embed, runner-pooling, convert-embed, embed-api]
level: practitioner
status: docs-checked
description: "Serve embedding models with the pooling runner, LLM.embed, LLM.score and the Embeddings, Cohere and Pooling APIs."
sources:
  - https://docs.vllm.ai/en/latest/models/pooling_models/embed/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: turn text, images or audio into embedding vectors for uses like RAG and similarity.

Summary from the page: the pooling task is `embed`. Offline APIs are `LLM.embed(...)`, `LLM.encode(..., pooling_task="embed")` and `LLM.score(...)`. Online APIs are the OpenAI-compatible Embeddings API (`/v1/embeddings`), the Cohere Embed API (`/v2/embed`) and the Pooling API (`/pooling`).

Sequence embedding yields one vector per input; token embedding yields one per token, and many models support both.

```python
from vllm import LLM
llm = LLM(model="intfloat/e5-small", runner="pooling")
(output,) = llm.embed("Hello, my name is")
embeds = output.outputs.embedding
```

`LLM.encode` works for all pooling models; pass `pooling_task="embed"` and read `output.outputs.data`. `LLM.score` returns similarity between sentence pairs as the cosine similarity of the two prompts' embeddings, so every embedding model supports it.

Conversion: models marked with a C superscript (Llama, Qwen2, Qwen3, Gemma 2 or 3 based and others) convert automatically via `--convert embed`. For an unlisted model vLLM tries automatic conversion and takes the normalized hidden state of the last token. Models trained for embeddings give better results than converted ones.

Overrides and quirks from the notes:
- mGTE-TRM has the generic architecture name `NewModel`; use `--hf-overrides '{"architectures": ["GteNewModel"]}'`.
- Jina embeddings v5 pick a task adapter with `--hf-overrides '{"jina_task": "<task>"}'`, default `retrieval`.
- `ssmits/Qwen2-7B-Instruct-embed-base` needs `--pooler-config '{"pooling_type": "MEAN"}'`; `Alibaba-NLP/gte-Qwen2-*` needs `--trust-remote-code`.
- Multimodal embedders that share an architecture with a generative model (VLM2Vec, DSE-Qwen2-MRL) need `--runner pooling` plus the custom chat template from the examples folder.

Online details:
- `/v1/embeddings` is OpenAI-compatible; if the model has a chat template, `messages` can replace the input and are treated as one prompt.
- `/v2/embed` follows Cohere Embed v2. Parameters: `model`, `input_type`, one of `texts`, `images` (base64 data URIs) or `inputs`, `embedding_types` (`float` default, `binary`, `ubinary`, `base64`), `output_dimension` (Matryoshka truncation) and `truncate` (`END` default, `START`, `NONE` which errors on overlong input). `input_type` is accepted only for models defining `task_instructions` in `config.json` or `prompts` in the sentence-transformers config; otherwise it raises a validation error.

Normalization is toggled with `use_activation`; `normalize` was removed from `PoolingParams`.

Matryoshka: `dimensions` (in `PoolingParams` or the request) works only for models trained with MRL; others return a 400 error. If `is_matryoshka` is true in `config.json` any dimension is allowed, and `matryoshka_dimensions` restricts the allowed values. For unrecognised models use `--hf-overrides '{"is_matryoshka": true}'` or `'{"matryoshka_dimensions": [256]}'`.

## Checked

Method: 2026-11-08 read the vLLM Embedding Usages page (docs source markdown) in full, apart from the model support tables, which were skimmed.
Changes: added pooler-config and trust-remote-code notes, the runner flag for multimodal embedders, Cohere API parameters, normalization and Matryoshka rules. Earlier claims were unchanged and match the page.
