---
id: computing-software.ai-ml-engineering.model-training.sources-of-gpu-nondeterminism
name: sources-of-gpu-nondeterminism
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, gpu-nondeterminism, atomic-operations, floating-point-reduction, cudnn-benchmark, reproducibility]
level: practitioner
status: draft
description: "Identify why identical GPU training runs diverge: atomic float adds, cuDNN autotuning, reduction order, TF32, multi-GPU collectives, data order, and how much it matters."
sources:
  - https://pytorch.org/docs/stable/notes/randomness.html
  - https://docs.nvidia.com/deeplearning/cudnn/latest/developer/misc.html#reproducibility-determinism
  - https://github.com/NVIDIA/framework-reproducibility
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sources of GPU nondeterminism

Floating-point addition is not associative: `(a + b) + c != a + (b + c)` in the last bits. Any change in summation order changes results slightly, and training amplifies tiny differences into different final weights.

## Main sources
| Source | Where | Control |
|---|---|---|
| Atomic adds (order depends on thread scheduling) | `index_add_`, `scatter_add_`, embedding backward, some conv/pooling backward, `bincount`, CTC loss, custom kernels | `torch.use_deterministic_algorithms(True)`; TF `tf.config.experimental.enable_op_determinism()` |
| cuDNN algorithm autotuning | conv layers with `cudnn.benchmark=True` | `torch.backends.cudnn.benchmark=False`, `deterministic=True` |
| cuBLAS split-K / workspace | large matmuls | `CUBLAS_WORKSPACE_CONFIG=:4096:8` |
| Compiler autotuning | `torch.compile` max-autotune, XLA, Triton autotune | fixed configs / caches |
| Multi-GPU collectives | NCCL all-reduce order, ring vs tree choice | fixed world size and NCCL algorithm (`NCCL_ALGO`); usually accepted as noise |
| Precision modes | TF32, bf16/fp16 autocast | changes values, deterministic per setting but differs across hardware |
| Data pipeline | worker scheduling, `tf.data` parallel map with `deterministic=False`, shuffling without seed | seeds, `deterministic=True`, fixed worker count |
| Batch composition | changing batch size/GPU count | keep identical for comparisons |
| Hardware and versions | different GPU models, driver, CUDA, cuDNN, framework versions | pin environment; cross-hardware bitwise equality isn't promised |

## How much does it matter
- Final metrics typically vary by an amount comparable to seed variance. For model selection this is noise to measure, not eliminate.
- It matters when debugging (a loss spike you can't reproduce), auditing/regulated contexts, and regression tests of training code.
- Deterministic mode costs speed (often 10-50% on conv-heavy models, more for some scatter-heavy models).

## Diagnose a divergence
1. Same seed, two runs, deterministic flags off: log loss per step; note the first differing step.
2. Turn on `use_deterministic_algorithms(True, warn_only=True)`: warnings list nondeterministic ops actually used.
3. Fix seeds and flags; if still diverging, compare data batches (hash input tensors per step) to rule out the pipeline.
4. Check inference: eval with `model.eval()` and no dropout should be deterministic on a fixed batch; if not, a kernel is nondeterministic even in forward.

## Inference consistency
LLM serving with dynamic batching changes batch composition per request, so the same prompt can produce different greedy outputs (batch-dependent kernels). Batch-invariant kernels or fixed batch configs are needed for strict consistency.

## Verify
With all controls on, two runs produce identical losses for 1000 steps on the same machine; document the remaining sources (multi-GPU, cross-hardware) accepted as noise.
