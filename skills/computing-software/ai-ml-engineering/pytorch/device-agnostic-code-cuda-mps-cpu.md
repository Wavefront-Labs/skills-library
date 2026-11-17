---
id: computing-software.ai-ml-engineering.pytorch.device-agnostic-code-cuda-mps-cpu
name: device-agnostic-code-cuda-mps-cpu
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, mps-backend, device-agnostic-code, cuda, apple-silicon, torch-accelerator]
level: practitioner
status: gated
description: "Write PyTorch code that runs unchanged on CUDA, Apple MPS and CPU: device selection, torch.accelerator, MPS op fallbacks, dtype limits and per-backend seeding."
sources:
  - https://pytorch.org/docs/stable/notes/mps.html
  - https://pytorch.org/docs/stable/accelerator.html
  - https://pytorch.org/docs/stable/notes/cuda.html#device-agnostic-code
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Device-agnostic code (CUDA / MPS / CPU)

**Goal:** one training/inference script that picks the best available accelerator and does not crash on the backend you did not test.

## Pick the device once
```python
import torch
if hasattr(torch, "accelerator") and torch.accelerator.is_available():   # exists in 2.14; first release not checked
    device = torch.accelerator.current_accelerator()                      # cuda / mps / xpu
elif torch.cuda.is_available():
    device = torch.device("cuda")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")
model.to(device)
x = x.to(device, non_blocking=True)
```
On a CPU-only torch 2.14 build this takes the final branch: `torch.accelerator.is_available()` is False, `current_accelerator()` returns `None` (signature `current_accelerator(check_available=False)`), and `torch.backends.mps.is_available()` is False. Then pass `device=` to every tensor factory (`torch.zeros(..., device=device)`) instead of `.cuda()`. Create tensors with `torch.empty_like`/`new_zeros` to inherit device and dtype (both kept float16 from a float16 source in a run).

## MPS specifics (Apple silicon)
No Apple hardware here, so every bullet in this section and the MPS and CUDA columns of the table below were not run (gated: unconfirmed, source is paywalled or blocked). Only API presence was checked on a Windows CPU build: `torch.mps.synchronize`, `current_allocated_memory`, `empty_cache`, `manual_seed` exist, and `torch.autocast("mps", dtype=torch.float16)` and `torch.amp.GradScaler("mps")` construct without error.
- Unsupported ops raise `NotImplementedError ... not currently implemented for the MPS device`. Set `PYTORCH_ENABLE_MPS_FALLBACK=1` before import to run them on CPU (slow; find and replace them).
- No float64 on MPS: cast to float32. bfloat16 needs recent macOS; fp16 autocast via `torch.autocast("mps", dtype=torch.float16)`.
- No distributed (NCCL) and no `pin_memory` benefit; unified memory means `num_workers` > 0 can still help for decode-heavy pipelines.
- Memory: `torch.mps.current_allocated_memory()`, `torch.mps.empty_cache()`; `PYTORCH_MPS_HIGH_WATERMARK_RATIO` caps usage.
- Seed with `torch.manual_seed` (covers MPS); `torch.mps.manual_seed` exists too.

## Branches you still need
| Concern | CUDA | MPS | CPU |
|---|---|---|---|
| Autocast dtype | bf16 (Ampere+) or fp16 | fp16 | bf16 |
| GradScaler | fp16 only | fp16 (`torch.amp.GradScaler("mps")`) | not needed |
| Sync for timing | `torch.cuda.synchronize()` | `torch.mps.synchronize()` | none |
| torch.compile | inductor | partial support; test | inductor (C++) |

Wrap these in a tiny helper keyed on `device.type` rather than scattering `if cuda` checks.

## Loading checkpoints across devices
`torch.load(path, map_location=device, weights_only=True)` so a CUDA-saved checkpoint loads on a Mac or CPU CI runner (the call ran on CPU for a tensor dict; loading a CUDA-saved file was not tried).

## Verify
- [ ] CI runs a smoke test on CPU (`CUDA_VISIBLE_DEVICES=""`) and the result matches GPU within tolerance.
- [ ] `grep -n "\.cuda()" -r src/` returns nothing.
- [ ] On MPS, run once without the fallback env var to list unsupported ops.
