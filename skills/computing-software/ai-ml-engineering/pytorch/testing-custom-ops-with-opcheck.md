---
id: computing-software.ai-ml-engineering.pytorch.testing-custom-ops-with-opcheck
name: testing-custom-ops-with-opcheck
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, custom-ops, opcheck, gradcheck, fake-tensor, op-testing, torch-library]
level: practitioner
status: verified
description: "Test PyTorch custom operators with torch.library.opcheck: schema, fake/meta, autograd registration and AOT dispatch checks, plus gradcheck and numerical comparison tests."
sources:
  - https://pytorch.org/docs/stable/library.html#torch.library.opcheck
  - https://pytorch.org/docs/stable/notes/custom_operators.html
  - https://pytorch.org/docs/stable/generated/torch.autograd.gradcheck.gradcheck.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing custom ops with opcheck

**Goal:** catch the subtle registration bugs that make a custom op work in eager but break under `torch.compile`, export or autograd.

## opcheck
```python
import torch
from torch.library import opcheck

dev = "cuda" if torch.cuda.is_available() else "cpu"   # run here with "cpu"
samples = [
    (torch.randn(3, device=dev),),
    (torch.randn(2, 5, device=dev, requires_grad=True),),
    (torch.randn(0, device=dev),),                                # empty input
    (torch.randn(4, 4, device=dev).t(),),                         # non-contiguous
]
for args in samples:
    opcheck(torch.ops.mylib.my_op.default, args)
```
It runs a set of utilities, including:
- `test_schema`: the op's declared schema matches its behaviour (mutation and aliasing declarations are honest).
- `test_autograd_registration`: autograd is registered correctly for ops that take tensors requiring grad.
- `test_faketensor`: the fake/meta implementation returns outputs with the same shapes, dtypes and strides as the real one.
- `test_aot_dispatch_dynamic`: works through AOTAutograd with dynamic shapes (what `torch.compile` uses).
Pass `test_utils=[...]` to run a subset while debugging. `opcheck` returns a dict of `SUCCESS` strings and raises `OpCheckError` on failure (`raise_exception=False` returns the failures instead). Run on torch 2.14 CPU: a correct NumPy-backed op passed all four tests for the four sample shapes above; a fake impl returning size 4 for a size-3 output failed `test_faketensor` ("found mismatched tensor metadata: Shapes torch.Size([3]) and torch.Size([4]) are not equal"); an op that mutated an input without declaring it failed `test_schema`.

## Numerical tests
```python
torch.testing.assert_close(torch.ops.mylib.my_op(x), reference(x), rtol=1e-4, atol=1e-5)
x64 = torch.randn(5, dtype=torch.double, device=dev, requires_grad=True)
torch.autograd.gradcheck(torch.ops.mylib.my_op, (x64,))
```
`gradcheck` compares analytic gradients with finite differences; use double precision and small inputs (it returned `True` for the sine op with `register_autograd`).

## Sample selection
Cover: several shapes (including size 0 and 1), non-contiguous strides, each supported dtype, each device implementation, `requires_grad` on and off. Most fake-impl bugs show up with non-contiguous or empty inputs.

## In CI
Run opcheck + numerical tests in pytest parametrised over samples; also a `torch.compile(fullgraph=True)` smoke test calling the op.

## Verify
- [ ] opcheck passes for every sample input.
- [ ] gradcheck passes in double precision.
- [ ] Compile smoke test runs without graph breaks.
