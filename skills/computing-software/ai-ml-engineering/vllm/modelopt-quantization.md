---
id: computing-software.ai-ml-engineering.vllm.modelopt-quantization
name: modelopt-quantization
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [modelopt, nvfp4, hf-quant-config, quant-algo, modelopt-fp4]
level: advanced
status: docs-checked
description: "Serve NVIDIA Model Optimizer checkpoints, map quant_algo values to quantization names, and quantize with mtq."
sources:
  - https://docs.vllm.ai/en/latest/features/quantization/modelopt/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run ModelOpt PTQ/QAT checkpoints (FP8, NVFP4, MXFP8, mixed) in vLLM.

Install the library with `pip install nvidia-modelopt`. vLLM detects ModelOpt checkpoints through `hf_quant_config.json` and supports these `quantization.quant_algo` values:
- `FP8`: per-tensor weight scale plus optional static activation scale. On GPUs that need it (e.g. AMD MI300), E4M3FN weights convert to E4M3FNUZ.
- `FP8_PER_CHANNEL_PER_TOKEN`: per-channel weight scale, dynamic per-token activations.
- `FP8_PB_WO`: block-scaled FP8 weight-only (typically 128x128 blocks).
- `NVFP4` and `W4A16_NVFP4`: use `quantization="modelopt_fp4"`.
- `MXFP8`: use `quantization="modelopt_mxfp8"`.
- `MIXED_PRECISION`: per-layer formats from `quantized_layers`; use `quantization="modelopt_mixed"`.

NVFP4 kernels are chosen automatically (CUTLASS, FlashInfer, Marlin, others). Without a native FP4 GEMM kernel, vLLM falls back to weight-only W4A16 via Marlin with a warning, which may reduce throughput. Override with `--linear-backend` (values include `cutlass`, `flashinfer_cutlass`, `flashinfer_cutedsl`, `flashinfer_trtllm`, `flashinfer_cudnn`, `marlin`); this replaces the deprecated `VLLM_NVFP4_GEMM_BACKEND` variable. For MXFP8 with BF16 activations on SM100-family GPUs, use `--linear-backend flashinfer_trtllm`.

Benchmarking with random weights: `--load-format dummy`; not for quality evaluation. `VLLM_MOE_SKIP_PADDING=0` disables the CUDA-graph padding-row skip in the Muse Spark NVFP4 FlashInfer TRT-LLM path, for comparisons.

Quantize with the PTQ API: `mtq.quantize(model, mtq.FP8_DEFAULT_CFG, forward_loop)`, then export via `export_hf_checkpoint(model, export_dir)` inside `torch.inference_mode()`.

## Checked

2026-11-03. Confirmed against the NVIDIA Model Optimizer page (docs.vllm.ai/en/latest/): quant_algo values, quantization names, NVFP4 fallback, --linear-backend values and the PTQ example. Narrowed VLLM_MOE_SKIP_PADDING=0 to the path the page describes.

Method: documentation only; no commands were run.
