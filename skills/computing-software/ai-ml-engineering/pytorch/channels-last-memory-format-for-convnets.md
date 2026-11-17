---
id: computing-software.ai-ml-engineering.pytorch.channels-last-memory-format-for-convnets
name: channels-last-memory-format-for-convnets
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, channels-last-memory-format, channels-last, memory-format, convolution-performance, tensor-cores, nhwc]
level: practitioner
status: gated
description: "Switch conv nets to torch.channels_last (NHWC) for Tensor Core speedups under AMP, convert model and inputs, keep layout through the net and verify it with a profiler."
sources:
  - https://pytorch.org/tutorials/intermediate/memory_format_tutorial.html
  - https://pytorch.org/docs/stable/tensor_attributes.html#torch-memory-format
  - https://docs.nvidia.com/deeplearning/performance/dl-performance-convolutional/index.html#tensor-layout
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# channels_last memory format for conv nets

**Why:** NCHW is PyTorch's default, but cuDNN Tensor Core convolutions run natively in NHWC. With NCHW inputs, cuDNN inserts transpose kernels around every conv (gated: unconfirmed, source is paywalled or blocked). No GPU was available here, so every speed statement below is unmeasured; the layout behaviour was run on CPU with torch 2.14. `channels_last` keeps the logical shape `(N, C, H, W)` and changes only the strides, so no model code changes.

## Convert
```python
model = model.to(device, memory_format=torch.channels_last)   # 4D params (conv weights) become NHWC strided
for x, y in loader:
    x = x.to(device, non_blocking=True, memory_format=torch.channels_last)
    with torch.autocast("cuda", dtype=torch.bfloat16):
        loss = criterion(model(x), y)
```
- 5D (video / 3D conv): `torch.channels_last_3d`; `channels_last` on a 5D tensor raises `required rank 4 tensor to use channels_last format`.
- Check: `x.is_contiguous(memory_format=torch.channels_last)`; strides look like `(H*W*C, 1, W*C, C)` (a `(2, 3, 16, 16)` input gave `(768, 1, 48, 3)`).

## When it pays
- Conv nets (ResNet, EfficientNet, UNet, detection backbones) under fp16/bf16 AMP on Volta or newer: typically 10-30% faster training (gated: unconfirmed, source is paywalled or blocked).
- Little or nothing for fp32 without TF32, for transformers (no convs), or on CPU without oneDNN paths (CPU does support the layout and often helps for inference) (gated: unconfirmed, source is paywalled or blocked).
- Channel counts that are multiples of 8 keep Tensor Core kernels eligible (gated: unconfirmed, source is paywalled or blocked).

## Keeping the layout
Conv, BN, ReLU, max-pooling and elementwise ops preserved channels_last in the CPU run (including `torch.cat` of a channels_last and an NCHW tensor). Layout is lost after:
- `x.view(...)` on a channels_last tensor raises `view size is not compatible with input tensor's size and stride`; `x.contiguous()` returns NCHW (use `x.contiguous(memory_format=torch.channels_last)`); `reshape` and reductions such as `mean((2, 3))` also return NCHW-contiguous results.
- Custom ops / extensions that assume NCHW strides and call `.contiguous()` internally.
A conversion in the middle of the net costs a full copy each step; find it in the profiler as `aten::copy_` / `aten::contiguous` around a specific layer.

## Verify
```python
from torch.profiler import profile, ProfilerActivity
with profile(activities=[ProfilerActivity.CUDA]) as p:
    model(x).sum().backward()
print(p.key_averages().table(sort_by="cuda_time_total", row_limit=15))
```
Look for NCHW-to-NHWC transpose kernels (`nchwToNhwcKernel`, `nhwcToNchwKernel`) disappearing after the switch (gated: unconfirmed, source is paywalled or blocked), then compare step time over 50+ steps after warm-up. `torch.profiler.profile` itself ran on CPU (with `ProfilerActivity.CPU`); the CUDA activity needs a GPU. Numerics: a channels_last Conv-BN-ReLU-pool stack matched the NCHW output within 1e-5 on CPU.

## Gotchas
- `torch.compile` handles layout itself (Inductor picks it), but converting inputs still helps on eager fallbacks (not run: Inductor needs a C++ compiler the test host lacks) (gated: unconfirmed, source is paywalled or blocked).
- Exporting to ONNX / TensorRT: layout is a stride detail and is not exported; the runtime chooses its own (gated: unconfirmed, source is paywalled or blocked).
- Checkpoints saved from a channels_last model load fine into NCHW models (checked: values equal, and the loaded weight is NCHW-contiguous).
