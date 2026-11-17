---
id: computing-software.ai-ml-engineering.pytorch.quantization-aware-training
name: quantization-aware-training
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, quantization-aware-training, qat, torchao, fake-quantization, int8, int4]
level: practitioner
status: verified
description: "Recover accuracy lost to post-training quantization with QAT: torchao fake-quant flows (int8 dynamic activations, int4 weights), fine-tune schedule and convert step."
sources:
  - https://pytorch.org/blog/quantization-aware-training/
  - https://github.com/pytorch/ao/tree/main/torchao/quantization/qat
  - https://pytorch.org/docs/stable/quantization.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Quantization-aware training

**When:** post-training quantization (PTQ) drops accuracy beyond your budget (common for int4 weights, small models, or edge targets). QAT fine-tunes with simulated quantization so weights adapt to rounding error.

## Mechanism
Fake-quantize ops round values to the target grid in forward (quantize then dequantize) while gradients pass through with a straight-through estimator. After training, you convert to real low-precision kernels.

## torchao QAT flow (torchao 0.18.0, torch 2.14, run on CPU)
```python
import torch
from torchao.quantization import quantize_, Int8DynamicActivationIntxWeightConfig
from torchao.quantization.granularity import PerGroup
from torchao.quantization.qat import QATConfig, IntxFakeQuantizeConfig

act = IntxFakeQuantizeConfig(torch.int8, "per_token", is_symmetric=False)
wt = IntxFakeQuantizeConfig(torch.int4, group_size=32)
quantize_(model, QATConfig(activation_config=act, weight_config=wt, step="prepare"))  # Linear -> FakeQuantizedLinear
train(model, steps=N)                                                                 # fine-tune as usual
base = Int8DynamicActivationIntxWeightConfig(weight_dtype=torch.int4, weight_granularity=PerGroup(32))
quantize_(model, QATConfig(base, step="convert"))                                     # real quantized weights
```
This ran on a Linear-ReLU-Linear toy: after `prepare` the layers were `FakeQuantizedLinear`; after `convert` the weight was an `IntxUnpackedToInt8Tensor` and the forward still returned the right shape. The library's own deprecation text also shows a base-config form: `base_config = Int4WeightOnlyConfig(group_size=32)`, `quantize_(model, QATConfig(base_config, step="prepare"))`, train, `quantize_(model, QATConfig(base_config, step="convert"))` (not run here).

Older names still import in 0.18.0 but warn: `IntXQuantizationAwareTrainingConfig` / `FromIntXQuantizationAwareTrainingConfig` / `FakeQuantizeConfig` (the `FromIntX...` one emits "is deprecated and will be removed in a future release" and points to `QATConfig`; see https://github.com/pytorch/ao/issues/2630). `Int8DynamicActivationInt4WeightConfig` is gone from `torchao.quantization` (ImportError); use `Int8DynamicActivationIntxWeightConfig(weight_dtype=torch.int4, ...)`. Names keep changing between releases, so pin the torchao version and read its QAT README.

The legacy `torch.ao.quantization` eager flow (`get_default_qat_qconfig`, `prepare_qat`, `convert`) still ran on torch 2.14, but emits `DeprecationWarning: torch.ao.quantization is deprecated and will be removed in 2.10` and tells you to migrate to torchao's `quantize_` and pt2e APIs; on this Windows build `torch.backends.quantized.supported_engines` was only `['onednn']`, so check your engine (fbgemm/qnnpack) before relying on it.
## Recipe
- Start from the fully trained float model; QAT is a short fine-tune with a lower learning rate than the original training (choose the step budget and LR by validation accuracy; no standard figure was checked).
- Keep sensitive layers (embeddings, final head, first conv) in higher precision if accuracy is still short.

## Pitfalls
- QAT config must match the deployment kernel exactly (bit width, group size, symmetric vs asymmetric, per-token vs per-tensor), or gains vanish at convert time.
- Training is slower because of the fake-quant overhead (not timed here).
- Evaluate the **converted** model, not the fake-quant model, as final truth.

## Verify
- [ ] Table: float vs PTQ vs QAT accuracy, and latency/size of the converted model on target hardware.
