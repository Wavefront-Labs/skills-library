---
id: computing-software.ai-ml-engineering.pytorch.torch-load-weights-only-and-safe-loading
name: torch-load-weights-only-and-safe-loading
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, pytorch-serialization, torch-save, weights-only, torch-load-security, add-safe-globals, pickle-security]
level: practitioner
status: verified
description: "Load PyTorch checkpoints safely: weights_only=True default since 2.6, allowlisting classes with add_safe_globals, fixing 'Weights only load failed', and untrusted files."
sources:
  - https://pytorch.org/docs/stable/generated/torch.load.html
  - https://pytorch.org/docs/stable/notes/serialization.html#weights-only
  - https://pytorch.org/docs/stable/notes/serialization.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# torch.load weights_only and safe loading

**Goal:** load checkpoints without giving arbitrary code execution to whoever produced the file, and fix the errors the safe loader raises.

## Why
`torch.save` uses pickle. A pickle can run arbitrary code on load, so `torch.load` on a downloaded `.pt`/`.bin` was historically a remote-code-execution risk. With `weights_only=True` the unpickler only reconstructs tensors, primitive types, dicts/lists/tuples and an allowlist of safe classes.

Since **PyTorch 2.6 the default is `weights_only=True`**. Old code that pickled whole models or custom objects now fails with `UnpicklingError: Weights only load failed ... WeightsUnpickler error: Unsupported global: GLOBAL mymodule.MyConfig was not an allowed global by default. Please use torch.serialization.add_safe_globals([...]) or the torch.serialization.safe_globals([...]) context manager ...` (the message and the 2.6 default change were reproduced on torch 2.14; the same error appeared for a pickled `nn.Module`, a NumPy scalar and array, and an `Enum`).

## Fix the error properly
1. Save state dicts, not modules: `torch.save(model.state_dict(), path)` and load with `model.load_state_dict(torch.load(path, map_location="cpu"))`.
2. If the checkpoint legitimately contains a trusted custom class (config dataclass, enum, NumPy scalar), allowlist it:
```python
import torch
from mypkg.config import TrainConfig
torch.serialization.add_safe_globals([TrainConfig])
ckpt = torch.load("ckpt.pt")                    # weights_only=True still
# or scoped:
with torch.serialization.safe_globals([TrainConfig]):
    ckpt = torch.load("ckpt.pt")
```
`torch.serialization.get_unsafe_globals_in_checkpoint(path)` lists what a file needs before you load it (returned `['__main__.TrainConfig']` here). `torch.serialization.clear_safe_globals()` undoes `add_safe_globals`.
3. Only for files you produced and trust: `torch.load(path, weights_only=False)`. Never for downloaded files.

## Make checkpoints loadable by design
- Store config as a plain dict (`dataclasses.asdict(cfg)`) instead of an object.
- Convert NumPy arrays/scalars to tensors or Python numbers before saving.
- Optimizer and scheduler `state_dict()`s are plain dicts and load fine (checked with Adam and StepLR).
- For distribution, prefer **safetensors** for weights; it cannot carry code at all.

## Other untrusted-input surfaces
- `torch.hub.load` (it has a `trust_repo` argument, default `"check"`) and `trust_remote_code=True` in Transformers (Transformers docs: custom models need it) execute repository code by design; pin a commit and review it.
- `pickle`/`joblib` model files from scikit-learn have the same problem; the scikit-learn persistence docs say loading can execute arbitrary code and point to `skops.io` for sharing.

## Verify
- [ ] Loading code works with the default `weights_only=True`.
- [ ] No `weights_only=False` on any path that can receive third-party files.
- [ ] Custom classes allowlisted explicitly, not by disabling the check.
