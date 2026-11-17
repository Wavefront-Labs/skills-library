---
id: computing-software.cloud-infrastructure-engineering.aws.sagemaker-and-bedrock
name: sagemaker-and-bedrock
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sagemaker, bedrock, machine-learning, generative-ai, foundation-models, sagemaker-endpoints, serverless-inference, training-jobs, sagemaker-studio, sagemaker-pipelines, model-registry, bedrock-knowledge-bases, bedrock-agents, bedrock-guardrails, converse-api, provisioned-throughput, model-access, inference-profiles, rag]
level: practitioner
status: draft
description: "Operate ML and generative AI on AWS: SageMaker training jobs, endpoints and pipelines with the right IAM/VPC shape, and Bedrock model access, Converse API, knowledge bases, guardrails and cost."
sources: ["Amazon SageMaker Developer Guide - Training jobs, real-time and serverless inference", "Amazon SageMaker Developer Guide - SageMaker Pipelines and Model Registry", "Amazon Bedrock User Guide - Model access, Converse API and inference profiles", "Amazon Bedrock User Guide - Knowledge Bases, Agents and Guardrails"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SageMaker and Bedrock — the infrastructure side of ML and generative AI on AWS

**Goal:** data scientists get training and hosting without root in prod; model endpoints
are sized, autoscaled and monitored like any service; generative-AI apps call Bedrock
through one API with guardrails, private networking and a cost ceiling.

## 1. SageMaker building blocks
| Piece | What it is |
|---|---|
| **Studio / notebooks** | Managed JupyterLab per user (domain + user profiles, IAM or SSO) |
| **Processing / Training jobs** | Ephemeral containers (`ml.*` instances) pulling data from S3, writing model artifacts (`model.tar.gz`) to S3; Spot training with checkpoints saves 60–90 % |
| **Endpoints** | Real-time (always-on instances, autoscaling), **serverless** (pay per ms, cold starts, ≤ 6 GB), **async** (queue, large payloads, scale to 0), **batch transform** (offline) |
| **Pipelines** | DAG of steps (process → train → evaluate → register → deploy) with caching; triggered by EventBridge/CodePipeline |
| **Model Registry** | Model package groups with versions and approval status gating deploys |
| **Feature Store, Model Monitor, Clarify** | Features, drift/quality monitoring, bias/explainability |
| **JumpStart** | One-click foundation/open models deployed to endpoints you own |

- Training job skeleton (SDK): `Estimator(image_uri, role, instance_type='ml.g5.xlarge', instance_count=1, use_spot_instances=True, max_wait=7200, checkpoint_s3_uri=…)` → `.fit({'train': 's3://…'})`.
- Endpoint sizing: load-test with **Inference Recommender**; set autoscaling on
  `InvocationsPerInstance` target; multi-model endpoints or **inference components** pack
  several models on one instance; GPU `g5/g6` for deep learning, `inf2` (Inferentia) for cheaper LLM serving.
- Monitor endpoints: `ModelLatency`, `OverheadLatency`, `Invocation4XX/5XXErrors`, `CPU/GPUUtilization`, `GPUMemoryUtilization`; alarm and scale.
- Cost traps: idle real-time endpoints and forgotten Studio apps (set idle shutdown, lifecycle configs); use serverless/async for spiky traffic.

## 2. SageMaker platform guardrails
- **VPC mode** for jobs/endpoints (`VpcConfig`), S3/ECR/STS/CloudWatch/SageMaker API/runtime
  **VPC endpoints**, no internet (`EnableNetworkIsolation`); KMS keys for volumes and outputs.
- IAM: a per-team **execution role** scoped to their S3 prefixes and ECR repos; condition
  `sagemaker:VpcSubnets`/`sagemaker:InstanceTypes` in SCPs to block non-VPC jobs and `p5`
  without approval; `sagemaker:ResourceTag` ABAC.
- Images: curated containers in your ECR (pull-through from SageMaker DLCs), scanned.
- Studio domain in VPC-only mode with a private hosted zone; SSO via Identity Center.
- Service quotas per instance type for training/endpoints are low by default — raise ahead.

## 3. Bedrock
- **Model access**: enabled per model per region under *Model access* in the console (an API exists for the same); third-party models need EULA acceptance and some a use-case form.
- **Inference**: use the **Converse API** (`bedrock-runtime converse`/`converse-stream`) — one request/response shape across models (messages, system, tools, images/docs);
  `invoke-model` only for model-specific features. Keep `modelId` in config, not code.
  ```bash
  aws bedrock-runtime converse --model-id anthropic.claude-3-5-sonnet-20241022-v2:0 \
    --messages '[{"role":"user","content":[{"text":"Summarise: ..."}]}]' \
    --inference-config '{"maxTokens":512,"temperature":0.2}'
  ```
- **Cross-region inference profiles** (`us.`/`eu.` prefixed ids) route across regions for
  higher throughput and resilience; **application inference profiles** tag usage for cost allocation per app.
- Throughput: on-demand (tokens-per-minute and requests-per-minute **quotas per model per
  region**, raise via Service Quotas), **provisioned throughput** (model units, 1–6-month
  commitments) for predictable high volume, **batch inference** (async, 50 % cheaper) for bulk.
- **Knowledge Bases** (managed RAG): S3 docs → chunking → embeddings → vector store
  (OpenSearch Serverless, Aurora pgvector, Pinecone…); `retrieve` / `retrieve-and-generate`.
  Sync on schedule; metadata filters for tenancy.
- **Agents**: LLM + action groups (Lambda/OpenAPI) + knowledge bases; **Guardrails**: content
  filters, denied topics, word lists, PII redaction, contextual grounding checks — attach by
  `guardrailIdentifier` to Converse/agents and version them.
- **Prompt management / flows** for versioned prompts and no-code chains; **custom models**
  via fine-tuning or imported weights (model import).
- Networking: **VPC endpoints** for `bedrock-runtime`, `bedrock`, `bedrock-agent-runtime`
  so traffic stays private; IAM `bedrock:InvokeModel` scoped by model ARN; SCP to allow only approved model ids.
- Observability: **model invocation logging** (CloudWatch Logs/S3, full prompts/responses —
  treat as sensitive), CloudWatch metrics `Invocations`, `InvocationLatency`, `InputTokenCount`,
  `OutputTokenCount`, `InvocationThrottles`, `InvocationClientErrors`.
- Cost control: tag via application inference profiles, Budgets on Bedrock service,
  anomaly monitor, `maxTokens` caps, cache (prompt caching where supported), route cheap
  models for easy tasks.

## 4. Choosing
- Bedrock when a foundation model via API fits (text, chat, RAG, agents, embeddings); no
  infra, per-token billing.
- SageMaker when you train/fine-tune your own models, need custom containers, or host open
  models with full control (and at scale can be cheaper than per-token).
- Both: SageMaker for embeddings/classic ML, Bedrock for generation; or JumpStart models on SageMaker endpoints behind the same app.

## Gotchas
- Bedrock throttling (`ThrottlingException`) is per model per region; SDK retries with backoff plus cross-region inference profiles are the fix, not a support ticket alone.
- Model ids/versions are deprecated on a schedule (Health events); pin and plan upgrades; test prompts against the new version.
- Invocation logging captures prompts with customer data — KMS, retention, access control.
- SageMaker endpoints in a VPC without the runtime endpoint cannot be invoked from a Lambda in that VPC.
- Studio spaces/apps bill while running; enforce idle shutdown via lifecycle config.
- Training with Spot needs checkpointing or you restart from zero on interruption.
- Unconfirmed: model ids, regions, quota defaults and feature names change monthly — verify against the current Bedrock/SageMaker docs before quoting.

## Verify
- [ ] `aws bedrock list-foundation-models --by-output-modality TEXT` shows access granted for the approved models only; an unapproved model id is denied by SCP.
- [ ] Converse call via the VPC endpoint succeeds from a private subnet with no NAT.
- [ ] Guardrail blocks a test denied topic and redacts a test PII string; version pinned in config.
- [ ] SageMaker training job in VPC mode with Spot completes and checkpoints exist in S3.
- [ ] Endpoint autoscaling triggers under load test; idle endpoints/Studio apps list is empty at end of day.
