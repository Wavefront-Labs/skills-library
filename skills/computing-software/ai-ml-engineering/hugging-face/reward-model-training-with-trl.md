---
id: computing-software.ai-ml-engineering.hugging-face.reward-model-training-with-trl
name: reward-model-training-with-trl
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, reward-model, rewardtrainer, trl, rlhf, preference-data, bradley-terry]
level: practitioner
status: verified
description: "Train a reward model with TRL RewardTrainer on chosen/rejected preference pairs: data format, sequence-classification head, margin and center_rewards, evaluation and use in RL."
sources:
  - https://huggingface.co/docs/trl/reward_trainer
  - https://huggingface.co/docs/trl/dataset_formats#preference
  - https://arxiv.org/abs/2203.02155
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Reward model training with RewardTrainer

A reward model scores a (prompt, response) pair. It is trained on human or AI preference pairs with a Bradley-Terry loss: `-log sigmoid(r_chosen - r_rejected)`.

## Data
Preference format, conversational or plain text:
```python
{"chosen":   [{"role": "user", "content": "Q"}, {"role": "assistant", "content": "good answer"}],
 "rejected": [{"role": "user", "content": "Q"}, {"role": "assistant", "content": "bad answer"}]}
# or {"prompt": ..., "chosen": ..., "rejected": ...}
```
Public examples: `trl-lib/ultrafeedback_binarized`, `Anthropic/hh-rlhf`.

## Train
```python
from trl import RewardTrainer, RewardConfig
from transformers import AutoModelForSequenceClassification, AutoTokenizer
tok = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
model = AutoModelForSequenceClassification.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct", num_labels=1)
model.config.pad_token_id = tok.pad_token_id
args = RewardConfig(output_dir="rm", per_device_train_batch_size=8, num_train_epochs=1,
                    learning_rate=1e-5, max_length=1024, center_rewards_coefficient=0.01, bf16=True)
trainer = RewardTrainer(model=model, args=args, processing_class=tok,
                        train_dataset=ds["train"], eval_dataset=ds["test"])
trainer.train()
```
- `num_labels=1`: a scalar head on the last token. The pad token must be set, because the score is read at the last non-pad position. `RewardTrainer` falls back to `eos_token` when `processing_class.pad_token` is missing (TRL source).
- Optional `margin` dataset column (not a `RewardConfig` field: `RewardConfig(margin=...)` raises `TypeError`) adds a per-pair margin to the loss, as in Llama 2; `DataCollatorForPreference` turns it into a tensor.
- `center_rewards_coefficient` keeps rewards near zero mean, which helps downstream RL stability.
- LoRA: pass `peft_config=LoraConfig(task_type="SEQ_CLS", ...)`; the score head must stay trainable; with `task_type="SEQ_CLS"` PEFT already wraps it (checked: only `score.modules_to_save.default.weight` was trainable among score parameters), so an explicit `modules_to_save` is unnecessary.

## Evaluate
- Preference accuracy on held-out pairs (RewardTrainer logs `accuracy`, `margin`, `min_reward`, `mean_reward`, `max_reward`, and `eval_` versions). Compare with inter-annotator agreement; no authoritative "typical" accuracy figure was checked, so do not rely on one.
- Check reward distributions by length: a reward that mostly tracks response length will be exploited by the policy. Correlate rewards with length; consider length-controlled data.
- RewardBench for standard comparisons.

## Using it
- RLOO and GRPO in TRL take a reward model (or functions); `PPOTrainer` no longer exists in TRL 1.16 and `OnlineDPOTrainer` is under `trl.experimental`.
- Score with `model(**tok(prompt_and_response, return_tensors="pt")).logits[0, 0]` (logits shape is `[batch, 1]`, checked), using the same chat template as training.

## Pitfalls
- Truncation: if chosen and rejected differ only after `max_length`, the pair is noise. Filter long examples or raise max_length.
- Overfitting quickly: one epoch is usually enough; watch eval accuracy.
