---
id: computing-software.ai-ml-engineering.hugging-face.evaluating-llms-with-lm-eval-harness-and-lighteval
name: evaluating-llms-with-lm-eval-harness-and-lighteval
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, peft, lm-eval-harness, lighteval, llm-benchmarks, few-shot-evaluation, model-evaluation]
level: practitioner
status: docs-checked
description: "Benchmark base and fine-tuned LLMs with lm-evaluation-harness or lighteval: task selection, chat templates, few-shot settings, vLLM backend, logging samples and fair comparisons."
sources:
  - https://github.com/EleutherAI/lm-evaluation-harness
  - https://huggingface.co/docs/lighteval/index
  - https://huggingface.co/learn/llm-course/chapter11/6
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Evaluating LLMs with lm-eval-harness and lighteval

**Goal:** measure whether fine-tuning improved the target capability without breaking general ones, with numbers comparable across runs.

## lm-evaluation-harness
```bash
pip install "lm_eval[vllm]"
lm_eval --model hf \
  --model_args pretrained=./sft-merged \
  --tasks mmlu,hellaswag,gsm8k,ifeval \
  --batch_size auto \
  --output_path results/sft --log_samples
# faster with vLLM:
lm_eval --model vllm --model_args pretrained=./sft-merged,tensor_parallel_size=1,gpu_memory_utilization=0.85 --tasks gsm8k
```
- Chat/instruct models: add `--apply_chat_template` (it auto-enables `--fewshot_as_multiturn`, which can be set to `false`).
- `--num_fewshot` sets the number of few-shot examples; keep it fixed across compared models.
- `--log_samples` (requires `--output_path`) saves all model inputs and outputs: read some before trusting a score.
- Custom tasks: external task YAML files in a directory passed with `--include_path`.

## lighteval
Hugging Face's LLM evaluation library (see the lighteval docs for its CLI and task syntax). Choose one harness per project; scores for the "same" benchmark differ between harnesses because prompts and answer extraction differ.

## Fair comparison rules
- Same harness version, task versions, few-shot count, chat-template setting, max generation length and dtype across all models.
- Evaluate base, SFT and final models in the same run.
- Report uncertainty (standard error) with each score, not just the point estimate.
- Public benchmarks may be contaminated in your fine-tuning data; check overlap, and rely on a private task-specific eval set for decisions.

## What to run
- Target capability: your own eval set (exact-match, judge-based, or task metric).
- Regression checks: a few broad benchmarks (MMLU-style knowledge, instruction following like IFEval, math/code if relevant).

## Verify
- [ ] All compared models evaluated with identical settings (saved config in `results/`).
- [ ] Sampled outputs reviewed for extraction/formatting failures.
- [ ] Decision based on private task eval + regression benchmarks with uncertainty reported.

## Checked
Date: 2026-10-28.
- Confirmed in the lm-evaluation-harness README and docs/interface.md: `lm_eval[vllm]`, `--model hf|vllm`, `--batch_size auto`, `tensor_parallel_size`, `gpu_memory_utilization`, `--apply_chat_template`, `--fewshot_as_multiturn` (auto-enabled with the chat template), `--num_fewshot`, `--output_path` (required with `--log_samples`), `--include_path`, ifeval task.
- Removed as unconfirmed: `dtype=bfloat16`, `--device`, the `peft=` adapter example, lighteval task-spec format and leaderboard claim, stderr printing, GSM8K extraction remark.
Method: documentation only; no commands were run.
