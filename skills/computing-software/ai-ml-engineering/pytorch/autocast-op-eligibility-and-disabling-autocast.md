---
id: computing-software.ai-ml-engineering.pytorch.autocast-op-eligibility-and-disabling-autocast
name: autocast-op-eligibility-and-disabling-autocast
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, autocast-op-lists, autocast, mixed-precision, numerical-stability, custom-fwd]
level: practitioner
status: verified
description: "Know which ops PyTorch autocast runs in low precision vs fp32, disable autocast for unstable regions, and make custom functions and ops autocast-safe."
sources:
  - https://pytorch.org/docs/stable/amp.html#autocast-op-reference
  - https://pytorch.org/docs/stable/amp.html#torch.amp.custom_fwd
  - https://pytorch.org/docs/stable/notes/amp_examples.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Autocast op eligibility and disabling autocast

Autocast does not cast the model; it picks a dtype per op call inside the region.

## The CUDA op lists (abridged; see the op reference for your version)
- **Run in fp16/bf16**: `matmul`, `mm`, `bmm`, `addmm`, `linear`, `conv*d`, `conv_transpose*d`, `baddbmm`, `addmv`, `mv`, `prelu`, `RNNCell`/`GRUCell`/`LSTMCell`. `scaled_dot_product_attention` is NOT in the CUDA list (it is in the CPU bf16 list).
- **Autocast to fp32**: `softmax`, `log_softmax`, `cross_entropy`, `nll_loss`, `layer_norm`, `group_norm`, `norm`, `exp`, `log`, `pow`, `sum`, `prod`, `cumsum`, `mse_loss`, `binary_cross_entropy_with_logits`, `kl_div`, `cosine_similarity`, many reductions.
- **Promote to widest input type** (CUDA list): `addcdiv`, `addcmul`, `atan2`, `bilinear`, `cross`, `dot`, `grid_sample`, `index_put`, `scatter_add`, `tensordot`. Mixing fp16 and fp32 inputs yields fp32. `add` is not listed; it promotes natively, with or without autocast. `cat`, `stack` and `index_copy` are in the CPU promote list (checked on CPU: `cat` of bf16 and fp32 gives fp32).
- `binary_cross_entropy` (on probabilities) raises an error in CUDA autocast regions; use `BCEWithLogitsLoss`. On CPU it is in the fp32 list instead (run here: no error, fp32 result).
- Ops not listed run in the input dtype: an fp16 tensor stays fp16 through `relu`, `gelu`, `dropout`.

## Disable autocast for a region
```python
with torch.autocast("cuda", dtype=torch.float16):
    h = backbone(x)
    with torch.autocast("cuda", enabled=False):
        logits = head(h.float())           # cast inputs yourself; disabling does not cast
        loss = custom_loss(logits, y)
```
Candidates: custom losses with `exp`/`log` written by hand, attention score computation in custom kernels, large sums or variance computations, eigen/solve ops (`torch.linalg.inv` and `eigh` raise on bf16/fp16 inputs; checked on CPU), and anything that produced inf/NaN only in mixed precision.

## Custom autograd Functions
```python
from torch.amp import custom_fwd, custom_bwd
class MyOp(torch.autograd.Function):
    @staticmethod
    @custom_fwd(device_type="cuda", cast_inputs=torch.float32)   # run forward in fp32
    def forward(ctx, x): ...
    @staticmethod
    @custom_bwd(device_type="cuda")                               # backward uses same autocast state
    def backward(ctx, g): ...
```
Without `custom_bwd`, backward runs outside autocast even if forward ran inside. Custom ops registered with `torch.library` need an autocast registration or explicit casts.

## Other gotchas
- Autocast regions should cover forward and loss only; backward runs in the same dtypes automatically.
- Tensors created inside autocast (e.g. `torch.zeros(..., dtype=...)`) keep their requested dtype; masks filled with `-inf` vs `finfo(fp16).min` matter.
- CPU autocast (`device_type="cpu"`, bf16) has its own, much shorter op lists. Run on torch 2.14 CPU: `matmul`/`linear`/`scaled_dot_product_attention` gave bf16, but `softmax`, `layer_norm`, `sum` and `exp` stayed bf16 (not promoted to fp32 as on CUDA), so do not assume the CUDA fp32 list applies.
- Nested `torch.autocast(..., dtype=bf16)` inside fp16 switches dtype for the inner region.

## Verify
`print(out.dtype)` at key points inside autocast, or register forward hooks printing dtypes per module once. Compare loss with autocast disabled on a batch: the difference should be small (3e-3 relative for a tiny MLP in bf16 on CPU; expect bf16 to be noisier than fp16).
