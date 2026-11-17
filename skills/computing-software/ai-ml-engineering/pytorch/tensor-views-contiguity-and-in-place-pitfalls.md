---
id: computing-software.ai-ml-engineering.pytorch.tensor-views-contiguity-and-in-place-pitfalls
name: tensor-views-contiguity-and-in-place-pitfalls
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, tensor-views, contiguous-memory, strides, in-place-ops, autograd-version-counter, torch-tensors]
level: practitioner
status: verified
description: "Know when a PyTorch op returns a view or a copy, fix non-contiguous errors with contiguous/reshape, and avoid in-place ops that break autograd or alias data."
sources:
  - https://pytorch.org/docs/stable/tensor_view.html
  - https://pytorch.org/docs/stable/notes/autograd.html#in-place-operations-with-autograd
  - https://pytorch.org/docs/stable/generated/torch.Tensor.contiguous.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tensor views, contiguity and in-place pitfalls

A view shares storage with its base; writing to one changes the other. Bugs here are silent data corruption or `RuntimeError: ... one of the variables needed for gradient computation has been modified by an inplace operation`.

## Which ops return views
- Always views: `view`, `transpose`/`t`/`permute`, `narrow`, basic slicing `x[:, 1:]`, `select`, `unsqueeze`/`squeeze`, `expand`, `unfold`, `diagonal`, `as_strided`, `detach`, `view_as_real`.
- Sometimes views: `reshape`, `flatten`, `contiguous` (view if already compatible, else copy). Never rely on either behaviour from `reshape`.
- Always copies: advanced indexing `x[idx_tensor]`, `x[mask]`, `clone`, `to(other_dtype/device)`, `cat`, `stack`.
- Check: `y._base is x` (only when `x` is itself a base tensor; if `x` is a view its `_base` is the original) or `y.untyped_storage().data_ptr() == x.untyped_storage().data_ptr()`.

## Contiguity
- `x.is_contiguous()` and `x.stride()` tell you the layout. After `transpose`/`permute`, strides are reordered and `x.view(...)` raises `view size is not compatible with input tensor's size and stride`.
- Fix: `x.contiguous().view(...)` or just `x.reshape(...)`. `contiguous()` copies, so do it once, not per step in a hot loop.
- `expand` creates stride-0 dims (`x[:, :1].expand(3, 4).stride()` is `(4, 0)`): an in-place write to an expanded tensor raises `unsupported operation: more than one element of the written-to tensor refers to a single memory location` (torch 2.14). Use `repeat` or `clone()` (copies) if you need independent values.
- `channels_last` tensors report `is_contiguous()` False but `is_contiguous(memory_format=torch.channels_last)` True; that is intended.

## In-place ops and autograd
- In-place ops end in `_` (`add_`, `relu_`, `clamp_`) plus `x[...] = v`, `+=`, and `nn.ReLU(inplace=True)`.
- Autograd tracks a version counter per tensor. If a saved tensor (input to `sigmoid`, `exp`, `pow`, output of `relu`...) is mutated after the forward, backward raises the "modified by an inplace operation" error. The message names the op and version; set `torch.autograd.set_detect_anomaly(True)` to get the forward stack trace.
- Fix by replacing `x += y` with `x = x + y` in the forward, or dropping `inplace=True`.
- In-place on a leaf that requires grad raises `a leaf Variable that requires grad is being used in an in-place operation`. Wrap init code in `with torch.no_grad():`.
- Mutating `t.data` bypasses the version counter: autograd computes wrong gradients with no error. Use `with torch.no_grad(): t.copy_(...)` instead.

## Aliasing gotchas
- `a = b[0]; a.zero_()` zeros row 0 of `b`.
- `torch.from_numpy(arr)` and `tensor.numpy()` share memory; mutating the NumPy array changes the tensor. Use `torch.tensor(arr)` to copy.
- Storing `loss` (not `loss.item()`) in a list keeps the entire graph alive: memory grows each step.
- Saving a slice with `torch.save(big[:10])` serialises the whole storage. `clone()` first.

## Verify
- `torch.testing.assert_close` on outputs before and after replacing in-place ops.
- Run one step with `set_detect_anomaly(True)` after refactors that add in-place ops.
