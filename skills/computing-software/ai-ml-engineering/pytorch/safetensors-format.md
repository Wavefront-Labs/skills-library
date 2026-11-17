---
id: computing-software.ai-ml-engineering.pytorch.safetensors-format
name: safetensors-format
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, pytorch-serialization, safetensors, save-file, load-file, shared-tensors, mmap-loading, hugging-face]
level: practitioner
status: verified
description: "Save and load weights with safetensors: save_file/load_file, shared-tensor errors and save_model, metadata, sharded index files and fast mmap/GPU loading."
sources:
  - https://huggingface.co/docs/safetensors/index
  - https://huggingface.co/docs/safetensors/api/torch
  - https://github.com/huggingface/safetensors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# safetensors format

**Goal:** store model weights in a format that is safe to load from strangers, fast to memory-map, and framework-neutral.

## Format in one paragraph
An 8-byte header length, a JSON header (tensor name -> dtype, shape, byte offsets, plus an optional `__metadata__` string map), then raw tensor bytes. No code, no pickle. Loading is a bounds-checked memory map, so it is fast and lazy.

## Basic use
```python
from safetensors.torch import save_file, load_file, safe_open
save_file(model.state_dict(), "model.safetensors", metadata={"arch": "resnet50", "step": "12000"})
state = load_file("model.safetensors", device="cpu")      # or device="cuda:0"
model.load_state_dict(state)

with safe_open("model.safetensors", framework="pt", device="cpu") as f:
    print(f.metadata())
    emb = f.get_tensor("embed.weight")                      # read one tensor only
```
Metadata values must be strings (an int raised `TypeError: ... 'int' object is not an instance of 'str'`). The file starts with an 8-byte little-endian header length followed by the JSON header (checked by parsing a saved file).

## Shared tensors
Tied weights (input embedding == output projection) share storage. `save_file` refuses (safetensors 0.8.0): `RuntimeError: Some tensors share memory, this will lead to duplicate memory on disk ...`. Options:
```python
from safetensors.torch import save_model, load_model
save_model(model, "model.safetensors")    # de-duplicates shared tensors
load_model(model, "model.safetensors")    # model must already be tied (build it the same way)
```
Or drop one key and re-tie after loading. Run here: `save_model` stored only `0.weight`; `load_model` into a tied model worked and kept it tied, while `load_model` into an untied copy raised `Missing key(s) in state_dict`.

## Large models
- Hugging Face `save_pretrained` writes `model-00001-of-0000N.safetensors` plus `model.safetensors.index.json` mapping each tensor to its shard; `max_shard_size` controls shard size. In transformers 4.57 the defaults were `safe_serialization=True` and `max_shard_size="5GB"`; on current main the `safe_serialization` argument is gone (safetensors is the only format written) and `max_shard_size` defaults to `"50GB"`, so pass it explicitly.
- Convert legacy checkpoints: load with `torch.load(..., weights_only=True)` (ran fine on a plain state dict) then `save_file`. `safe_open(...).get_tensor(name)` reads one tensor at a time (checked).

## Gotchas
- Only tensors: optimizer state, step counters, configs go elsewhere (JSON alongside, or `torch.save` for trusted resume checkpoints).
- Non-contiguous tensors raise `ValueError: You are trying to save a non contiguous tensor`; make them contiguous (`{k: v.contiguous() for k, v in sd.items()}`).
- To keep memory down, read tensors one at a time with `safe_open` instead of `load_file` for the whole file.

## Verify
- [ ] Round-trip: reload into a fresh model and compare outputs on a fixed input.
- [ ] Tied weights still tied after load (`model.lm_head.weight is model.embed.weight` or equal data_ptr).
- [ ] Distribution artifacts contain no pickle files.
