---
id: computing-software.ai-ml-engineering.pytorch.flop-counting-and-achieved-tflops
name: flop-counting-and-achieved-tflops
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, flop-counter, mfu, tflops, flopcounter-mode, performance-measurement, roofline]
level: practitioner
status: gated
description: "Count model FLOPs with torch.utils.flop_counter.FlopCounterMode, compute achieved TFLOPS and MFU against hardware peak, and use them to judge how much speedup is left."
sources:
  - https://pytorch.org/docs/stable/generated/torch.utils.flop_counter.FlopCounterMode.html
  - https://arxiv.org/abs/2204.02311
  - https://github.com/pytorch/torchtitan/blob/main/torchtitan/tools/utils.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# FLOP counting and achieved TFLOPS

## Count
```python
from torch.utils.flop_counter import FlopCounterMode
x = torch.randn(8, 3, 224, 224, device="cuda")
with FlopCounterMode(display=True, depth=2) as fc:     # per-module table
    model(x).sum().backward()
total = fc.get_total_flops()                           # forward + backward of this batch
```
- Counts matmul, conv, attention (SDPA) analytically from shapes; elementwise ops are ignored (they are memory-bound anyway). Checked on torch 2.14: `nn.Linear(64, 32)` on a batch of 10 counted 40960 = 2*10*64*32, conv matched 2 x MACs, `relu(x) + 1` counted 0, and a forward+backward of the linear layer counted 81920 (weight-gradient mm only, since the input needs no gradient). `display=True` needs the `tabulate` package (`ModuleNotFoundError` without it).
- Attention: SDPA on tensors counted 16384 = 4*B*H*S*S*D under the meta device, but a CPU `scaled_dot_product_attention` call counted 0 in 2.14 (the CPU kernel is not registered), so count attention on meta or CUDA.
- Works on the meta device: build the model under `torch.device("meta")` and count without a GPU (a 512-wide `TransformerEncoderLayer` on a 4x128 batch counted 3355443200 FLOPs, equal to 2 x matmul-weight-params x tokens plus the attention term).
- FLOPs here are floating-point operations (one multiply-add = 2).

## Transformer shortcut
Training FLOPs per token ~= 6 x N (params) + attention term 12 x n_layers x d_model x seq_len (PaLM appendix B). Forward only ~= 2N per token. Use to sanity-check the counter. The forward-only rule was checked here: counted FLOPs equalled 2 x (weights in 2-D parameters) x tokens plus 4 x d_model x seq_len x tokens for the attention scores and values; the 6N and 12 L d s training forms were not re-derived (gated: unconfirmed, source is paywalled or blocked).

## Achieved TFLOPS and MFU
```python
torch.cuda.synchronize(); t0 = time.perf_counter()
for _ in range(steps): train_step()
torch.cuda.synchronize(); dt = (time.perf_counter() - t0) / steps
achieved = total / dt / 1e12                        # TFLOPS per GPU (divide total by world size if counted globally)
mfu = achieved / peak_tflops
```
Peak dense numbers (no sparsity): A100 bf16 312, H100 SXM bf16 ~989, H100 PCIe ~756, L4 bf16 ~121, RTX 4090 bf16 ~165 (with fp32 accumulate figures differing on consumer cards) (gated: unconfirmed, source is paywalled or blocked). Use the dense, not the "with sparsity" datasheet column, and confirm the figure in the vendor datasheet for your exact SKU. No GPU was available to time anything.

## Reading MFU
- Rules of thumb, not measured here: 40-60% for large transformer training is good; 20-30% is typical before tuning; below 15% means something is very wrong (input bound, tiny batches, fp32 matmuls, syncs) (gated: unconfirmed, source is paywalled or blocked).
- HFU (hardware FLOPs utilisation) counts recomputed activation-checkpoint FLOPs too; MFU does not. Report which one.
- Small models cannot reach high MFU: elementwise and launch overhead dominate. Compare against similar-size published runs.

## Use it
Before optimising, compute MFU. If it is already high, gains must come from fewer FLOPs (smaller model, FP8, sparsity), not kernel tuning. If low, profile (see torch.profiler) for idle GPU time and memory-bound kernels.

## Gotchas
- Time must exclude warm-up and compile steps.
- With TF32 disabled, fp32 matmuls run at the non-tensor-core fp32 peak (~19.5 TFLOPS on A100) (gated: unconfirmed, source is paywalled or blocked), not the TF32 one.
- Per-GPU FLOPs under data parallel: count one replica's batch.
