---
id: computing-software.ai-ml-engineering.hugging-face.choosing-a-quantization-method
name: choosing-a-quantization-method
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, quantization-method-selection, bitsandbytes, gptq, awq, hqq, torchao, fp8]
level: practitioner
status: docs-checked
description: "Choose an LLM quantization method by goal: bnb for QLoRA training, AWQ/GPTQ for serving, FP8 on Hopper, GGUF for CPU, HQQ/torchao on-the-fly, with quality and speed trade-offs."
sources:
  - https://huggingface.co/docs/transformers/main/en/quantization/overview
  - https://huggingface.co/docs/transformers/main/en/quantization/selecting
  - https://docs.vllm.ai/en/latest/features/quantization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Choosing a quantization method

## Start from the goal
| Goal | Method | Notes |
|---|---|---|
| Fine-tune a big model on one GPU (QLoRA) | bitsandbytes 4-bit NF4 | on-the-fly, no calibration; slower inference |
| Serve with vLLM/TGI at high throughput on Ampere/Ada | AWQ or GPTQ (int4 weight-only, Marlin kernels) | needs a calibration pass or a pre-quantized checkpoint |
| Serve on Ada/Hopper | FP8 (W8A8) via llm-compressor / compressed-tensors | vLLM's hardware table lists llm-compressor FP8 W8A8 for Ada and Hopper |
| CPU, Mac, edge | GGUF (llama.cpp) | the Transformers overview marks CPU and Metal as supported |
| Quick experiments without calibration | HQQ or torchao int4/int8 | on-the-fly; torchao integrates with torch.compile |

## Quality expectations
Measure quality yourself. Bit widths per method in the Transformers overview: AQLM 1/2, AWQ 4, bitsandbytes 4/8, GPT-QModel 2/3/4/8, HQQ 1/8, torchao 4/8.

## Checklist
1. Is there a trusted pre-quantized checkpoint? Prefer it (saves calibration effort), but evaluate it yourself.
2. Does your serving engine and GPU support the kernel? (vLLM's quantization page has a hardware table: Marlin covers Ampere, Ada and Hopper; llm-compressor FP8 W8A8 covers Ada and Hopper).
3. Calibrate on data resembling your traffic (chat-formatted samples for chat models).
4. Evaluate on your own task set plus a perplexity check, and measure latency/throughput at production batch sizes.

## Loading examples
```python
# bitsandbytes: build a BitsAndBytesConfig (see the bitsandbytes page of the Transformers docs)
# and pass it as quantization_config=... to from_pretrained
```

## Verify
- [ ] Results table: method, memory, tokens/s, task score vs bf16 baseline.

## Checked
Date: 2026-10-28.
- Confirmed in the Transformers quantization overview and selecting pages: method list, bit widths, bitsandbytes for QLoRA, HQQ on-the-fly without calibration, torchao with torch.compile, GPTQModel/AWQ calibration, compressed-tensors for FP8. vLLM quantization page: hardware table for Marlin and llm-compressor FP8.
- Removed as unconfirmed: quality-loss claims, Blackwell/NVFP4 row, Q4_K_M, memory-bound/compute-bound rows, BitsAndBytesConfig argument names, vLLM auto-detect claim.
Method: documentation only; no commands were run.
