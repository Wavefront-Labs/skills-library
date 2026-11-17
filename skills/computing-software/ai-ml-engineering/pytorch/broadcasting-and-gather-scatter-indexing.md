---
id: computing-software.ai-ml-engineering.pytorch.broadcasting-and-gather-scatter-indexing
name: broadcasting-and-gather-scatter-indexing
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, broadcasting-rules, gather-scatter, advanced-indexing, index-select, scatter-reduce, tensor-operations]
level: practitioner
status: gated
description: "Apply PyTorch broadcasting rules safely and use gather, scatter, scatter_reduce, index_select and advanced indexing for batched lookups without Python loops."
sources:
  - https://pytorch.org/docs/stable/notes/broadcasting.html
  - https://pytorch.org/docs/stable/generated/torch.gather.html
  - https://pytorch.org/docs/stable/generated/torch.Tensor.scatter_reduce_.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Broadcasting and gather / scatter indexing

## Broadcasting rules
Two tensors broadcast if, aligning shapes from the right, each dim pair is equal, one of them is 1, or one is missing. The result takes the max per dim.
- `(N, 1) - (N,)` -> `(N, N)`. This is the most common silent bug (MSE between `(N,1)` predictions and `(N,)` targets). Assert `pred.shape == target.shape` or `squeeze(-1)` explicitly.
- Add axes on purpose with `x[:, None]` or `unsqueeze`. Pairwise distances: `(x[:, None, :] - y[None, :, :]).norm(dim=-1)` -> `(N, M)`; for large N prefer `torch.cdist`, which avoids the `(N, M, D)` temporary.
- In-place ops cannot broadcast the left side: `a.add_(b)` requires `b` to broadcast to `a.shape`.
- `torch.broadcast_shapes(s1, s2)` checks compatibility without allocating.

## gather: pick values per row
`out[i][j] = x[i][idx[i][j]]` for `dim=1`. `idx` must have the same number of dims as `x` (tested error: "Index tensor must have the same number of dimensions as input tensor"); use int64 indices (an int32 index also ran on this build, but int64 is the documented type).
```python
logp = logits.log_softmax(-1)             # (N, C)
picked = logp.gather(1, y.unsqueeze(1)).squeeze(1)   # (N,) log-prob of the true class
# token log-probs for LM: logits (B, T, V), labels (B, T)
tok_lp = logits.log_softmax(-1).gather(-1, labels.unsqueeze(-1)).squeeze(-1)
```
Equivalent advanced indexing: `logp[torch.arange(N), y]`.

## scatter / scatter_add / scatter_reduce: write or aggregate by index
```python
onehot = torch.zeros(N, C).scatter_(1, y.unsqueeze(1), 1.0)
# segment sum: sum features per group id
out = torch.zeros(G, D).index_add_(0, group_ids, feats)
# segment mean / max
out = torch.zeros(G, D).scatter_reduce(0, group_ids[:, None].expand(-1, D), feats, reduce="mean", include_self=False)
```
- `scatter_` with duplicate indices is nondeterministic about which write wins. Use `scatter_reduce` or `index_add_` when duplicates exist.
- On CUDA, `index_add`, `scatter_add_` and `scatter_reduce` (sum/mean) are on the `torch.use_deterministic_algorithms` list of ops that are nondeterministic or switch to a slower deterministic path (list read from the installed torch docstring; CUDA behaviour itself not run here, no GPU).
- `include_self=False` matters for `amax`/`mean`: otherwise the initial zeros take part.

## Advanced indexing
- `x[idx]` with a LongTensor or bool mask always copies. `x[mask] = v` writes in place.
- Mixing slices and index tensors: `x[:, idx]` keeps dim 0; two index tensors broadcast against each other: `x[rows, cols]` picks pairs, not a grid. For a grid use `x[rows[:, None], cols]`.
- `index_select(dim, idx)` is the explicit form and works with `torch.compile` and ONNX export more reliably.
- Out-of-range indices on CUDA raise a device-side assert that poisons the context (gated: unconfirmed, source is paywalled or blocked); rerun with `CUDA_LAUNCH_BLOCKING=1` or on CPU to see the real line.

## Verify
Write the loop version on a tiny input and compare with `torch.testing.assert_close` before trusting the vectorised one.
