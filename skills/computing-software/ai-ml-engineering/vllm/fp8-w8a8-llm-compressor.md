---
id: computing-software.ai-ml-engineering.vllm.fp8-w8a8-llm-compressor
name: fp8-w8a8-llm-compressor
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [fp8, w8a8, llm-compressor, fp8-dynamic, fp8-per-tensor]
level: practitioner
status: docs-checked
description: "Quantize a model to FP8 W8A8 (FP8_DYNAMIC, no calibration data) and serve it, including kernel selection notes."
sources:
  - https://docs.vllm.ai/en/latest/features/quantization/llm_compressor/fp8/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: halve weight memory with FP8 weights and activations, up to 1.6x higher throughput per the docs.

Support: W8A8 on Ada Lovelace, Hopper, Blackwell (compute capability 8.9 or higher). Turing and Ampere run weight-only W8A16 via FP8 Marlin. Formats: E4M3 (values up to +/-448 and nan) and E5M2 (up to +/-57344, inf, nan; lower precision).

Install llm-compressor in a separate environment from vLLM: `pip install llmcompressor`; for evaluation `pip install vllm "lm-eval[api]>=0.4.12"`.

Recipe: target all `Linear` layers with `FP8_DYNAMIC` (static per-channel weights, dynamic per-token activations). Simple RTN needs no calibration data.

```python
recipe = QuantizationModifier(targets="Linear", scheme="FP8_DYNAMIC", ignore=["lm_head"])
oneshot(model=model, recipe=recipe)
model.save_pretrained("Meta-Llama-3-8B-Instruct-FP8-Dynamic")
```

Evaluate with `lm_eval --model vllm --model_args pretrained=$MODEL,add_bos_token=True --tasks gsm8k --num_fewshot 5 --limit 250`. Quantized models can be sensitive to the `bos` token, and `lm_eval` does not add one by default.

Kernel selection: vLLM logs `Selected <kernel> for <module>`. For block-quantized CUDA checkpoints it tries FlashInfer/DeepGEMM hybrid (Hopper), DeepGEMM, CUTLASS, Marlin, Triton, Humming, then PyTorch. If inference hangs, try `VLLM_USE_DEEP_GEMM=0` or `--linear-backend cutlass`. `--linear-backend` does not affect MoE experts (use `--moe-backend`), and an unsupported explicit backend raises an error.

No-calibration alternative: `--quantization="fp8_per_tensor"` online.

## Checked

2026-11-03. Confirmed against the FP8 W8A8 page (docs.vllm.ai/en/latest/): hardware support, FP8 formats, install, FP8_DYNAMIC recipe, lm_eval note and kernel selection.

Method: documentation only; no commands were run.
