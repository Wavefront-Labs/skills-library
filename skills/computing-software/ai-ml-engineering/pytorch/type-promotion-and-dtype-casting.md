---
id: computing-software.ai-ml-engineering.pytorch.type-promotion-and-dtype-casting
name: type-promotion-and-dtype-casting
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, type-promotion, dtype-casting, torch-tensors, result-type, dtype]
level: practitioner
status: verified
description: "Predict and control PyTorch dtype promotion: category rules, 0-dim scalar behaviour, result_type/promote_types, in-place cast errors and silent float64 creep."
sources:
  - https://pytorch.org/docs/stable/tensor_attributes.html#type-promotion-doc
  - https://pytorch.org/docs/stable/generated/torch.result_type.html
  - https://pytorch.org/docs/stable/generated/torch.can_cast.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Type promotion and dtype casting

**Goal:** know what dtype an op will return before it surprises you with float64 memory, an int overflow or an in-place error.

## The rules (torch.result_type)
1. Operands are ranked by category: bool < integer < floating < complex.
2. If a **dimensioned tensor** is in a higher category than every 0-dim tensor or Python scalar, the dimensioned tensors decide the dtype.
3. A 0-dim tensor or Python scalar only "wins" when its category is higher. A Python scalar then gives the default dtype for that category (`torch.get_default_dtype()` for float, int64 for Python int, also for a bool tensor times a Python int); a 0-dim tensor keeps its own dtype (`int32` tensor times a 0-dim `float64` tensor gives `float64`, checked).

```python
import torch
a = torch.ones(3, dtype=torch.float16)
(a * 2.5).dtype                       # float16  (scalar same category -> tensor dtype wins)
(a * torch.tensor(2.5, dtype=torch.float64)).dtype  # float16 (0-dim does not upcast within category)
(torch.ones(3, dtype=torch.int32) * 2.5).dtype      # float32 (Python scalar higher category -> default float)
(torch.ones(3, dtype=torch.uint8) + torch.ones(3, dtype=torch.int8)).dtype  # int16
torch.result_type(a, 2.5); torch.promote_types(torch.int32, torch.float16)  # float16
```

## Where it bites
- **Silent float64:** `torch.from_numpy(np_array)` keeps float64 from NumPy defaults; a float64 input then promotes every op it touches. Cast at the boundary: `torch.from_numpy(x).float()` or `torch.as_tensor(x, dtype=torch.float32)`.
- **In-place ops cannot upcast:** `int_tensor += 0.5` raises `RuntimeError: result type Float can't be cast to the desired output type Long`. Use out-of-place or cast first. Check with `torch.can_cast(from_, to)`.
- **Integer division:** `/` always returns float (true division); use `torch.div(a, b, rounding_mode="floor")` or `//` for integer results.
- **uint8 masks:** indexing with uint8 is deprecated; use `bool`.
- **Mixed-precision weights:** a float32 buffer added to bf16 activations promotes to float32 outside autocast, doubling activation memory. Register buffers in the model dtype or cast in `forward`.
- **Loss on half tensors:** compute reductions in float32 (`loss.float()`), since fp16 sums overflow above 65504.

## Casting API
- `t.to(torch.bfloat16)`, `t.half()`, `t.float()`; `model.to(dtype)` casts parameters and floating buffers only (integer buffers like `num_batches_tracked` stay int).
- `torch.set_default_dtype(torch.float64)` changes what Python floats create; avoid in libraries.
- `t.to(dtype, copy=False)` returns self if already that dtype (no copy).

## Verify
- [ ] Add `assert x.dtype == torch.float32` at data-loader output in tests.
- [ ] Run one step with `torch.set_printoptions` off and print `{n: p.dtype for n, p in model.named_parameters()}` plus activation dtypes via a forward hook.
- [ ] Peak memory matches the expected element size (2 bytes bf16, 4 bytes fp32).
