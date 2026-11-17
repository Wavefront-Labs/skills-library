---
id: computing-software.ai-ml-engineering.mlops.sagemaker-projects-codepipeline
name: sagemaker-projects-codepipeline
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, sagemaker-projects, codepipeline, codebuild, ci-cd, model-build, model-deploy]
level: practitioner
status: draft
description: "Set up MLOps CI/CD with SageMaker Projects templates: model-build and model-deploy repos, CodePipeline/CodeBuild stages, registry approval triggers and staged endpoint deploys."
sources:
  - https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-projects.html
  - https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-projects-templates-sm.html
  - https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# SageMaker Projects with CodePipeline / CodeBuild

**What a project gives you:** templated repos plus pipelines (via Service Catalog / CloudFormation) implementing build -> register -> approve -> deploy.

## Standard template: build, train and deploy
1. **Model build repo** (`modelbuild`): SageMaker Pipelines definition (`pipelines/<name>/pipeline.py`) and `codebuild-buildspec.yml`. A commit triggers CodePipeline -> CodeBuild, which upserts and starts the SageMaker Pipeline (preprocess, train, evaluate, condition, register).
2. **Model Registry:** the pipeline registers a model package with status `PendingManualApproval`.
3. **Model deploy repo** (`modeldeploy`): CloudFormation templates and per-stage config (`staging-config.json`, `prod-config.json`). An EventBridge rule on registry **approval** triggers the deploy pipeline: deploy to staging, run tests (CodeBuild), manual approval action, deploy to prod.

## Day-to-day operations
- Approve: `aws sagemaker update-model-package --model-package-arn ... --model-approval-status Approved` (or Studio UI). Rejecting keeps the current endpoint.
- Rollback: approve the previous model package version (re-triggers deploy) or redeploy the previous CloudFormation stack.
- Add tests in the deploy pipeline's test stage: endpoint smoke test, latency check, schema validation.

## Customizing
- Templates support GitHub/GitLab/Bitbucket via CodeStar connections, and Terraform or third-party CI in custom templates.
- Multi-account: build in a tooling/dev account, deploy to staging/prod accounts with cross-account roles and KMS keys on artifacts.

## Pitfalls
- IAM: CodeBuild role needs SageMaker pipeline permissions plus `iam:PassRole` for the execution role.
- Endpoint config changes in the deploy repo redeploy endpoints; use deployment guardrails (blue/green with auto-rollback) in the endpoint config.

## Verify
- [ ] End-to-end dry run: commit -> pipeline -> pending package -> approve -> staging endpoint -> tests -> prod.
