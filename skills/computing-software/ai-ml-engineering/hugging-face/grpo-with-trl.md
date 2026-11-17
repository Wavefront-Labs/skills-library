---
id: computing-software.ai-ml-engineering.hugging-face.grpo-with-trl
name: grpo-with-trl
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, grpo, trl, reinforcement-learning, verifiable-rewards, reward-functions, vllm]
level: practitioner
status: gated
description: "Train reasoning or task skills with TRL GRPOTrainer: dataset prompts, reward functions with verifiable checks, num_generations, KL beta, vLLM generation and reward hacking checks."
sources:
  - https://huggingface.co/docs/trl/main/en/grpo_trainer
  - https://huggingface.co/learn/llm-course/chapter12/1
  - https://arxiv.org/abs/2402.03300
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GRPO with TRL (RL from verifiable rewards)

**Idea:** sample a group of completions per prompt, score each with reward functions, and push the policy toward completions that beat the group average. No value model and no separate reward model needed when rewards are programmatic (math answer correct, unit tests pass, format valid).

## Minimal setup
```python
from trl import GRPOConfig, GRPOTrainer
import re

def correctness(completions, answer, **kwargs):       # dataset column "answer" is passed by name
    texts = [c[0]["content"] if isinstance(c, list) else c for c in completions]
    preds = [re.search(r"<answer>(.*?)</answer>", t, re.S) for t in texts]
    return [1.0 if p and p.group(1).strip() == a.strip() else 0.0 for p, a in zip(preds, answer)]

def format_ok(completions, **kwargs):
    texts = [c[0]["content"] if isinstance(c, list) else c for c in completions]
    return [0.2 if re.search(r"<think>.*</think>\s*<answer>.*</answer>", t, re.S) else 0.0 for t in texts]

cfg = GRPOConfig(output_dir="grpo", learning_rate=1e-6, per_device_train_batch_size=8,
                 num_generations=8, max_completion_length=1024, beta=0.0,
                 temperature=1.0, use_vllm=True, bf16=True, logging_steps=5)
trainer = GRPOTrainer(model="Qwen/Qwen2.5-1.5B-Instruct", reward_funcs=[correctness, format_ok],
                      args=cfg, train_dataset=ds)      # ds needs a "prompt" column
trainer.train()
```

## Key settings
- `num_generations` (group size, default 8; 4-16 is a common range): bigger = better advantage estimates, more compute. `generation_batch_size` must be divisible by it (`ValueError: generation_batch_size (3) must be divisible by num_generations (4)`, ran).
- `beta`: KL penalty to the reference model; the TRL 1.16 default is already 0.0 (no reference model, less memory), so set it above 0 explicitly if you want a KL term, and watch for drift.
- `use_vllm=True` makes generation fast (colocated or a separate vLLM server via `trl vllm-serve --model <id>`; the subcommand exists, but vLLM itself was not run here: no GPU or Linux host) (gated: unconfirmed, source is paywalled or blocked).
- LoRA via `peft_config=` reduces memory.

## Monitoring
Log reward mean/std per function (TRL logs `rewards/<function_name>/mean` and `/std`), completion length (`completions/mean_length`, `completions/clipped_ratio`), KL, and fraction of groups with zero reward variance (`frac_reward_zero_std`, which was 1.0 in a CPU run where nothing was rewarded) (no learning signal: prompts too hard or too easy). Curate prompts to a difficulty where the base model sometimes succeeds.

## Reward hacking
Inspect samples regularly: models exploit loose regexes, emit the answer tag multiple times, or pad length. Tighten checks, cap length, and evaluate on a held-out set with a strict grader.

## Verify
- [ ] Held-out accuracy improves over the starting checkpoint; general benchmarks not degraded.
