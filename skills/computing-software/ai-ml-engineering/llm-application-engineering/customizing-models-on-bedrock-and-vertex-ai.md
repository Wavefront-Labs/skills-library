---
id: computing-software.ai-ml-engineering.llm-application-engineering.customizing-models-on-bedrock-and-vertex-ai
name: customizing-models-on-bedrock-and-vertex-ai
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, bedrock-custom-models, vertex-ai-tuning, fine-tuning, model-distillation, custom-model-import]
level: practitioner
status: draft
description: "Customize foundation models on Amazon Bedrock and Vertex AI: fine-tuning, continued pre-training and distillation jobs, Custom Model Import, deployment and cost model."
sources:
  - https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html
  - https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-import-model.html
  - https://cloud.google.com/vertex-ai/generative-ai/docs/models/tune-models
  - https://docs.aws.amazon.com/bedrock/latest/userguide/model-distillation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Customizing models on Bedrock and Vertex AI

**Goal:** a managed, customised model (tuned, distilled or imported) runs inside your cloud account with your governance, after prompting and RAG proved insufficient.

## Bedrock customization types
| Type | Data | Use for |
|---|---|---|
| Fine-tuning | labelled JSONL (prompt/completion or conversation format) | task format, tone, classification |
| Continued pre-training | unlabelled domain text | domain vocabulary (supported models only) |
| Distillation | prompts (teacher generates responses) | small, cheap student matching a large teacher on your task |
| Reinforcement fine-tuning | prompts + reward/grader (where offered) | verifiable tasks |
Which base models support which type changes often; check the supported-models table.
```python
bedrock = boto3.client("bedrock")
bedrock.create_model_customization_job(
    jobName="support-ft-2026-10", customModelName="support-intent-v3", roleArn=ROLE,
    baseModelIdentifier="<base model id>", customizationType="FINE_TUNING",
    trainingDataConfig={"s3Uri": "s3://ml/ft/train.jsonl"},
    validationDataConfig={"validators": [{"s3Uri": "s3://ml/ft/val.jsonl"}]},
    outputDataConfig={"s3Uri": "s3://ml/ft/output/"},
    hyperParameters={"epochCount": "2", "batchSize": "8", "learningRate": "0.00001"},
    customModelKmsKeyId=KMS_KEY)
```
Training data stays in your S3; the role needs read on data and write on output; use VPC configuration and KMS for regulated data.

## Serving custom models on Bedrock
Custom models are invoked through provisioned throughput or, for supported models, on-demand custom model deployments - check pricing before training, as a small hourly commitment can dwarf training cost.

## Custom Model Import
Bring fine-tuned open-weight models (supported architectures, Hugging Face safetensors format) from S3 with `create_model_import_job`; they are served serverlessly behind the Bedrock API, billed by active model copies over time windows, with cold starts after idle. Good for teams who fine-tune with their own stack but want Bedrock's API, IAM and guardrails.

## Vertex AI
```python
from vertexai.tuning import sft
job = sft.train(source_model="<gemini model id>", train_dataset="gs://ml/ft/train.jsonl",
                validation_dataset="gs://ml/ft/val.jsonl", epochs=3, tuned_model_display_name="support-intent-v3")
```
The tuned model gets its own endpoint; preference tuning and distillation recipes exist for some models; open models (Llama, Gemma, Mistral) can be tuned and deployed from Model Garden on your own Vertex endpoints.

## Process
1. Baseline: best prompt + RAG on the base model, measured on an eval set.
2. Data: hundreds to thousands of high-quality examples; dedupe; hold out a test set.
3. Train, then compare tuned vs baseline on the test set, including safety and refusal behaviour.
4. Factor serving cost and deprecation: base model retirement forces re-tuning.

## Verify
- [ ] Tuned model beats prompt-only baseline on held-out data by the required margin.
- [ ] Serving cost per month estimated before training.
- [ ] Training data, job config and model ARN/ID recorded in the model inventory.
