---
id: computing-software.ai-ml-engineering.pytorch.inplace-modification-errors-in-backward
name: inplace-modification-errors-in-backward
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, autograd, inplace-autograd-error, version-counter, in-place-ops, debugging]
level: practitioner
status: verified
description: "Fix 'one of the variables needed for gradient computation has been modified by an inplace operation': version counters, finding the op and safe replacements."
sources:
  - https://pytorch.org/docs/stable/notes/autograd.html#in-place-operations-with-autograd
  - https://pytorch.org/docs/stable/autograd.html#anomaly-detection
  - https://pytorch.org/docs/stable/generated/torch.Tensor.clone.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# In-place modification errors in backward

**Symptom:** `RuntimeError: one of the variables needed for gradient computation has been modified by an inplace operation: [torch.FloatTensor [4, 3]], which is output 0 of Sigmoid, is at version 1; expected version 0 instead.` (torch 2.14 CPU wording; the dtype prefix is `torch.cuda.FloatTensor` on GPU)

## Why
Every tensor has a version counter (`t._version`) bumped by in-place ops (`add_`, `relu_`, `x[idx] = ...`, `+=`, `inplace=True` modules). Ops that save a tensor for backward record its version; backward checks it is unchanged.

## Find the culprit
1. Read the message: shape, dtype and the op name (`Sigmoid`, `Relu`, `Softmax`, `AsStrided`) point at the op whose output was saved and then modified.
2. Turn on anomaly mode for one step; the error then includes the forward stack trace of the op:
```python
with torch.autograd.detect_anomaly():
    loss = model(x).sum(); loss.backward()
```
3. Search the code for `inplace=True`, `_(`, `+=`, `*=`, slice assignment and `.data` writes on that tensor.

## Common causes and fixes
| Pattern | Fix |
|---|---|
| `nn.ReLU(inplace=True)` after an op whose output is saved (e.g. sigmoid, or a residual branch reused) | `inplace=False` |
| `x += residual` where `x` is saved by the previous layer | `x = x + residual` |
| `h[:, t] = cell(h[:, t-1])` in an RNN loop | collect in a list, `torch.stack` at the end |
| Optimizer step between two backward passes on a retained graph (GAN loops) | compute both losses before `step()`, or recompute the forward |
| Modifying a parameter in place (`with torch.no_grad(): p.mul_(2)`) between its use in the forward and `backward()` | do it after `backward()`. Writing through `p.data` skips the version check and silently gives wrong gradients instead of an error (run here: no error), so do not use it as a workaround |
| Editing a softmax output in place (`probs[:, 0] = 0`); softmax saves its output, not its input (masking the input after softmax did not error when run) | `probs = probs * keep` or `masked_fill` before the softmax |

`clone()` before the in-place op is the quick fix when you need both values.

## Notes
- Prefer out-of-place ops by default; use in-place ones only where profiling shows a need.
- `torch.no_grad()` in-place edits of leaf parameters are fine (that is how optimizers work) as long as no live graph saved them.
- Inference tensors created under `torch.inference_mode()` have no version counter (`t._version` raises "Inference tensors do not track version counter"), so this error cannot occur there; in-place updates to them outside inference mode raise a different error.

## Verify
- [ ] The step runs with `detect_anomaly()` off and on.
- [ ] Gradients match a version of the model with every `inplace=True` removed (`torch.allclose` on a fixed batch).
