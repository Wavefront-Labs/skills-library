---
id: computing-software.ai-ml-engineering.pytorch.tf32-and-matmul-precision
name: tf32-and-matmul-precision
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, tf32, matmul-precision, set-float32-matmul-precision, ampere, numerical-precision]
level: practitioner
status: gated
description: "Control TF32 on Ampere+ GPUs in PyTorch with set_float32_matmul_precision and cuDNN flags, and know when the 10-bit mantissa hurts accuracy."
sources:
  - https://pytorch.org/docs/stable/notes/cuda.html#tensorfloat-32-tf32-on-ampere-and-later-devices
  - https://pytorch.org/docs/stable/generated/torch.set_float32_matmul_precision.html
  - https://blogs.nvidia.com/blog/tensorfloat-32-precision-format/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TF32 and matmul precision

TF32 keeps fp32's 8-bit exponent but only a 10-bit mantissa, run on tensor cores on Ampere (A100, RTX 30xx) and newer. fp32 matmuls get a speedup with about 1e-3 relative error (the 8x and 1e-3 figures are vendor numbers, not measured here: no GPU) (gated: unconfirmed, source is paywalled or blocked).

## Defaults (PyTorch 1.12+)
- `torch.backends.cuda.matmul.allow_tf32 = False` (matmuls run in full fp32 by default).
- `torch.backends.cudnn.allow_tf32 = True` (convolutions use TF32 by default).

## Turning it on
```python
torch.set_float32_matmul_precision("high")     # TF32 for matmuls (or bf16x3 if supported)
# "highest" = full fp32 (default), "medium" = bf16 internally if a fast kernel exists (fastest, least precise)
torch.backends.cudnn.allow_tf32 = True
```
On torch 2.14 the new API is `torch.backends.fp32_precision`, `torch.backends.cuda.matmul.fp32_precision`, `torch.backends.cudnn.fp32_precision` (plus `cudnn.conv` and `cudnn.rnn`), settable to `"ieee"` or `"tf32"`; they read `"none"` until set, and setting `allow_tf32 = True` made `matmul.fp32_precision` read `"tf32"` (run on CPU build). The CUDA semantics page says the old `allow_tf32` flags are going to be deprecated and that mixing old and new settings is not supported, so pick one style. An invalid name such as `set_float32_matmul_precision("foo")` only warns and has no effect.

## When to use it
- Training in fp32 (no autocast): turn on "high". Convergence is unaffected for almost all deep learning workloads; NVIDIA and PyTorch both validate this.
- Under `torch.autocast` with bf16/fp16, matmuls already run in low precision; TF32 only affects ops left in fp32.
- Keep "highest" for: numerical tests comparing against a reference, scientific computing, solvers (`torch.linalg`), large reductions where error accumulates, and gradient checks (`gradcheck` needs float64 anyway).

## Gotchas
- Tests that pass on one GPU generation and fail on a newer one with small tolerance mismatches: TF32 in convs (cudnn defaults to allowed). Set `cudnn.allow_tf32 = False` in the test fixture or loosen `rtol` to ~1e-3.
- Set the matmul precision before compiling or tracing (not run here: inductor needs a C++ compiler on this machine) (gated: unconfirmed, source is paywalled or blocked).
- The setting is process-global. Libraries (Lightning, HF Trainer `tf32=True`) may flip it; log `torch.get_float32_matmul_precision()` at start.

## Verify
```python
a, b = torch.randn(4096, 4096, device="cuda"), torch.randn(4096, 4096, device="cuda")
ref = (a.double() @ b.double()).float()
for p in ["highest", "high"]:
    torch.set_float32_matmul_precision(p)
    print(p, ((a @ b) - ref).abs().max().item())
```
Pair with a CUDA-event timing of the same matmul to see the speed difference on your GPU. This block needs a CUDA GPU and was not run (gated: unconfirmed, source is paywalled or blocked).
