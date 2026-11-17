---
id: computing-software.ai-ml-engineering.hugging-face.fp8-and-compressed-tensors-with-llm-compressor
name: fp8-and-compressed-tensors-with-llm-compressor
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, compressed-tensors, llm-compressor, fp8, w4a16, vllm, quantization]
level: practitioner
status: docs-checked
description: "Quantize LLMs for vLLM with llm-compressor into the compressed-tensors format: FP8 dynamic, W8A8 and W4A16 GPTQ recipes, calibration data, saving and accuracy checks."
sources:
  - https://docs.vllm.ai/projects/llm-compressor/en/latest/
  - https://github.com/neuralmagic/compressed-tensors
  - https://docs.vllm.ai/en/latest/features/quantization/fp8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# FP8 and compressed-tensors quantization (llm-compressor)

`llm-compressor` (vLLM project) applies quantization recipes to Hugging Face models and saves them in the **compressed-tensors** format, which vLLM loads natively (and Transformers can read).

## FP8 dynamic (no calibration data)
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from llmcompressor import oneshot
from llmcompressor.modifiers.quantization import QuantizationModifier
mid = "meta-llama/Llama-3.1-8B-Instruct"
model = AutoModelForCausalLM.from_pretrained(mid, torch_dtype="auto"); tok = AutoTokenizer.from_pretrained(mid)
recipe = QuantizationModifier(targets="Linear", scheme="FP8_DYNAMIC", ignore=["lm_head"])
oneshot(model=model, recipe=recipe)
model.save_pretrained("Llama-3.1-8B-Instruct-FP8-Dynamic", save_compressed=True); tok.save_pretrained(...)
```
- `FP8_DYNAMIC` needs no calibration dataset. Check the vLLM quantization docs for which GPUs run FP8 natively.

## W4A16 (GPTQ) and W8A8 with calibration
```python
from llmcompressor.modifiers.gptq import GPTQModifier
from llmcompressor.modifiers.transform.smoothquant import SmoothQuantModifier
recipe = [SmoothQuantModifier(smoothing_strength=0.8),                       # for W8A8 int8
          GPTQModifier(targets="Linear", scheme="W8A8", ignore=["lm_head"])]
# W4A16: GPTQModifier(targets="Linear", scheme="W4A16", ignore=["lm_head"])
oneshot(model=model, dataset=calib_ds, recipe=recipe, max_seq_length=2048, num_calibration_samples=512)
```
- Calibration data: the llm-compressor examples use 512 samples at `max_seq_length=2048`; use samples that resemble your production prompts.
- Pick W4A16 vs W8A8 by measuring on your own workload.

## Serve
```bash
vllm serve ./Llama-3.1-8B-Instruct-FP8-Dynamic --max-model-len 8192
```
The saved directory is a compressed-tensors checkpoint; see the vLLM quantization documentation for serving options.

## Accuracy check
Run the same eval before and after quantization, including task-specific evals (code, long context).

## Gotchas
- Keep `lm_head` unquantized with `ignore=["lm_head"]`, as the llm-compressor examples do.

## Checked

2026-11-02. Checked against the llm-compressor repository examples on main (quantization_w8a8_fp8, quantization_w4a16, quantization_w8a8_int8): oneshot, QuantizationModifier with FP8_DYNAMIC, GPTQModifier W4A16 (group size 128) and W8A8, SmoothQuantModifier(smoothing_strength=0.8), ignore=["lm_head"], max_seq_length and num_calibration_samples, save_pretrained(save_compressed=True). Corrected: SmoothQuantModifier now imports from llmcompressor.modifiers.transform.smoothquant. Removed because no readable source states them (the vLLM docs pages are script shells): hardware-support and size claims, vLLM serving and online-FP8 flags, accuracy figures and lm_eval invocation, MoE router ignore pattern, sequential-onloading note and the KV-cache dtype note, and the ultrachat default dataset claim.

Method: documentation only; no commands were run.
