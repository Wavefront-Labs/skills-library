---
id: computing-software.ai-ml-engineering.hugging-face.loading-large-models-dtype-and-sharded-checkpoints
name: loading-large-models-dtype-and-sharded-checkpoints
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, transformers, sharded-checkpoints, torch-dtype, low-cpu-mem-usage, from-pretrained]
level: practitioner
status: gated
description: "Load large transformers models efficiently: torch_dtype, device_map, low_cpu_mem_usage, sharded safetensors, max_memory and offload, and saving with max_shard_size."
sources:
  - https://huggingface.co/docs/transformers/main/en/models
  - https://huggingface.co/docs/transformers/big_models
  - https://huggingface.co/docs/accelerate/usage_guides/big_modeling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loading large models

## The memory maths
Weights in bytes ~ params x bytes per param: 7B at fp32 = 28 GB, bf16 = 14 GB, int8 = 7 GB, 4-bit = 3.5 GB before quantisation overhead (decimal GB; in GiB these are 26.1, 13.0, 6.5 and 3.3). Add KV cache and activations for inference.

## Load
```python
import torch
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct",
    dtype=torch.bfloat16,                # or "auto": use the dtype stored in config.json (`torch_dtype=` still works but warns "deprecated")
    device_map="auto",                   # place layers on GPUs, then CPU, then disk
    max_memory={0: "20GiB", 1: "20GiB", "cpu": "64GiB"},
    revision="<commit-sha>")
print(model.hf_device_map)
```
- Without `dtype`, older 4.x versions loaded in fp32 regardless of checkpoint dtype, doubling memory. On transformers 5.20.2 a checkpoint saved in bf16 loaded as `torch.bfloat16` with no argument (and with `dtype="auto"`), while `dtype=torch.float32` upcast it; a checkpoint whose `config.json` has no dtype entry (the tiny test model) loaded as fp32. Set it explicitly anyway.
- `low_cpu_mem_usage=True` (implied by `device_map`) builds the model on the meta device and loads weights directly, avoiding two full copies in RAM.
- `device_map="auto"` with offload to CPU/disk works but is slow (weights move per forward); fine for occasional use, not serving. On a CPU-only host `device_map="auto"` loaded fine but the model had no `hf_device_map` attribute, so guard that `print` with `getattr`; GPU placement and `max_memory` splitting were not run here (gated: unconfirmed, source is paywalled or blocked).
- Quantised loading: `quantization_config=BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.bfloat16)` (config object constructs; the bitsandbytes load was not run: package absent here) (gated: unconfirmed, source is paywalled or blocked).

## Sharded checkpoints
Large repos store `model-00001-of-00004.safetensors` plus `model.safetensors.index.json` (maps each tensor to a shard). `from_pretrained` loads shard by shard so peak RAM stays near one shard.
```python
model.save_pretrained("out/", max_shard_size="5GB")   # safetensors is already the default
```
Ran with `max_shard_size="100KB"` on a tiny model: it wrote `model-00001-of-00003.safetensors` ... plus `model.safetensors.index.json` with keys `metadata` and `weight_map`. On 5.20.2 `safe_serialization=True` is accepted and `safe_serialization=False` is silently ignored (still wrote `model.safetensors`), so do not rely on the flag to produce a pickle `.bin`.
- Prefer safetensors: memory-mapped, fast, no pickle code execution. Avoid `.bin` from untrusted repos.
- Download only what's needed: `snapshot_download(repo, allow_patterns=["*.safetensors", "*.json", "tokenizer*"])` (ran: fetched config, safetensors, tokenizer.json, tokenizer.model and the special-token files only).

## Training note
For training large models, don't use `device_map="auto"` (naive pipeline, one GPU active at a time); use FSDP/DeepSpeed via Accelerate or Trainer.

## Gotchas
- `device_map="auto"` with a model that fits on one GPU may still split across GPUs if others are visible; use `device_map={"": 0}` or `"cuda:0"` to keep it on one device (`device_map={"": "cpu"}` loaded fine here).
- Tied weights (embeddings and LM head) on different devices cause errors; use `no_split_module_classes` (handled for official architectures) (gated: unconfirmed, source is paywalled or blocked).
- `model.to("cuda")` after `device_map` loading breaks the dispatch hooks (gated: unconfirmed, source is paywalled or blocked).

## Verify
`model.get_memory_footprint() / 2**30` and `torch.cuda.memory_allocated(i)` per GPU; run one generate call to ensure no "meta tensor" or device mismatch errors.
