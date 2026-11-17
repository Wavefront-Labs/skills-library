---
id: computing-software.ai-ml-engineering.llm-application-engineering.hosted-fine-tuning-apis
name: hosted-fine-tuning-apis
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, fine-tuning-vs-prompting, hosted-fine-tuning, sft-data-format, fine-tuning-evaluation, model-customization]
level: practitioner
status: draft
description: "Decide when to fine-tune a hosted LLM and do it well: data format and size, validation splits, supervised vs preference methods, prompted baselines and lifecycle."
sources:
  - https://platform.openai.com/docs/guides/fine-tuning
  - https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html
  - https://cloud.google.com/vertex-ai/generative-ai/docs/models/tune-models
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hosted fine-tuning APIs

**Goal:** use provider fine-tuning only when it beats good prompting, and run it with proper data and evaluation.

## Fine-tune or prompt?
Try first: a better prompt, few-shot examples, retrieval, structured outputs, a larger model. Fine-tuning helps for: consistent style/format at scale, a narrow task where a smaller fine-tuned model matches a larger prompted one (cost/latency), and behaviours hard to describe but easy to demonstrate. It is poor at adding new factual knowledge - use retrieval for that.

## Data
OpenAI-style chat JSONL (other providers are similar):
```json
{"messages": [{"role": "system", "content": "You are..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "ideal answer"}]}
```
- Quality over quantity: start with ~50-200 excellent, diverse examples; scale to thousands if evals keep improving.
- Examples must look like production inputs (same system prompt, same input distribution, including hard and edge cases).
- Hold out a validation file; keep your eval set separate from both.
- Check for PII, licensing and duplicates before uploading.

## Run
```python
f = client.files.create(file=open("train.jsonl", "rb"), purpose="fine-tune")
v = client.files.create(file=open("val.jsonl", "rb"), purpose="fine-tune")
job = client.fine_tuning.jobs.create(model=BASE_MODEL, training_file=f.id, validation_file=v.id)
```
Methods vary by provider: supervised fine-tuning, preference fine-tuning (DPO), and reinforcement fine-tuning with graders. Watch training/validation loss in job events; use checkpoints if later epochs overfit.

Other platforms: Amazon Bedrock custom models (fine-tuning and continued pre-training for supported models), Vertex AI supervised tuning for Gemini models, and open-weight models via your own training (TRL/PEFT).

## Evaluate
Compare fine-tuned model vs the best prompted baseline (same eval set, same graders) on quality, cost per request and latency. Also run regression checks on general behaviours (safety refusals, instruction following) that fine-tuning can erode.

## Lifecycle
Fine-tuned models are tied to a base model version; when the base is deprecated you must retrain. Keep the dataset, config and eval results versioned so retraining is a pipeline, not a project.

## Verify
- [ ] Prompted baseline measured before fine-tuning.
- [ ] Fine-tuned model beats it on the eval set at acceptable cost.
- [ ] Training data, job config and eval results stored for retraining.
