---
id: computing-software.ai-ml-engineering.llm-application-engineering.reinforcement-fine-tuning-with-graders
name: reinforcement-fine-tuning-with-graders
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, reinforcement-fine-tuning, graders, grpo, rlvr, model-customization]
level: practitioner
status: draft
description: "Improve reasoning models on verifiable tasks with reinforcement fine-tuning: grader design, hosted RFT jobs, TRL GRPO with reward functions, reward hacking checks and evals."
sources:
  - https://platform.openai.com/docs/guides/reinforcement-fine-tuning
  - https://platform.openai.com/docs/guides/graders
  - https://huggingface.co/docs/trl/main/en/grpo_trainer
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Reinforcement fine-tuning with graders

**Goal:** a model gets better at a task with checkable answers (classification with rationale, extraction, code, maths, policy decisions) using a grader as the training signal, with tens to hundreds of examples rather than thousands of demonstrations.

## When RFT fits
- Correctness can be scored automatically or by a reliable model grader.
- Prompting and supervised fine-tuning plateaued; the model sometimes gets it right (RL amplifies existing ability, it rarely creates new ones).
- You have a held-out set to prove improvement.
Not for style or tone (use SFT/preference tuning) or for adding knowledge (use retrieval).

## Grader design
Graders return a score in [0, 1]:
- **String check:** exact or case-insensitive match on a field.
- **Text similarity:** fuzzy/BLEU-style for near matches.
- **Python grader:** arbitrary code (parse JSON, partial credit per field, run unit tests).
- **Model grader:** an LLM scores against a rubric - calibrate against human labels first.
- **Multi-grader:** weighted combination (e.g. 0.7 correctness + 0.3 format).
Give partial credit where meaningful; a binary reward on hard tasks gives little signal.

## Hosted RFT (OpenAI-style)
Fine-tuning job with `method: {"type": "reinforcement", "reinforcement": {"grader": {...}, "hyperparameters": {...}}}` on a supported reasoning model, with training and validation JSONL where each item has the prompt plus reference fields the grader reads. Watch validation reward and sampled outputs during training.

## Open-weight models with TRL GRPO
```python
from trl import GRPOConfig, GRPOTrainer
def correct(completions, answer, **kw):
    return [1.0 if extract(c) == a else 0.0 for c, a in zip(completions, answer)]
def formatted(completions, **kw):
    return [0.2 if is_valid_json(c) else 0.0 for c in completions]
trainer = GRPOTrainer(model="Qwen/Qwen2.5-7B-Instruct", reward_funcs=[correct, formatted],
                      args=GRPOConfig(output_dir="grpo", num_generations=8, max_completion_length=512,
                                      learning_rate=1e-6, use_vllm=True),
                      train_dataset=ds)        # columns: prompt, answer
trainer.train()
```
GRPO samples several completions per prompt and pushes toward those with above-group-average reward; vLLM generation makes it practical.

## Reward hacking
Models exploit grader loopholes (always outputting the most common label, gaming a model grader with confident language, tests that do not check edge cases). Inspect samples every checkpoint, keep a separate evaluation grader or human review, and add penalties for discovered exploits.

## Verify
- [ ] Held-out score improves over the base model and over a prompt-optimised baseline.
- [ ] Sampled outputs reviewed for reward hacking.
- [ ] Grader validated against human judgments before training.
