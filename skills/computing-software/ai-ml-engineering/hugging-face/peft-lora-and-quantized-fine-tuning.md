---
id: computing-software.ai-ml-engineering.hugging-face.peft-lora-and-quantized-fine-tuning
name: peft-lora-and-quantized-fine-tuning
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [huggingface, peft, lora, qlora, quantization, bitsandbytes, parameter-efficient-fine-tuning, adapters, rank, target-modules, merge-and-unload, fine-tuning, low-rank-adaptation, 4bit, bf16]
level: advanced
status: gated
description: "Fine-tune large models cheaply with Hugging Face PEFT: LoRA rank/target-module choices, QLoRA 4-bit quantization, adapter merging, and the gotchas that silently degrade quality."
sources:
  - https://huggingface.co/docs/peft/index
  - https://arxiv.org/abs/2106.09685
  - https://arxiv.org/abs/2305.14314
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LoRA / QLoRA fine-tuning with Hugging Face PEFT

**Goal:** fine-tune a model that doesn't fit (or isn't worth fully fine-tuning) on your hardware, without the quality loss or deployment confusion that comes from getting rank, target modules, or merging wrong.

## 1. LoRA basics and the choices that matter
```python
from peft import LoraConfig, get_peft_model
config = LoraConfig(r=16, lora_alpha=32, target_modules=["q_proj","v_proj"],
                     lora_dropout=0.05, bias="none", task_type="CAUSAL_LM")
model = get_peft_model(base_model, config)
model.print_trainable_parameters()   # sanity check: a small fraction of the total (0.198% on a tiny Llama, r=16 on q_proj/v_proj)
```
- **Rank (`r`)**: controls adapter capacity. 8–16 is enough for most style/format/domain-adaptation tasks; go to 32–64 only if the task needs genuinely new capability (a new language, a very different domain) and you've confirmed lower rank underfits. Higher rank costs more memory/compute for diminishing returns past the task's actual complexity — don't default to the largest number "to be safe."
- **`lora_alpha`**: scales the adapter's contribution (effective scale is `alpha/r`: `scaling == {'default': 2.0}` for r=16, alpha=32, ran; `use_rslora=True` changes the formula). A common convention is `alpha = 2*r`, but this is a starting point, not a law — if the fine-tune barely changes behavior, raise alpha before raising rank.
- **`target_modules`**: attention projections (`q_proj`, `v_proj`, sometimes `k_proj`, `o_proj`) are the default and cover most tasks cheaply. Adding MLP/`gate_proj`/`up_proj`/`down_proj` increases trainable parameters and can help on tasks needing more factual/knowledge shift, at higher memory cost — verify with `print_trainable_parameters()` that you know what you added.
- `print_trainable_parameters()` after `get_peft_model` is the single most useful sanity check — if it reports 100% trainable, the base model wasn't frozen (a model loaded without the expected PEFT wrapping, or a custom module PEFT didn't target) and you are accidentally full-fine-tuning, with the resource cost that implies and no corresponding serving convenience.

## 2. QLoRA: fine-tuning a quantized base
```python
from transformers import BitsAndBytesConfig
bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                                 bnb_4bit_compute_dtype=torch.bfloat16,
                                 bnb_4bit_use_double_quant=True)
base_model = AutoModelForCausalLM.from_pretrained(name, quantization_config=bnb_config, device_map="auto")
```
- The base model's weights stay frozen and 4-bit; only the LoRA adapters (added on top, in bf16/fp32) are trained — this is what makes fine-tuning a 7B–70B model feasible on a single consumer/prosumer GPU.
- `bnb_4bit_compute_dtype` is `torch.float32` unless you set it (checked on `BitsAndBytesConfig`; default `bnb_4bit_quant_type` is `fp4`, so `nf4` must be requested). Set bf16 or fp16 explicitly for speed; the speed gap was not measured here (gated: unconfirmed, source is paywalled or blocked).
- Gotcha: gradient checkpointing (`model.gradient_checkpointing_enable()`) is near-mandatory at this scale. Older stacks needed `model.enable_input_require_grads()` with PEFT or gradients did not reach the adapter. On transformers 5.20.2 with PEFT 0.21.2 (tiny Llama, CPU) all adapter tensors received gradients with and without that call, with `use_reentrant` True, False and unset, so keep the call as cheap insurance but do not assume it is your bug; a loss that never moves is more often learning rate, masking or data. (The QLoRA path itself was not run: bitsandbytes is not installed here.) (gated: unconfirmed, source is paywalled or blocked)
- 4-bit quantization is for *training-time memory*, not an automatic win for serving: either keep serving through bitsandbytes/the same quantized path, or merge-and-requantize deliberately (next section) — don't assume the quantized training artifact is the deployment artifact without checking inference-time quantization support for your target runtime.

## 3. Merging and deployment gotchas
- `model.merge_and_unload()` bakes the LoRA delta into the base weights, producing a standalone model with no PEFT dependency at inference (ran: returns `LlamaForCausalLM` with no `lora` parameters) — needed for runtimes that don't support adapter loading (some serving engines) or when you want one self-contained checkpoint.
- Merging from a **4-bit quantized base is lossy**: dequantize to bf16/fp32 first, merge, then requantize for serving if needed — merging directly against 4-bit weights compounds quantization error into the merged result in a way that's easy to miss in a quick eval but shows up as subtly worse generation quality.
- Keep the **unmerged adapter** saved separately even after merging — it's small (9,224 bytes of weights for the tiny model above; a few MB to hundreds of MB for real models depending on rank and targets), lets you A/B multiple adapters on one base model in serving (hot-swap without reloading the base), and lets you re-merge cleanly if you find a merging bug later.
- Catastrophic forgetting check: LoRA is gentler than full fine-tuning but can still degrade general capability if trained too long or at too high an LR on a narrow dataset — eval on a general benchmark (not just the fine-tune's own validation set) before shipping, especially for a chat/assistant model.

## Verify
- [ ] `print_trainable_parameters()` run right after `get_peft_model`; the trainable fraction matches expectations (not 100%, not 0%).
- [ ] If QLoRA: `bnb_4bit_compute_dtype` set explicitly; gradient checkpointing + `enable_input_require_grads()` both on; loss confirmed to actually decrease in the first few hundred steps.
- [ ] Merging done from a dequantized (not raw 4-bit) base when quality matters.
- [ ] Unmerged adapter weights retained separately from the merged artifact.
- [ ] Post-fine-tune eval includes a general-capability check, not only the task-specific validation set.
