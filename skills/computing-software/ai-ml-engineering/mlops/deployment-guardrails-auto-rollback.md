---
id: computing-software.ai-ml-engineering.mlops.deployment-guardrails-auto-rollback
name: deployment-guardrails-auto-rollback
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, deployment-guardrails, automatic-rollback, blue-green-deployment, canary-release, cloudwatch-alarms]
level: practitioner
status: draft
description: "Deploy models with automatic rollback: SageMaker deployment guardrails (blue/green canary/linear, alarms, baking period), Kubernetes/Argo Rollouts analysis and rollback criteria."
sources:
  - https://docs.aws.amazon.com/sagemaker/latest/dg/deployment-guardrails.html
  - https://docs.aws.amazon.com/sagemaker/latest/dg/deployment-guardrails-blue-green.html
  - https://argo-rollouts.readthedocs.io/en/stable/features/analysis/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Deployment guardrails and automatic rollback

**Goal:** a bad model version (crashes, latency regression, broken outputs) is detected and rolled back within minutes, without a human watching.

## SageMaker endpoints
```python
sm.update_endpoint(
    EndpointName="fraud-prod", EndpointConfigName="fraud-v8-config",
    DeploymentConfig={
        "BlueGreenUpdatePolicy": {
            "TrafficRoutingConfiguration": {"Type": "CANARY",
                "CanarySize": {"Type": "CAPACITY_PERCENT", "Value": 10},
                "WaitIntervalInSeconds": 600},
            "TerminationWaitInSeconds": 300,
            "MaximumExecutionTimeoutInSeconds": 3600},
        "AutoRollbackConfiguration": {"Alarms": [{"AlarmName": "fraud-prod-5xx"},
                                                 {"AlarmName": "fraud-prod-p99-latency"},
                                                 {"AlarmName": "fraud-prod-score-mean-shift"}]}})
```
- Traffic types: `ALL_AT_ONCE`, `CANARY` (small slice, then the rest), `LINEAR` (steps).
- During the baking period, any alarm in ALARM state rolls traffic back to the blue fleet.
- Alarms must exist beforehand on endpoint/variant metrics (`Invocation5XXErrors`, `ModelLatency`) or custom metrics you publish (e.g. mean prediction score, null-output rate).
- Rolling deployments (`RollingUpdatePolicy`) for large GPU fleets where doubling capacity is too expensive.

## Kubernetes
Argo Rollouts / Flagger with an `AnalysisTemplate` querying Prometheus (error rate, latency, custom model metrics); failing analysis aborts and reverts the canary. KServe supports `canaryTrafficPercent` with manual or scripted promotion.

## What to alarm on
- Operational: 5xx/4xx rate, p99 latency, container restarts, OOMs.
- Model sanity: prediction distribution shift vs previous version (mean/positive rate), share of default/fallback outputs, schema validation failures.
- Business metrics are usually too slow for rollback; use them for post-deploy review.

## Verify
- [ ] Game day: deploy a deliberately broken version to staging; confirm rollback triggers and timing.
