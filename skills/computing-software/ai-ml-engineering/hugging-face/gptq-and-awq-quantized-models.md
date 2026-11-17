---
id: computing-software.ai-ml-engineering.hugging-face.gptq-and-awq-quantized-models
name: gptq-and-awq-quantized-models
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, quantization, gptq, awq, 4bit, gptqmodel, autoawq, weight-only-quantization]
level: practitioner
status: docs-checked
description: "Use and create GPTQ and AWQ 4-bit models with Transformers: loading pre-quantized checkpoints, calibration settings, kernels, vLLM serving, and comparing against bitsandbytes."
sources:
  - https://huggingface.co/docs/transformers/main/en/quantization/gptq
  - https://huggingface.co/docs/transformers/main/en/quantization/awq
  - https://arxiv.org/abs/2210.17323
  - https://arxiv.org/abs/2306.00978
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPTQ and AWQ quantized models

**Goal:** run LLMs in 4-bit with small accuracy loss and fast inference kernels.

## What they are
- **GPTQ** (Frantar et al.): post-training, weight quantization using approximate second-order information from calibration data.
- **AWQ** (Lin et al.): activation-aware weight quantization - preserves the small fraction of weights that matter most for LLM quality.
Both are used here at 4 bits (the AWQ example config shows `group_size` 128).

## Loading pre-quantized checkpoints
```python
from transformers import AutoModelForCausalLM
m = AutoModelForCausalLM.from_pretrained("org/Model-7B-AWQ", device_map="auto", torch_dtype="auto")
m = AutoModelForCausalLM.from_pretrained("org/Model-7B-GPTQ-Int4", device_map="auto")
```
Backends must be installed (`gptqmodel` for GPTQ, `autoawq` for AWQ; installing autoawq may downgrade Transformers, so reinstall your version afterwards). The quantization config is read from the checkpoint's `config.json`.

## Quantizing yourself (GPTQ via Transformers)
```python
from transformers import GPTQConfig
qcfg = GPTQConfig(bits=4, dataset="c4", tokenizer=tok)
qm = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=qcfg, device_map="auto")
qm.push_to_hub("<user>/model-gptq")  # also saves the GPTQConfig
```
- Calibration data should resemble your use (chat transcripts for a chat model, code for code).

## Serving
vLLM lists AutoAWQ and GPTQModel among its supported quantization methods. Transformers offers a 4-bit GPTQ Marlin kernel (`GPTQConfig(bits=4, backend="marlin")`), optimized for NVIDIA A100 (Ampere); it supports inference only, not quantization.

## vs bitsandbytes
bitsandbytes NF4 quantizes on the fly (no calibration, any model) and is the Transformers docs' pick for QLoRA fine-tuning. TGI's launcher reference says bitsandbytes-nf4 is much slower than native f16 and that AWQ has faster kernels than GPTQ.

## Verify
- [ ] Perplexity and task evals of the quantized model vs fp16 measured (expect small drops; large drops mean bad calibration data or a sensitive model).
- [ ] Tokens/s and memory measured on the serving engine you'll use.
- [ ] Quantization config (bits, group size, act-order) recorded with the model.

## Checked
Date: 2026-10-28.
- Confirmed in the Transformers GPTQ and AWQ pages: `GPTQConfig(bits=4, dataset="c4", tokenizer=...)`, `push_to_hub` saves the config, Marlin backend, gptqmodel and autoawq installs and the autoawq Transformers downgrade, AWQ `group_size` 128 and `bits` 4. vLLM page: AutoAWQ and GPTQModel supported. TGI launcher reference: AWQ vs GPTQ and bitsandbytes-nf4 notes.
- Removed as unconfirmed: ~1% channels, Hessian and layer-by-layer wording, weight-only claim, `desc_act` and `group_size` arguments, sample counts, 70B timing, `vllm serve --quantization awq` command, FP8 on Hopper advice.
Method: documentation only; no commands were run.
