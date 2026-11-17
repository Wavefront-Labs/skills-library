---
id: computing-software.ai-ml-engineering.hugging-face.preference-tuning-with-dpo
name: preference-tuning-with-dpo
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, peft, dpo, preference-optimization, dpotrainer, trl, rlhf, chosen-rejected]
level: practitioner
status: verified
description: "Align an SFT model with Direct Preference Optimization in TRL: chosen/rejected data, DPOConfig beta and learning rate, reference model with PEFT, and reading reward metrics."
sources:
  - https://arxiv.org/abs/2305.18290
  - https://huggingface.co/docs/trl/dpo_trainer
  - https://huggingface.co/learn/llm-course/chapter11/4
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Preference tuning with DPO

**Goal:** make a model prefer the responses people (or a judge) rated better, without training a separate reward model and running PPO.

## Data
Each row: a prompt plus a preferred and a dispreferred response:
```json
{"prompt": [{"role": "user", "content": "Explain DNS briefly"}],
 "chosen": [{"role": "assistant", "content": "DNS maps names to IPs..."}],
 "rejected": [{"role": "assistant", "content": "DNS is a protocol that..." }]}
```
Sources: human comparisons, LLM-as-judge rankings of samples from your SFT model, or edits (original = rejected, edited = chosen). Pairs from your own model's outputs (on-policy) work better than pairs written by other models.

## Train
```python
from trl import DPOTrainer, DPOConfig
cfg = DPOConfig(output_dir="dpo-out", beta=0.1, learning_rate=5e-7,   # full FT; LoRA ~5e-6 to 5e-5
                per_device_train_batch_size=2, gradient_accumulation_steps=16,
                num_train_epochs=1, bf16=True, max_length=2048,   # max_prompt_length no longer exists (TypeError in TRL 1.16)
                logging_steps=10, eval_strategy="steps", eval_steps=100)
trainer = DPOTrainer(model=sft_model, ref_model=None, args=cfg,
                     train_dataset=train, eval_dataset=val, processing_class=tok,
                     peft_config=lora_cfg)
trainer.train()
```
- Start from an SFT model; DPO on a raw base model works poorly.
- `ref_model=None` with PEFT: the reference is the base model with adapters disabled - saves a full model copy in memory (checked: `trainer.ref_model is None`). Without PEFT, a frozen copy of the starting model is created (checked: `LlamaForCausalLM`). `ref_model_init_kwargs` is not a `DPOConfig` field in TRL 1.16.
- `beta` controls how far the policy may move from the reference (smaller = more deviation). 0.1 is a common start; try 0.05-0.5.

## Reading metrics
- `rewards/chosen`, `rewards/rejected`: implicit rewards (beta x log-ratio vs reference). Logged keys on a 3-step CPU run: `rewards/chosen`, `rewards/rejected`, `rewards/accuracies`, `rewards/margins`, `logps/chosen`, `logps/rejected` (loss 0.6931 = ln 2 at step 0, as expected when policy equals reference).
- `rewards/margins` should grow; `rewards/accuracies` (fraction where chosen > rejected) should rise well above 0.5.
- Watch for both chosen and rejected log-probs falling sharply: the model is "winning" by making everything less likely, which often harms generation quality. Lower LR, fewer steps, or add an SFT term: `rpo_alpha` was removed from `DPOConfig` in TRL 1.16; use `loss_type=["sigmoid", "sft"]` with `loss_weights=[1.0, 0.5]` (ran).

## Alternatives in TRL
ORPO (no reference model, SFT + preference in one stage; now under `trl.experimental`), KTO (unpaired good/bad labels; `trl.KTOTrainer`), online methods with a judge or reward model (`OnlineDPOTrainer` is under `trl.experimental`; `PPOTrainer` is gone from TRL 1.16, `RLOOTrainer` and `GRPOTrainer` remain).

## Verify
- [ ] Preference accuracy on held-out pairs improved.
- [ ] Win rate vs the SFT model on an eval prompt set (human or judge) improved.
- [ ] Length change checked - DPO often makes answers longer; control for length in judging.
