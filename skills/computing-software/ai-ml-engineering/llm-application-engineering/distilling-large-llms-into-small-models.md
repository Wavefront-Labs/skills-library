---
id: computing-software.ai-ml-engineering.llm-application-engineering.distilling-large-llms-into-small-models
name: distilling-large-llms-into-small-models
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, fine-tuning-vs-prompting, model-distillation, knowledge-distillation, teacher-student, synthetic-labels]
level: practitioner
status: draft
description: "Distill a large LLM's behaviour on your task into a smaller model: teacher output collection on real inputs, filtering, student fine-tuning, evaluation and teacher fallback."
sources:
  - https://arxiv.org/abs/1503.02531
  - https://arxiv.org/abs/2305.02301
  - https://platform.openai.com/docs/guides/distillation
  - https://huggingface.co/docs/trl/sft_trainer
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Distilling a large LLM into a small model

**Goal:** match a large model's quality on one task with a much cheaper/faster small model.

## Recipe
1. **Inputs:** collect a large, representative set of real task inputs (production logs, scrubbed) - thousands to tens of thousands. Coverage of the input distribution matters more than volume.
2. **Teacher outputs:** run the large model with the best prompt (and reasoning enabled if it helps). For classification/extraction, ask for structured outputs; for generation, the final answer (optionally with rationales - "distilling step-by-step" showed rationales can improve small-model learning, Hsieh et al. 2023).
3. **Filter:** keep only outputs that pass validators (schema, business rules) and, where possible, a judge or agreement check (sample the teacher several times; keep consistent answers). Bad teacher outputs teach bad behaviour.
4. **Train the student:** hosted fine-tuning of a small model, or SFT/LoRA of an open-weight model.
5. **Evaluate** on a human-labelled eval set (not teacher labels): student vs teacher vs small-model-prompted baseline.
6. **Deploy with fallback:** route low-confidence or out-of-distribution inputs to the teacher.

## Practical points
- Keep the eval set disjoint from distillation inputs (dedupe near-duplicates).
- Check provider terms: some prohibit using outputs to train models that compete with the provider; distilling for your own narrow task is a common allowed case but verify for your provider and model.
- Retrain periodically: the student doesn't improve when the teacher does, and inputs drift.
- Classical alternative for classification: distil into a non-LLM model (fine-tuned encoder, logistic regression on embeddings) - even cheaper.

## Verify
- [ ] Student quality measured on human-labelled data within an agreed margin of the teacher.
- [ ] Cost and latency savings quantified at production volume.
- [ ] Fallback routing and its rate monitored.
