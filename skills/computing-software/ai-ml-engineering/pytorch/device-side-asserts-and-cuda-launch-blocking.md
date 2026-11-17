---
id: computing-software.ai-ml-engineering.pytorch.device-side-asserts-and-cuda-launch-blocking
name: device-side-asserts-and-cuda-launch-blocking
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, cuda-launch-blocking, device-side-assert, cuda-errors, debugging, index-out-of-bounds]
level: practitioner
status: docs-checked
description: "Debug misleading asynchronous CUDA errors (device-side assert, illegal memory access) with CUDA_LAUNCH_BLOCKING, a CPU repro and compute-sanitizer memcheck."
sources:
  - https://github.com/pytorch/pytorch/blob/main/docs/source/notes/cuda.md
  - https://docs.nvidia.com/compute-sanitizer/ComputeSanitizer/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Device-side asserts and CUDA_LAUNCH_BLOCKING

**Symptom:** a CUDA error such as a device-side assert or illegal memory access, with a stack trace pointing at an unrelated later line.

## Why the trace lies
GPU operations are asynchronous. PyTorch's CUDA notes: with asynchronous execution such an error is not reported until after the operation is actually executed, so the stack trace does not show where it was requested.

## Get the real location
1. `CUDA_LAUNCH_BLOCKING=1 python train.py` forces synchronous computation, so the traceback points at the faulty op. Debugging only; it removes the asynchrony.
2. Run the same batch on CPU: CPU kernels raise readable index and shape errors.
3. `compute-sanitizer --tool memcheck python repro.py` for memory errors in custom kernels. NVIDIA's docs say memcheck is the default tool when you run the Compute Sanitizer application.

## Common causes to check
| Cause | Check |
|---|---|
| Class labels outside `[0, num_classes)` in a classification loss | assert `y.min() >= 0` and `y.max() < C`; use the loss's `ignore_index` for padding labels |
| Token ids at or above the embedding size (new tokenizer tokens, wrong vocab) | compare `ids.max()` with the embedding's `num_embeddings` |
| Index, gather or scatter with out-of-range indices | bounds-check the indices on CPU |
| Custom CUDA kernel bug | compute-sanitizer |

## Verify
- [ ] Add cheap data assertions in the dataset or collate function so bad batches fail on CPU with a clear message.
- [ ] Re-run without `CUDA_LAUNCH_BLOCKING` for normal speed.

## Checked
2026-11-01. Confirmed in the PyTorch CUDA semantics notes: asynchronous error reporting and CUDA_LAUNCH_BLOCKING=1; in the NVIDIA Compute Sanitizer manual: `compute-sanitizer --tool memcheck` and that memcheck is the default tool. Removed (not confirmed in fetched sources): TORCH_USE_CUDA_DSA, exact error messages, the claim that the CUDA context is unusable after an assert, BCE input range and position-id causes, notebook restart advice.
Method: documentation only; no commands were run.
