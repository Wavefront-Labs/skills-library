---
id: computing-software.ai-ml-engineering.pytorch.sparse-tensors-coo-csr
name: sparse-tensors-coo-csr
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, sparse-tensors, sparse-coo, sparse-csr, torch-sparse, semi-structured-sparsity, sparse-matmul]
level: practitioner
status: gated
description: "Use PyTorch sparse tensors: build COO and CSR layouts, coalesce, sparse-dense matmul, autograd support limits, 2:4 semi-structured sparsity and when dense is faster."
sources:
  - https://pytorch.org/docs/stable/sparse.html
  - https://pytorch.org/tutorials/advanced/semi_structured_sparse.html
  - https://pytorch.org/docs/stable/generated/torch.sparse.mm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sparse tensors (COO / CSR)

## Rule of thumb first
Unstructured sparse kernels usually only beat dense matmul at very high sparsity (the break-even depends on hardware and shapes; no universal threshold). Below that, keep tensors dense and mask. Measure before converting.

## Layouts
| Layout | Build | Good for |
|---|---|---|
| COO | `torch.sparse_coo_tensor(indices, values, size)` | construction, arbitrary dims, accumulating duplicates |
| CSR | `torch.sparse_csr_tensor(crow, col, values, size)` or `x.to_sparse_csr()` | fast row slicing and SpMM (2D) |
| CSC / BSR / BSC | `to_sparse_csc()`, `to_sparse_bsr(blocksize)` | column access, block-sparse kernels |

```python
i = torch.tensor([[0, 1, 1], [2, 0, 2]])       # 2 x nnz (row, col)
v = torch.tensor([3., 4., 5.])
A = torch.sparse_coo_tensor(i, v, (2, 3)).coalesce()   # sums duplicate indices, sorts
A.indices(), A.values(), A.to_dense()
y = torch.sparse.mm(A, dense_B)                # or A @ dense_B
```
- Uncoalesced COO (duplicates) is legal; many ops coalesce implicitly at a cost. Call `.coalesce()` once after construction.
- `A.is_sparse`, `A.layout` (`torch.sparse_coo`, `torch.sparse_csr`).

## Autograd
- `torch.sparse.mm(sparse, dense)` supports backward for both inputs; the gradient for the sparse input is sparse with the same pattern (masked semantics).
- Many dense ops have no sparse kernel and raise `NotImplementedError ... SparseCPU/SparseCUDA backend`. Check the support table in the docs before building a pipeline on them.
- Graph neural nets: adjacency as sparse CSR plus `torch.sparse.mm`, or use PyTorch Geometric's `SparseTensor` / `torch_scatter` which are more complete.

## Embeddings
`nn.Embedding(..., sparse=True)` produces sparse gradients; only `optim.SGD`, `optim.SparseAdam` and `Adagrad` accept them. Large recommender tables use this to avoid dense gradient updates.

## 2:4 semi-structured sparsity (Ampere+)
Exactly 2 non-zeros in every group of 4 along a row, accelerated on NVIDIA GPUs from Ampere onward. The PyTorch docs give no speedup figure (only 56.25% storage compression for fp16/bf16 and 62.5% for int8): measure it. `to_sparse_semi_structured` accepts CUDA tensors only (tested: a CPU tensor raises "Only CUDA tensors are currently supported").
```python
from torch.sparse import to_sparse_semi_structured
W = prune_2_4(linear.weight)                    # your pruning step zeroes 2 of every 4
linear.weight = torch.nn.Parameter(to_sparse_semi_structured(W.half()))
```
Accuracy needs fine-tuning after pruning; supported dtypes are fp16/bf16/int8; 2D only, with both dimensions a positive multiple of 64 (fp16/bf16) or 128 (int8) per the docs. (gated: unconfirmed, speed and accuracy on real GPUs were not run here)

## Gotchas
- `torch.save` of sparse tensors works; `safetensors` does not store sparse layouts (densify or save indices/values).
- `.to_dense()` on a huge sparse tensor allocates the full dense size and OOMs.
- Sparse CSR on CPU supports MKL SpMM; on GPU uses cuSPARSE. Benchmark both layouts.
