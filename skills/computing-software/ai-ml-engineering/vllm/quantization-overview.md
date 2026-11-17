---
id: computing-software.ai-ml-engineering.vllm.quantization-overview
name: quantization-overview
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [quantization, linear-backend, kernel-config, hardware-support, quantization-plugin]
level: practitioner
status: docs-checked
description: "See supported quantization formats, the hardware compatibility table and --linear-backend overrides."
sources:
  - https://docs.vllm.ai/en/latest/features/quantization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick a quantization format that your hardware supports.

Supported formats in the docs: AutoAWQ, BitsAndBytes, GPTQModel, Intel Neural Compressor, LLM Compressor (FP8 W8A8, INT4 W4A16, INT8 W4A8, INT8 W8A8), NVIDIA Model Optimizer, Online Quantization, AMD Quark, Quantized KV Cache, TorchAO and FP8 ViT encoder attention. The docs recommend starting with LLM Compressor.

Hardware table highlights (Volta SM 7.0, Turing 7.5, Ampere 8.0/8.6, Ada 8.9, Hopper 9.0):
- AWQ: Turing to Hopper, Intel GPU, x86 CPU; not Volta or AMD.
- GPTQ: Volta to Hopper, Intel GPU, x86 CPU.
- Marlin (GPTQ/AWQ/FP8/FP4): Ampere, Ada, Hopper (Turing partly, but no Marlin MXFP4).
- llm-compressor INT8 W8A8: Turing to Hopper, x86 and Arm CPU. INT8 W4A8: Arm CPU only.
- llm-compressor FP8 W8A8: Ada, Hopper, AMD GPU.
- bitsandbytes and DeepSpeedFP: Volta to Hopper. GGUF: those plus AMD GPU.
- Intel Gaudi support moved to vLLM-Gaudi; TPU is covered by the TPU-Inference feature matrix.

Select linear backends: `--linear-backend` picks one backend for all quantized linear layers. For mixed-precision models override per scheme:

```bash
vllm serve <model> --linear-backend cutlass \
  --kernel-config '{"linear_backend_per_quant":{"nvfp4_w4a16":"humming"}}'
```

Per-quantization overrides win over `--linear-backend`; schemes without one use the global setting, including automatic selection when it is `auto`.

Marlin now always runs with 16-bit activations; the `VLLM_MARLIN_INPUT_DTYPE` variable is removed and setting it is an error. For W4A8 on GPTQ, AWQ or compressed-tensors weight-only checkpoints use `--quantization humming` with `VLLM_HUMMING_INPUT_QUANT_CONFIG='{"dtype":"int8"}'` (or `float8e4m3`). The `fp_quant` method and QuTLASS backend are removed; use a compressed-tensors checkpoint.

Out-of-tree methods: register a class inheriting `QuantizationConfig` with the `@register_quantization_config` decorator, with no change to the vLLM codebase.

## Checked

Method: 2026-11-08 read the quantization overview page in full. Format list, hardware table and linear-backend override matched. Added the Marlin 16-bit activation, humming W4A8 and removed fp_quant notes from the page.
