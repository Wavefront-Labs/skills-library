---
id: computing-software.cloud-infrastructure-engineering.aws.bedrock-model-evaluation-jobs
name: bedrock-model-evaluation-jobs
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, bedrock, model-evaluation, llm-as-a-judge, rag-evaluation, human-evaluation, evaluation-datasets]
level: practitioner
status: docs-checked
description: "Evaluate models and RAG on Bedrock: automatic metrics, LLM-as-a-judge, human review jobs, Knowledge Base retrieval evaluation, custom prompt datasets and reading the report."
sources: ["https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html", "https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation-jobs-management-create.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bedrock model evaluation jobs

## Job types
| Type | Scores with | Use for |
|---|---|---|
| Automatic (programmatic) | built-in metrics (for example accuracy and robustness) on built-in or your datasets | quick comparisons on standard tasks |
| LLM-as-a-judge | a second LLM acting as judge | open-ended generation at scale |
| Human | your own employees or subject-matter experts | final quality calls, subjective criteria |
| RAG (Knowledge Bases) | judge model on Knowledge Base retrieval, or retrieve-and-generate | tuning chunking, retrieval and prompts |
You can also bring your own inference responses (evaluate outputs from any model or application).

## Prompt dataset (JSONL)
Use JSONL with one record per prompt; take the exact field names from the Bedrock prompt dataset requirements page for your job type.
- Use representative prompts, including hard and adversarial cases.

## Run
```bash
aws bedrock create-evaluation-job --job-name summarise-judge-1 \
  --role-arn arn:aws:iam::111122223333:role/BedrockEval \
  --evaluation-config file://eval-config.json \
  --inference-config file://models.json \
  --output-data-config s3Uri=s3://ml-eval/results/
```
(Build the JSON configs in the console once and export, or follow the API reference for
`automated.datasetMetricConfigs` and `evaluatorModelConfig`.)
- Role needs S3 access to datasets and results and permission to invoke the candidate and judge models.
- Human-based jobs require CORS permissions on the S3 output bucket.

## Reading results
- Report card per metric and category with score distributions; per-prompt outputs and judge rationales in S3.
- Compare candidates on the same dataset: model A vs B, prompt v1 vs v2, chunking 300 vs 800 tokens.
- Judge bias: a judge model can be biased; spot-check with humans and keep the judge model fixed across comparisons.

## Practice
- Keep a versioned "golden" dataset per use case; run evaluation in CI for prompt or model changes.
- Track cost: each evaluation invokes candidate and judge models per prompt.

## Verify
- [ ] Baseline evaluation stored; changes require equal or better scores on key metrics.
- [ ] Human review sample agrees with judge scores on a subset.

## Checked

2026-10-28

Confirmed: automated and human evaluation types, judge-model jobs, RAG source evaluation, Builtin.Accuracy and Builtin.Robustness metrics, CORS requirement for human jobs (Bedrock User Guide pages); datasetMetricConfigs and evaluatorModelConfig under automated config (botocore); create-evaluation-job flags (check_commands).

Removed: toxicity metric, judge metric list, AWS-managed reviewers, sample JSONL field names, 100-1,000 prompt guidance, bedrock:InvokeModel action name, CORS claim for console viewing, judge-bias specifics.

Method: documentation only; no commands were run.
