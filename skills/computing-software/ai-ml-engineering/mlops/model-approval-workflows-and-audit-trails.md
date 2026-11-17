---
id: computing-software.ai-ml-engineering.mlops.model-approval-workflows-and-audit-trails
name: model-approval-workflows-and-audit-trails
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, model-approval-workflow, model-governance, sagemaker-model-registry, audit-trail, segregation-of-duties]
level: practitioner
status: draft
description: "Gate production models behind recorded approvals: SageMaker registry approval status and EventBridge deploys, MLflow/UC alias promotion via CI, evidence packs and audit logs."
sources:
  - https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry-approve.html
  - https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry-deploy.html
  - https://mlflow.org/docs/latest/ml/model-registry/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Model approval workflows and audit trails

**Goal:** no model reaches production without a named approver, recorded evidence and an automated, logged deployment.

## Approval states (SageMaker Model Registry)
Model package versions carry `ModelApprovalStatus`: `PendingManualApproval` (default from pipelines), `Approved`, `Rejected`.
```python
sm.update_model_package(ModelPackageArn=arn, ModelApprovalStatus="Approved",
                        ApprovalDescription="AUC +1.2pt vs champion; fairness OK; risk ticket RISK-481")
```
An EventBridge rule on `SageMaker Model Package State Change` with `ModelApprovalStatus: Approved` starts the deployment pipeline (staging, tests, then prod with manual gate). Rejected versions stay for audit.

## MLflow / Unity Catalog
No built-in approval state: model a request with a tag (`approval=pending`), approvals happen in a PR or ticket, and CI (with the only principal allowed to set production aliases) sets `@champion` after checks pass, writing approver and ticket into version tags.

## Evidence pack (attached or linked to the version)
- Evaluation vs current champion on the frozen test set and key slices.
- Fairness and robustness results; known limitations.
- Data and code versions (lineage), training run link.
- Model card.
- Risk review / sign-off for regulated models (SR 11-7 style validation).

## Segregation of duties
The person or role that trained the model cannot approve it. Enforce with IAM: data scientists lack `UpdateModelPackage` approval on prod groups; approvers lack write access to training code. Two-person rule for high-risk models.

## Audit trail
- CloudTrail records `UpdateModelPackage` with the principal and parameters; retain per policy.
- Deployment pipeline logs which version went where and when.
- Periodically reconcile: every production endpoint's model version has an Approved status and evidence.

## Gotchas
- Auto-approval in CI for low-risk models is fine if the criteria are codified and logged; manual approval without evidence is not governance.
- Approvals must be per version; approving a model group or name approves nothing specific.

## Verify
- [ ] Deploying a `PendingManualApproval` version is impossible through the pipeline.
- [ ] For a production model, approver, timestamp and evidence can be produced in minutes.
