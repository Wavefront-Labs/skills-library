---
id: computing-software.cloud-infrastructure-engineering.aws.bedrock-model-customization-fine-tuning-and-distillation
name: bedrock-model-customization-fine-tuning-and-distillation
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, bedrock, model-customization, fine-tuning, model-distillation, continued-pre-training, provisioned-throughput]
level: practitioner
status: draft
description: "Customise Bedrock models: when to fine-tune vs prompt or RAG, training data formats, customization jobs, distillation from a teacher model, and deploying custom models."
sources: ["Amazon Bedrock User Guide - Customize your model (fine-tuning and continued pre-training)", "Amazon Bedrock User Guide - Model distillation", "Amazon Bedrock User Guide - Prepare training datasets", "Amazon Bedrock User Guide - Use a custom model (Provisioned Throughput and on-demand deployment)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bedrock model customization: fine-tuning and distillation

## Decide first
| Need | Try first |
|---|---|
| Knowledge of your documents | RAG (Knowledge Bases), not fine-tuning |
| Output format/tone | prompt engineering, few-shot examples, structured output |
| Consistent narrow task at lower cost/latency | **distillation** to a smaller model |
| Domain style/terminology the base model gets wrong after prompting | **fine-tuning** |
| Large unlabeled domain corpus | continued pre-training (where supported) |
Customization is supported for specific models and regions only; check the model support table.

## Data
Fine-tuning JSONL (format depends on model family), e.g. conversational:
```json
{"system":"You classify support tickets.","messages":[{"role":"user","content":"My invoice is wrong"},{"role":"assistant","content":"billing"}]}
```
or prompt/completion pairs for older formats. Hundreds to thousands of high-quality examples beat
large noisy sets. Hold out a validation file. Remove PII unless approved.

## Job
```bash
aws bedrock create-model-customization-job --job-name tickets-ft-1 \
  --custom-model-name tickets-classifier-v1 --customization-type FINE_TUNING \
  --base-model-identifier <base-model-id> --role-arn arn:aws:iam::111122223333:role/BedrockCustomization \
  --training-data-config s3Uri=s3://ml-data/tickets/train.jsonl \
  --validation-data-config 'validators=[{s3Uri=s3://ml-data/tickets/val.jsonl}]' \
  --output-data-config s3Uri=s3://ml-data/tickets/output/ \
  --hyperparameters epochCount=2,batchSize=8,learningRate=0.00001
aws bedrock get-model-customization-job --job-identifier tickets-ft-1
```
- Role needs S3 access (and KMS); VPC config option keeps training data access private.
- Output includes training/validation loss metrics; watch for overfitting (validation loss rising).

## Distillation
`--customization-type DISTILLATION` with a teacher model and a student model; supply prompts (and
optionally invocation logs from production) and Bedrock generates teacher responses as training data.
Good for moving a working large-model prompt to a cheaper, faster model with similar task accuracy.

## Deploy and use
- Custom models are invoked through **Provisioned Throughput** for many models, or on-demand
  deployment where supported; check which applies (cost difference is large).
- Evaluate against the base model and the prompt-only baseline with Bedrock model evaluation before switching traffic.

## Verify
- [ ] Evaluation shows the custom model beats prompt-only baseline on the held-out set.
- [ ] Cost model includes training plus provisioned/on-demand inference.
