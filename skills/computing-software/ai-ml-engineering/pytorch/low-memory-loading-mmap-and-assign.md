---
id: computing-software.ai-ml-engineering.pytorch.low-memory-loading-mmap-and-assign
name: low-memory-loading-mmap-and-assign
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, mmap-load, assign, load-state-dict, meta-device, large-model-loading, torch-load]
level: practitioner
status: verified
description: "Load big PyTorch checkpoints without doubling RAM: torch.load(mmap=True), meta-device models and load_state_dict(assign=True), plus dtype and device caveats."
sources:
  - https://pytorch.org/tutorials/recipes/recipes/module_load_state_dict_tips.html
  - https://pytorch.org/docs/stable/generated/torch.load.html
  - https://pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module.load_state_dict
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Low-memory loading: mmap and assign

Naive loading holds two full copies: the randomly initialised model and the loaded state_dict, then copies one into the other. For a 30 GB checkpoint that is 60 GB of RAM plus init time.

## The pattern
```python
with torch.device("meta"):
    model = MyModel(cfg)                         # no memory, no init compute
sd = torch.load("ckpt.pt", mmap=True, weights_only=True)   # tensors backed by the file, paged in lazily
model.load_state_dict(sd, assign=True)           # params *become* the loaded tensors (no copy)
model.to("cuda")                                 # pages in and moves each tensor
```
- `mmap=True` needs the zipfile format (default since 1.6). Pages are read from disk only when touched; RAM use stays near one tensor at a time when moving to GPU.
- `assign=True` replaces parameters instead of copying into them, so meta params get real storage. Without it, loading into meta params is a silent-ish no-op: tested, the params stay on meta and PyTorch only emits a UserWarning ("copying from a non-meta parameter in the checkpoint to a meta parameter ... is a no-op").
- The loaded tensors keep the **checkpoint's dtype**. If the model should be bf16 and the checkpoint is fp32, call `model.to(torch.bfloat16)` after, or convert per tensor.

## Caveats of assign
- Properties from the module definition are lost: `requires_grad` comes from the loaded tensor (False for plain tensors). Tested on torch 2.14: parameters assigned from a plain checkpoint tensor came out with `requires_grad=True`; check on your version.
- Buffers not in the checkpoint (non-persistent) stay on meta. Re-initialise them: e.g. rotary `inv_freq` via a method, or use `model.to_empty(device=...)` then reset those buffers.
- Optimizers must be created after loading (they hold references to the parameter objects).
- Tied weights (embedding / LM head) must be re-tied after assign if the checkpoint stores only one.

## safetensors equivalent
`safetensors.torch.load_file(path, device="cpu")` is documented as memory-mapped (load_file and safe_open both ran here); with `safe_open(path, "pt")` you can load tensor by tensor straight to GPU (`f.get_tensor(name).to("cuda")`). Hugging Face `from_pretrained` has `low_cpu_mem_usage` / `device_map` options for this; check the current transformers docs for their behaviour.

## Verify
```python
import psutil, os
print(psutil.Process(os.getpid()).memory_info().rss / 2**30)     # before and after load
assert not any(p.is_meta for p in model.parameters())
assert not any(b.is_meta for b in model.buffers())
```
Compare a forward pass on fixed input against a reference load to confirm nothing was left uninitialised.
