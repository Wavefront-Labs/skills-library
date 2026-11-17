---
id: computing-software.ai-ml-engineering.pytorch.cross-device-loading-and-state-dict-mismatches
name: cross-device-loading-and-state-dict-mismatches
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, pytorch-serialization, map-location, load-state-dict-strict, missing-keys, ddp-module-prefix, torch-compile-orig-mod]
level: practitioner
status: gated
description: "Load checkpoints across devices and architectures: map_location, module./_orig_mod. prefixes, strict=False missing/unexpected keys, and size mismatches in heads."
sources:
  - https://pytorch.org/tutorials/beginner/saving_loading_models.html
  - https://pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module.load_state_dict
  - https://pytorch.org/docs/stable/generated/torch.load.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-device loading and state_dict key mismatches

**Goal:** load any checkpoint into the model you have, on the device you have, and know exactly which weights did not load.

## Devices
```python
sd = torch.load("ckpt.pt", map_location="cpu")                 # always safe; move model afterwards
sd = torch.load("ckpt.pt", map_location={"cuda:1": "cuda:0"})   # remap a specific device
model.load_state_dict(sd); model.to(device)
```
Loading a GPU-saved checkpoint without `map_location` on a CPU-only machine fails with `Attempting to deserialize object on a CUDA device`.  In multi-GPU jobs without it, every rank loads onto the device the tensors were saved from (often `cuda:0`), causing OOM or contention on GPU 0 (gated: unconfirmed, source is paywalled or blocked). Load to CPU, or to `f"cuda:{local_rank}"`.

## Prefix mismatches
| Saved from | Key prefix | Fix |
|---|---|---|
| `DistributedDataParallel` / `DataParallel` | `module.` | save `model.module.state_dict()`; or strip |
| `torch.compile`d model | `_orig_mod.` | save `model._orig_mod.state_dict()`; or strip |
| Wrapped in a LightningModule etc. | `model.` | strip |
```python
from torch.nn.modules.utils import consume_prefix_in_state_dict_if_present
consume_prefix_in_state_dict_if_present(sd, "module.")   # in place
```

## strict=False, but read the result
```python
result = model.load_state_dict(sd, strict=False)
print("missing:", result.missing_keys)        # in model, not in checkpoint -> left at init values
print("unexpected:", result.unexpected_keys)  # in checkpoint, not in model -> ignored
```
`strict=False` without inspecting these lists is how models silently run with a randomly initialised backbone. Assert that only the keys you expect (e.g. the new head) are missing.

## Size mismatches (new head / vocab)
`strict=False` does not skip shape mismatches; it still raises `size mismatch for fc.weight`. Filter them:
```python
own = model.state_dict()
sd = {k: v for k, v in sd.items() if k in own and v.shape == own[k].shape}
model.load_state_dict(sd, strict=False)
```
For a grown vocabulary, copy the old rows into the new embedding matrix rather than dropping it.

## Other gotchas
- Buffers (BatchNorm `running_mean`, `num_batches_tracked`) are in the state dict; a `persistent=False` buffer is not.
- Optimizer state is keyed by parameter order, not name; loading an optimizer state into a model with a different parameter order mismatches silently. Rebuild the optimizer if the architecture changed.
- dtype: a bf16 checkpoint loaded into an fp32 model is upcast by `copy_`; that is fine, but check the model's dtype is what you intend.

## Verify
- [ ] Missing/unexpected key lists printed and asserted.
- [ ] Model outputs on a fixed input match the original run after loading.
- [ ] Multi-GPU load uses CPU or the local rank's device.
