---
id: computing-software.ai-ml-engineering.pytorch.fp8-training-transformer-engine-torchao
name: fp8-training-transformer-engine-torchao
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, fp8-training, float8, transformer-engine, torchao, hopper]
level: practitioner
status: draft
description: "Train PyTorch models in FP8 on Hopper/Blackwell with Transformer Engine or torchao float8: scaling recipes, which layers to convert, and how to validate convergence."
sources:
  - https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/examples/fp8_primer.html
  - https://github.com/pytorch/ao/tree/main/torchao/float8
  - https://arxiv.org/abs/2209.05433
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FP8 training (Transformer Engine / torchao float8)

FP8 halves matmul cost again versus bf16 on H100/H200/B200 (sm_89+ for some paths, sm_90 for full speed). Formats: **E4M3** (more precision, used for weights/activations) and **E5M2** (more range, used for gradients). Because range is tiny, every tensor needs a scale factor.

## Where it pays
Large transformer matmuls (hidden size >= 2048-4096). Small layers lose time to casting/scaling overhead. Expect ~1.3-1.5x end-to-end over bf16 on big models; little or nothing on small ones.

## torchao float8 (pure PyTorch, works with FSDP2 and torch.compile)
```python
from torchao.float8 import convert_to_float8_training, Float8LinearConfig
config = Float8LinearConfig.from_recipe_name("tensorwise")   # or "rowwise" for better accuracy
def module_filter_fn(mod, fqn):
    return isinstance(mod, nn.Linear) and mod.in_features % 16 == 0 and mod.out_features % 16 == 0 \
        and "lm_head" not in fqn
convert_to_float8_training(model, config=config, module_filter_fn=module_filter_fn)
model = torch.compile(model)          # needed for performance: fuses the scaling
```
Keep the model in bf16 autocast/params; only selected Linear matmuls run in FP8. Dimensions must be multiples of 16.

## Transformer Engine
```python
import transformer_engine.pytorch as te
from transformer_engine.common.recipe import DelayedScaling, Format
recipe = DelayedScaling(fp8_format=Format.HYBRID, amax_history_len=1024, amax_compute_algo="max")
layer = te.Linear(4096, 4096)          # or te.TransformerLayer
with te.fp8_autocast(enabled=True, fp8_recipe=recipe):
    out = layer(x)
```
Delayed scaling uses the amax history of previous steps to pick scales (cheap, slight lag). Newer recipes include per-tensor current scaling and block scaling (MXFP8 on Blackwell).

## Rules of thumb
- Keep first embedding, final LM head, norms and softmax in higher precision.
- Optimizer states and master weights stay fp32/bf16.
- Use FP8 for the all-gather of weights under FSDP2 (`enable_fsdp_float8_all_gather=True` in torchao) for extra communication savings.
- Checkpoints remain in bf16/fp32; FP8 is a compute format here, not a storage format.

## Validate convergence
Run the same config in bf16 and FP8 for a few thousand steps; loss curves should overlap (difference within run-to-run noise). Watch for loss spikes appearing only in FP8: try rowwise scaling, exclude the offending layer, or increase amax history. Check speed with the profiler to confirm FP8 GEMMs (`sm90_xmma_gemm_e4m3...` kernels) actually run.
