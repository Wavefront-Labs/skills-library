---
id: computing-software.ai-ml-engineering.mlops.feature-attribution-drift-monitoring
name: feature-attribution-drift-monitoring
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, attribution-drift, model-monitoring, shap, sagemaker-clarify, vertex-model-monitoring]
level: practitioner
status: draft
description: "Detect when what drives predictions changes: SHAP attribution baselines, SageMaker Clarify explainability monitors, Vertex attribution skew and drift, and ranking comparisons."
sources:
  - https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-model-monitor-feature-attribution-drift.html
  - https://cloud.google.com/vertex-ai/docs/model-monitoring/monitor-explainable-ai
  - https://shap.readthedocs.io/en/latest/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Feature attribution drift

**Goal:** catch changes in which features drive the model's decisions, even when each input's distribution looks stable or labels are not yet available.

## Why it is different from data drift
Input drift tests each feature separately; a small shift in a feature the model relies on heavily matters more than a big shift in one it ignores. Attribution drift weights change by importance and also exposes broken pipelines (a feature suddenly constant gets near-zero attribution).

## Baseline
Compute global importance on the training or validation set: mean absolute SHAP value per feature, and the feature ranking. Store it with the model version.

## SageMaker Clarify explainability monitor
```python
from sagemaker.model_monitor import ModelExplainabilityMonitor, CronExpressionGenerator
mon = ModelExplainabilityMonitor(role=ROLE, instance_count=1, instance_type="ml.m5.xlarge")
mon.suggest_baseline(data_config=data_cfg, model_config=model_cfg, explainability_config=shap_cfg)
mon.create_monitoring_schedule(endpoint_input=endpoint_name, schedule_cron_expression=CronExpressionGenerator.daily(),
                               analysis_config=mon.latest_baselining_job_config.analysis_config)
```
It computes SHAP on captured endpoint traffic and compares the feature ranking to the baseline with NDCG; violations below the threshold (default around 0.9) emit CloudWatch metrics and violation reports. Needs data capture enabled on the endpoint.

## Vertex AI Model Monitoring
For models with an explanation spec, enable attribution skew (training vs serving) and drift (serving over time) objectives; set per-feature attribution score thresholds. Alerts go to email/Cloud Monitoring.

## DIY
```python
import numpy as np, shap
from scipy.stats import spearmanr
expl = shap.TreeExplainer(model)
cur = np.abs(expl.shap_values(window_sample)).mean(axis=0)
rho, _ = spearmanr(baseline_importance, cur)
shift = (cur - baseline_importance) / (baseline_importance.sum())
```
Alert on rank correlation drop or on any top-10 feature's share changing by more than a set fraction. Sample windows (a few thousand rows) - SHAP is expensive.

## Acting on alerts
Check for pipeline bugs first (feature constant, defaulted, unit change), then genuine population shift; retrain or adjust only after diagnosis.

## Verify
- [ ] Baseline importance stored with each model version.
- [ ] Zeroing a top feature in a test window triggers the alert.
