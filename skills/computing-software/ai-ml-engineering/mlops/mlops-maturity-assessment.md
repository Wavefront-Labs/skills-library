---
id: computing-software.ai-ml-engineering.mlops.mlops-maturity-assessment
name: mlops-maturity-assessment
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, mlops-maturity, ml-test-score, continuous-training, assessment, roadmap]
level: practitioner
status: draft
description: "Assess an ML team against Google's MLOps levels, the Azure MLOps maturity model and the ML Test Score rubric, then turn gaps into a prioritised roadmap."
sources:
  - https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning
  - https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/mlops-maturity-model
  - https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# MLOps maturity assessment

**Goal:** an evidence-based picture of where each ML system stands and the next few investments that reduce the most risk.

## Reference models
**Google Cloud levels**
- Level 0 - manual: notebooks, hand-off of a model file, rare releases, no monitoring.
- Level 1 - ML pipeline automation: automated training pipeline, continuous training on new data or triggers, data/model validation, metadata, feature store optional.
- Level 2 - CI/CD pipeline automation: pipeline code itself is built, tested and deployed automatically.

**Azure MLOps maturity (0-4)**
0 No MLOps, 1 DevOps but no MLOps, 2 automated training, 3 automated model deployment, 4 full MLOps automated operations (automated retraining and deployment driven by monitoring).

**ML Test Score** - 28 tests in four sections: data and features, model development, ML infrastructure, monitoring. Each test scores 0 (not done), 0.5 (done manually, documented) or 1 (automated). Section score = sum; overall score = the minimum of the four sections, so a team cannot compensate for no monitoring with great tests.

## Running the assessment
1. Scope per ML system, not per team; systems differ.
2. For each criterion collect evidence (pipeline link, test file, dashboard, runbook), not opinions.
3. Interview the on-call: how was the last bad model caught, and how long did rollback take?
4. Score, and record the weakest section for each system.

## Evidence checklist (sample)
- Can any engineer retrain the production model from a commit and data version? (reproducibility)
- Is there a schema/data validation gate before training and before scoring?
- Is a candidate compared to the current model on the same eval set before promotion?
- Is training/serving skew checked?
- Are model and data drift monitored with alerts and an owner?
- Rollback time to previous model?
- Cost per training run and per 1k predictions known?

## Turning gaps into a roadmap
- Fix the lowest ML Test Score section first.
- Prefer changes that shorten time-to-detect and time-to-rollback for production incidents.
- Do not jump levels: CT (level 1) without validation gates automates shipping bad models.
- Keep it proportional: a quarterly batch model rarely needs level 2; a fraud model scoring live traffic does.
Present per-system scores, the top three gaps, owners and target dates; reassess every two quarters.

## Verify
- [ ] Each score is backed by a linked artifact.
- [ ] Roadmap items map to specific failed criteria.
