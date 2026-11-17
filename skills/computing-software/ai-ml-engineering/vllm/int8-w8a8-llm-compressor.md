---
id: computing-software.ai-ml-engineering.vllm.int8-w8a8-llm-compressor
name: int8-w8a8-llm-compressor
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [int8, w8a8, smoothquant, llm-compressor, blackwell-limitation]
level: practitioner
status: docs-checked
description: "Quantize weights and activations to INT8 with SmoothQuant plus GPTQ, and avoid the Blackwell limitation."
sources:
  - https://docs.vllm.ai/en/latest/features/quantization/llm_compressor/int8_w8a8/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: INT8 weights and activations for memory savings and acceleration.

Support: NVIDIA compute capability above 7.5 (Turing, Ampere, Ada, Hopper). Warning: INT8 is not supported on compute capability 10.0 or higher (for example RTX 6000 Blackwell); use FP8 quantization instead, or run on Hopper, Ada or Ampere.

Prerequisites: `pip install llmcompressor` in its own environment, and `pip install vllm "lm-eval[api]>=0.4.12"` for evaluation, since the two may not work together.

Steps: load the model (transformers AutoModel classes), prepare calibration data (activation scales need samples; the example uses `ultrachat` with 512 samples and max length 2048), apply quantization, evaluate in vLLM.

The recipe chains two modifiers:

```python
recipe = [
    SmoothQuantModifier(smoothing_strength=0.8),
    GPTQModifier(targets="Linear", scheme="W8A8", ignore=["lm_head"]),
]
oneshot(model=model, dataset=ds, recipe=recipe,
        max_seq_length=2048, num_calibration_samples=512)
```

Save the result as `Meta-Llama-3-8B-Instruct-W8A8-Dynamic-Per-Token` with `save_pretrained(SAVE_DIR, save_compressed=True)`, load it with `LLM("./Meta-Llama-3-8B-Instruct-W8A8-Dynamic-Per-Token")`, then evaluate with `lm_eval` and `add_bos_token=True`.

Best practices: start with 512 calibration samples (increase if accuracy drops), sequence length 2048, use the chat or instruction template the model was trained with, and for fine-tuned models calibrate on a sample of training data.

## Checked

Method: 2026-11-08 read the INT8 W8A8 page in full. Hardware note, Blackwell warning, prerequisites, SmoothQuant plus GPTQ recipe and best practices matched; fixed one garbled sentence about the saved model name, no claims changed.
