---
id: computing-software.ai-ml-engineering.vllm.lora-adapters
name: lora-adapters
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [lora, enable-lora, lora-modules, lora-request, max-loras]
level: practitioner
status: docs-checked
description: "Serve LoRA adapters offline with LoRARequest and online with --enable-lora and --lora-modules."
sources:
  - https://docs.vllm.ai/en/latest/features/lora/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run per-request LoRA adapters on top of a base model.

Adapters work with any vLLM model that implements `SupportsLoRA` and are served per request with minimal overhead.

Offline:

```python
llm = LLM(model="meta-llama/Llama-3.2-3B-Instruct", enable_lora=True)
outputs = llm.generate(prompts, sampling_params,
    lora_request=LoRARequest("sql_adapter", 1, sql_lora_path))
```

`LoRARequest` takes a human-readable name, a globally unique integer ID and the adapter path. Download adapters first, e.g. with `huggingface_hub.snapshot_download`.

Online with the OpenAI-compatible server:

```bash
vllm serve meta-llama/Llama-3.2-3B-Instruct --enable-lora \
    --lora-modules sql-lora=jeeejeee/llama32-3b-text2sql-spider
```

Use `--lora-modules {name}={path} {name}={path}` for each module. Other LoRA parameters such as `max_loras`, `max_lora_rank` and `max_cpu_loras` apply server-wide. `GET /v1/models` lists the base model plus each adapter name. Select an adapter by putting its name in the request `model` field; requests run in parallel with base-model requests and other adapters if `max_loras` is high enough.

JSON form of `--lora-modules` adds a base model: `'{"name": "sql-lora", "path": "jeeejeee/llama32-3b-text2sql-spider", "base_model_name": "meta-llama/Llama-3.2-3B-Instruct"}'`. The old `name=path` form still works but leaves `base_model_name` unspecified. With the JSON form the model card's `parent` field points at the base model and `root` at the adapter location.

Tuning tips from the page:
- `--max-lora-rank`: set it to the largest rank among your adapters (64 for ranks 16, 32, 64), not higher; a much larger value wastes memory and can hurt performance.
- `--lora-target-modules`: restrict LoRA to module suffixes such as `o_proj` or `qkv_proj`; unset means all supported modules.

MoE adapters: to serve 2D (megatron) and 3D (peft) formats from one engine, start with `--enable-mixed-moe-lora-format` and set `is_3d_lora_weight` per module. Without that flag the field is ignored and the adapter must match the base model's wrapper; it is also ignored for non-MoE models.

Other cases on the page: default multimodal LoRAs via `default_mm_loras` or `--default-mm-loras` (only one LoRA per prompt, generate and chat only), PEFT sequence-classification heads saved as `score` or `classifier` with `--max-lora-cls-labels`, and experimental LoRA for tower and connector parts of multimodal models.

## Checked

Method: 2026-11-08 read the vLLM LoRA Adapters page (docs source markdown) in full and compared every claim.
Changes: added the max-lora-rank and lora-target-modules tips, model-card lineage, the mixed-format flag behaviour and a pointer to multimodal and classification cases. Existing offline, serve and JSON-format claims were unchanged and match the page.
