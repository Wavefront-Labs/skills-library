---
id: computing-software.ai-ml-engineering.hugging-face.efficient-single-gpu-fine-tuning-unsloth-liger
name: efficient-single-gpu-fine-tuning-unsloth-liger
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, unsloth, liger-kernel, qlora, single-gpu, memory-efficient-training, trl]
level: practitioner
status: docs-checked
description: "Fine-tune LLMs on one GPU with Unsloth FastLanguageModel (4-bit, LoRA, GGUF export) and Liger kernels, with TRL SFT loss-masking and memory options."
sources:
  - https://raw.githubusercontent.com/unslothai/unsloth/main/README.md
  - https://raw.githubusercontent.com/unslothai/unsloth/main/unsloth/models/loader.py
  - https://raw.githubusercontent.com/unslothai/unsloth/main/unsloth/models/llama.py
  - https://raw.githubusercontent.com/unslothai/unsloth/main/unsloth/save.py
  - https://raw.githubusercontent.com/linkedin/Liger-Kernel/main/README.md
  - https://raw.githubusercontent.com/huggingface/trl/main/docs/source/sft_trainer.md
  - https://raw.githubusercontent.com/huggingface/trl/main/docs/source/reducing_memory_usage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Single-GPU efficient LLM fine-tuning (Unsloth / Liger)

## Unsloth
The Unsloth README claims faster fine-tuning with substantially less VRAM and no accuracy loss, and lists GGUF export among its deployment formats. Check its benchmark table for your model before relying on a speedup.
```python
from unsloth import FastLanguageModel
model, tok = FastLanguageModel.from_pretrained(
    "<model id or unsloth 4-bit repo>", max_seq_length=4096, load_in_4bit=True, dtype=None)
model = FastLanguageModel.get_peft_model(model, r=16, lora_alpha=16, lora_dropout=0,
        use_gradient_checkpointing="unsloth", random_state=3407)
```
- From the source: `from_pretrained` defaults are `max_seq_length=2048`, `dtype=None`, `load_in_4bit=True` (commented "4-bit QLoRA"). `get_peft_model` defaults are `r=16`, `lora_alpha=16`, `lora_dropout=0.0`, `use_gradient_checkpointing="unsloth"`, `random_state=3407`, and a default `target_modules` list that includes `q_proj`. Pass `target_modules` explicitly if you need different layers.
- Train with TRL's `SFTTrainer` and `SFTConfig`.

## TRL SFT settings that matter on one GPU
- `max_length` in `SFTConfig` bounds the sequence length: too small discards tokens, too large can cause out-of-memory errors and, without packing or padding-free batching, wasteful padding.
- `packing=True` packs several examples into one sequence; `packing_strategy="bfd"` (default) discards overflow tokens beyond `max_length`, `"bfd_split"` splits long sequences to keep all tokens.
- `padding_free=True` flattens a batch into one sequence without padding (the docs example sets a FlashAttention-2 `attn_implementation` through `model_init_kwargs`).
- Gradient checkpointing is enabled by default in TRL trainers; set `gradient_checkpointing=False` to disable it.
- Loss masking: for conversational datasets `assistant_only_loss=True` computes loss only on assistant messages; for prompt-completion datasets loss is on completion tokens by default (`completion_only_loss=True` by default there; `False` trains on the full sequence).

## Export
Unsloth's save helpers (source: `save.py`): `save_pretrained_merged(..., save_method=...)` with `"lora"` (adapter only), `"merged_16bit"` or `"merged_4bit"`; `save_pretrained_gguf` for GGUF, whose quantization methods include `q4_k_m` (described in source as the recommended one). Under tensor parallel the source warns that `merged_4bit` merges LoRA into the 4-bit base and recommends `merged_16bit`.

## Liger kernels
LinkedIn's Liger Kernel provides Triton kernels for LLM training: RMSNorm, RoPE, SwiGLU, CrossEntropy and fused linear cross entropy, using kernel fusion, in-place replacement and chunking. It requires only Torch and Triton and works with multi-GPU setups (PyTorch FSDP, DeepSpeed, DDP). The README lists integrations with Axolotl, LLaMA-Factory, TRL's `SFTTrainer`, the Hugging Face Trainer, SWIFT and oumi.
```python
from liger_kernel.transformers import AutoLigerKernelForCausalLM
model = AutoLigerKernelForCausalLM.from_pretrained("path/to/some/model")   # patches if the model type is supported
```
Alternatively call a model-specific patch such as `apply_liger_kernel_to_llama` before creating the model; the README's table lists the patch function and kernels per architecture.

## Choosing
| Need | Pick |
|---|---|
| One GPU, 4-bit LoRA on a model Unsloth supports | Unsloth |
| Any supported HF model, multi-GPU (FSDP, DeepSpeed, DDP) | Liger patches |
| Unsupported architecture | plain PEFT + bitsandbytes + TRL memory options |

## Verify
- [ ] Loss curve over a few hundred steps compared with an unpatched run.
- [ ] Exported model evaluated with the same chat template used in training.
- [ ] Versions pinned; Unsloth and Liger both patch transformers, so re-test after upgrades.

## Checked
Date: 2026-11-09.
- Confirmed in the Unsloth README and source, the Liger README, and TRL SFT and memory docs: API defaults, save methods, gguf quant name, Liger kernels, requirements, multi-GPU support, TRL packing/padding-free/loss-masking/checkpointing settings.
- Removed as unconfirmed: the "~2x faster" figure (percentage and speed figures are not kept), model family support list, the specific Qwen model id, the full target_modules list, `optim="adamw_8bit"`, `bf16`, batch-size values, `use_liger_kernel=True` in TrainingArguments (TRL's Liger integration page returned 404), the "fused linear cross entropy avoids materialising full-vocabulary logits" explanation, the claim that Unsloth is single-GPU only, the "offloads activations" description of gradient checkpointing "unsloth", and the "import unsloth before trl" ordering comment, and the docs.unsloth.ai and TRL liger page sources.
Method: documentation and source files only; no commands were run.
