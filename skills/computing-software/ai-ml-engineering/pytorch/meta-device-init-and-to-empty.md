---
id: computing-software.ai-ml-engineering.pytorch.meta-device-init-and-to-empty
name: meta-device-init-and-to-empty
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, meta-device, to-empty, deferred-initialization, large-models, fsdp, init-empty-weights]
level: practitioner
status: gated
description: "Build huge models without allocating memory using the meta device, then materialize with to_empty plus reset_parameters or load weights directly with assign=True."
sources:
  - https://pytorch.org/docs/stable/meta.html
  - https://pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module.to_empty
  - https://huggingface.co/docs/accelerate/concept_guides/big_model_inference
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Meta-device initialization and to_empty

**Goal:** construct a 70B-parameter model in milliseconds with zero memory, then materialize only the shards or weights each rank needs.

## Meta tensors
Tensors on `device="meta"` carry shape/dtype but no storage. Ops on them compute output shapes only, so you can also use them for shape inference.

```python
import torch
with torch.device("meta"):
    model = MyTransformer(cfg)          # no memory allocated
print(next(model.parameters()).device)  # meta
```

## Materialize option A: random init
```python
model.to_empty(device="cuda")           # allocates uninitialized storage
for m in model.modules():
    if hasattr(m, "reset_parameters"):
        m.reset_parameters()
```
`to_empty` leaves garbage values; you must re-init every parameter and buffer (including non-persistent buffers like RoPE caches, which are often computed in `__init__` and lost). Recompute them explicitly.

## Materialize option B: load weights directly
```python
sd = torch.load("ckpt.pt", map_location="cpu", mmap=True, weights_only=True)
model.load_state_dict(sd, assign=True)  # params become the loaded tensors; no double allocation
```
`assign=True` (PyTorch 2.1+) replaces meta params with the checkpoint tensors; dtype comes from the checkpoint.

## With FSDP2
Build on meta, call `fully_shard` on each block and the root, then `model.to_empty(device="cuda")` and init: each rank allocates only its shard (gated: unconfirmed, source is paywalled or blocked). Load sharded weights with `torch.distributed.checkpoint` or `set_model_state_dict`.

## Hugging Face equivalents
`accelerate.init_empty_weights()` context, or `from_pretrained(..., device_map="auto", low_cpu_mem_usage=True)` which does this for you (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- Code that reads tensor values in `__init__` (e.g. `torch.arange(...).float()` buffers, data-dependent asserts) breaks or produces meta buffers; compute them in a `reset_parameters`/`_init_buffers` method.
- Tied weights must be re-tied after `to_empty` (`model.tie_weights()` in HF (gated: unconfirmed, source is paywalled or blocked); tested in plain torch: after `assign=True` the tied head stayed on meta and untied).
- Missing keys after `assign=True` stay on meta; check `[n for n, p in model.named_parameters() if p.is_meta]`.

## Verify
- [ ] No parameter or buffer is still `is_meta` after materialization.
- [ ] Output on a fixed input matches a model built normally and loaded the same checkpoint.
