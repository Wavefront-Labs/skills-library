---
id: computing-software.ai-ml-engineering.vllm.int4-w4a16-llm-compressor
name: int4-w4a16-llm-compressor
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [int4, w4a16, gptq, llm-compressor, dampening-frac]
level: practitioner
status: docs-checked
description: "Quantize weights to INT4 (W4A16, GPTQ) with calibration data and tune dampening_frac and actorder."
sources:
  - https://docs.vllm.ai/en/latest/features/quantization/llm_compressor/int4/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: shrink a model with 4-bit integer weights, useful for low-QPS, latency-sensitive workloads.

Requires NVIDIA compute capability above 8.0 (Ampere, Ada, Hopper, Blackwell). Install `llmcompressor` in a separate environment from vLLM.

Four steps: load the model with transformers AutoModel classes, prepare calibration data, apply quantization, evaluate in vLLM.

Calibration: weights need sample data to estimate weight updates and scales. The example uses `HuggingFaceH4/ultrachat_200k` with `NUM_CALIBRATION_SAMPLES = 512` and `MAX_SEQUENCE_LENGTH = 2048`, applying the chat template.

Apply with `GPTQModifier` and `oneshot(model=model, dataset=ds, recipe=recipe, max_seq_length=..., num_calibration_samples=...)`, then `model.save_pretrained(SAVE_DIR, save_compressed=True)`. Load with `LLM("./Meta-Llama-3-8B-Instruct-W4A16-G128")`; evaluate with `lm_eval` and `add_bos_token=True`.

Best practices from the page:
- Start with 512 samples; raise them if accuracy drops.
- Use varied data to avoid overfitting; start at sequence length 2048.
- Use the model's trained chat or instruction template.
- For a fine-tuned model, sample your training data.
- `dampening_frac` sets GPTQ influence; lower can improve accuracy but may cause numerical instability and failure.
- `actorder="weight"` can improve accuracy without added latency.

Expanded recipe: `QuantizationArgs(num_bits=4, type=INT, strategy=GROUP, group_size=128, symmetric=True, dynamic=False, actorder="weight")`, `ignore=["lm_head"]`, `dampening_frac=0.01`.

## Checked

Method: 2026-11-08 read the INT4 W4A16 page in full. Hardware note, four-step flow, calibration settings, best practices and expanded recipe all matched; unchanged.
