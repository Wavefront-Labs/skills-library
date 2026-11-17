---
id: computing-software.ai-ml-engineering.mlops.bias-and-fairness-metrics-clarify-fairlearn
name: bias-and-fairness-metrics-clarify-fairlearn
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, model-governance, fairness-metrics, fairlearn, sagemaker-clarify, demographic-parity, equalized-odds, bias-mitigation]
level: practitioner
status: draft
description: "Measure and mitigate model bias: choosing fairness metrics for the harm, Fairlearn MetricFrame and mitigators, SageMaker Clarify pre/post-training bias reports, and trade-offs."
sources:
  - https://fairlearn.org/main/user_guide/index.html
  - https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-configure-processing-jobs.html
  - https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-measure-post-training-bias.html
  - https://fairmlbook.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bias and fairness metrics with Fairlearn and SageMaker Clarify

**Goal:** detect whether a model's errors or decisions differ across groups in ways that cause harm, and act on it with documented trade-offs.

## Pick metrics from the harm
| Harm | Metric family |
|---|---|
| Allocation (loans, jobs): who gets the positive outcome | selection rate per group, demographic parity difference/ratio (disparate impact) |
| Quality of service: model works worse for some groups | per-group accuracy/recall/error rates |
| Errors with different costs (false negatives in screening) | equalized odds / equal opportunity (TPR, FPR per group) |
| Scores interpreted as risk | calibration within groups |
These criteria generally can't all be satisfied at once when base rates differ; choose with domain and legal input and write the choice down.

## Fairlearn
```python
from fairlearn.metrics import MetricFrame, selection_rate, true_positive_rate, false_positive_rate
from fairlearn.metrics import demographic_parity_difference, equalized_odds_difference
mf = MetricFrame(metrics={"sel": selection_rate, "tpr": true_positive_rate, "fpr": false_positive_rate},
                 y_true=y, y_pred=y_hat, sensitive_features=df["group"])
print(mf.by_group, mf.difference())
equalized_odds_difference(y, y_hat, sensitive_features=df["group"])
```
Mitigation: `ThresholdOptimizer` (post-processing, group-specific thresholds - requires the sensitive feature at prediction time, which may be legally restricted), `ExponentiatedGradient` (in-training constraint). Always report the accuracy cost.

## SageMaker Clarify
A processing job producing bias reports:
- **Pre-training** metrics on data: class imbalance (CI), difference in proportions of labels (DPL), etc.
- **Post-training** metrics on predictions: disparate impact (DI), difference in positive proportions of predicted labels (DPPL), recall/accuracy differences, and more.
Configure `DataConfig`, `BiasConfig(label_values_or_threshold=[1], facet_name="age_group")`, `ModelConfig`, then `SageMakerClarifyProcessor.run_bias(...)`. Clarify also produces SHAP explanations and can monitor bias drift on endpoints.

## Practicalities
- You often don't have the sensitive attribute; consider proxies carefully, privacy constraints, and audits on a consented sample.
- Small groups -> wide CIs; report n.
- Intersectional groups (gender x age) can hide issues that single attributes don't show.

## Verify
- [ ] Chosen fairness criterion and rationale documented.
- [ ] Per-group metrics with n and CIs in the evaluation report and model card.
- [ ] Mitigation (if any) evaluated for both fairness and accuracy impact.
