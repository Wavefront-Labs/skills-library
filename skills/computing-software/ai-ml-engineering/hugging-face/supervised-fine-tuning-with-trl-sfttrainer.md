---
id: computing-software.ai-ml-engineering.hugging-face.supervised-fine-tuning-with-trl-sfttrainer
name: supervised-fine-tuning-with-trl-sfttrainer
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, peft, supervised-fine-tuning, sfttrainer, trl, instruction-tuning, packing, assistant-only-loss]
level: practitioner
status: verified
description: "Instruction-tune an LLM with TRL SFTTrainer: conversational dataset format, SFTConfig (max_length, packing, assistant-only loss), LoRA, and checking the formatted data."
sources:
  - https://huggingface.co/docs/trl/sft_trainer
  - https://huggingface.co/learn/llm-course/chapter11/3
  - https://huggingface.co/docs/trl/dataset_formats
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Supervised fine-tuning with TRL SFTTrainer

**Goal:** turn a base or instruct model into one that follows your task format, with the right loss masking and efficient batching.

## Data format
Conversational (preferred):
```json
{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
```
Also accepted: `{"prompt": ..., "completion": ...}` and plain `{"text": ...}`. With `messages`, the tokenizer's chat template is applied automatically.

## Train
```python
from trl import SFTTrainer, SFTConfig
from peft import LoraConfig
cfg = SFTConfig(
    output_dir="sft-out",
    max_length=2048,                  # TRL 1.16 rejects the older max_seq_length (TypeError)
    packing=False,                    # True = concatenate short examples into full sequences
    assistant_only_loss=True,         # loss only on assistant turns (template must support it)
    per_device_train_batch_size=4, gradient_accumulation_steps=8,
    learning_rate=2e-4,               # LoRA; full fine-tune ~1e-5 to 2e-5
    num_train_epochs=2, lr_scheduler_type="cosine", warmup_steps=0.03,   # float < 1 = fraction of steps; warmup_ratio is rejected on transformers 5.x
    bf16=True, gradient_checkpointing=True, logging_steps=10,
    eval_strategy="steps", eval_steps=200,
)
trainer = SFTTrainer(model="Qwen/Qwen2.5-1.5B", args=cfg, train_dataset=train, eval_dataset=val,
                     peft_config=LoraConfig(r=16, lora_alpha=32, target_modules="all-linear", task_type="CAUSAL_LM"))
trainer.train()
```
Checked by running the same API on CPU with a tiny Llama (TRL 1.16.0, transformers 5.20.2): `SFTTrainer(model="<hub id>", ...)` accepts a model id string, `peft_config` with `target_modules="all-linear"` trains, and `warmup_ratio`/`max_seq_length` raise `TypeError`. `SFTConfig` accepted `bf16=True` and `gradient_checkpointing=True` (training with them needs suitable hardware), and `Qwen/Qwen2.5-1.5B` exists on the Hub (`model_info`). TRL argument names change between releases; check the installed version's `SFTConfig` docs.

## Decisions that matter
- **Loss masking:** training on prompt tokens wastes capacity and can teach the model to generate user turns. Defaults, observed by decoding `labels`: prompt-completion rows mask the prompt with -100 automatically; `messages` and `text` rows train on every token unless you set `assistant_only_loss=True`. That option needs a chat template with `{% generation %}...{% endgeneration %}` markers; without them SFTTrainer raises "The chat template is not training-compatible". With markers it masks everything except the assistant text (and warns if the end-of-turn token falls outside the marked span, so the model may not learn to stop).
- **Packing** speeds training a lot on short examples; use it with attention implementations that respect example boundaries to avoid cross-contamination between packed examples. The default `packing_strategy="bfd"` enables padding-free mode itself and adds a `seq_lengths` column (observed), but `padding_free` per the `SFTConfig` docs is only supported with FlashAttention 2 or 3.
- **Epochs:** 1-3 on small high-quality data; more overfits and degrades general ability.
- **Base vs instruct start:** starting from the instruct model needs less data but inherits its style; base needs a chat template you define.

## Inspect before training
Decode one batch: `tok.decode(trainer.train_dataset[0]["input_ids"])`, and check which tokens have labels != -100. Most SFT bugs (wrong template, double BOS, all tokens masked) are visible here.

## Verify
- [ ] Decoded training example shows the intended template; only assistant tokens contribute to loss.
- [ ] Eval loss and a small generation eval set tracked per checkpoint.
- [ ] Held-out general benchmark checked for regressions (catastrophic forgetting).
