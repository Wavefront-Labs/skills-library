---
id: computing-software.ai-ml-engineering.model-training.sliced-evaluation-and-subgroup-metrics
name: sliced-evaluation-and-subgroup-metrics
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, metrics, sliced-evaluation, subgroup-metrics, fairlearn-metricframe, slice-discovery, model-evaluation]
level: practitioner
status: draft
description: "Evaluate models per slice (segment, region, device, demographic): MetricFrame and groupby recipes, slice sizes with CIs, worst-slice gates and slice discovery."
sources:
  - https://fairlearn.org/main/user_guide/assessment/index.html
  - https://www.tensorflow.org/tfx/model_analysis/get_started
  - https://arxiv.org/abs/1807.06068
  - https://developers.google.com/machine-learning/guides/rules-of-ml
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sliced evaluation and subgroup performance

**Goal:** find where the model fails before users do, since aggregate metrics hide bad performance on important minorities.

## Compute metrics per slice
```python
from fairlearn.metrics import MetricFrame, count
from sklearn.metrics import recall_score, precision_score
mf = MetricFrame(metrics={"recall": recall_score, "precision": precision_score, "n": count},
                 y_true=y_te, y_pred=y_hat, sensitive_features=df_te[["region", "device"]])
mf.by_group                          # table per (region, device)
mf.difference(method="between_groups")
```
Plain pandas works too: `df.groupby("segment").apply(lambda g: pd.Series({"auc": roc_auc_score(g.y, g.p), "n": len(g)}))`.

Choose slices from: business segments (plan, region, channel), data properties (input length, image brightness, language), time (new vs old customers), and protected attributes where legally appropriate.

## Small slices
- Report n per slice. Bootstrap CIs per slice (resample rows within the slice); a 10-point recall gap on 40 examples is often noise.
- Set a minimum n before a slice can fail a release gate.

## Release gates
- Gate on the **worst** important slice, not just the average: "no slice with n >= 500 below 0.80 recall" and "no slice regresses more than 2 points vs champion".
- Compare candidate vs champion per slice; an average gain can hide a slice regression.

## Finding unknown bad slices
- Error analysis on high-loss examples, then group by metadata.
- Automated slice discovery: SliceFinder (Chung et al.) searches feature-value combinations with significantly higher loss; for unstructured data, cluster embeddings of errors (Domino-style) and inspect clusters.
- Fit a shallow decision tree predicting "model was wrong" from metadata: its leaves are candidate weak slices.

## Verify
- [ ] Slice table with n and CIs in every model evaluation report.
- [ ] Worst-slice and per-slice regression gates in the promotion pipeline.
- [ ] Slice discovery run at least once per major model change.
