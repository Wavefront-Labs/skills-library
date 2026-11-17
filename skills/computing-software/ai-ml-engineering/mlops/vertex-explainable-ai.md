---
id: computing-software.ai-ml-engineering.mlops.vertex-explainable-ai
name: vertex-explainable-ai
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, vertex-explainable-ai, explainability, sampled-shapley, integrated-gradients, xrai]
level: practitioner
status: draft
description: "Configure Vertex Explainable AI: choose sampled Shapley, integrated gradients or XRAI, set explanation metadata and baselines, request explanations online and in batch."
sources:
  - https://cloud.google.com/vertex-ai/docs/explainable-ai/overview
  - https://cloud.google.com/vertex-ai/docs/explainable-ai/configuring-explanations-feature-based
  - https://cloud.google.com/vertex-ai/docs/explainable-ai/getting-explanations
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Vertex Explainable AI and explanation reports

**Goal:** predictions from a Vertex model come with feature attributions that reviewers and monitoring can use, at known cost.

## Methods
| Method | Models | Notes |
|---|---|---|
| Sampled Shapley | any (non-differentiable OK: trees, ensembles) | `path_count` trades accuracy for cost |
| Integrated gradients | differentiable (TF/NN) | `step_count`; needs a sensible baseline |
| XRAI | image models | region-based saliency built on IG |
| Example-based | embeddings models | nearest training examples instead of attributions |

## Configure at upload
```python
from google.cloud import aiplatform
from google.cloud.aiplatform import explain
params = explain.ExplanationParameters({"sampled_shapley_attribution": {"path_count": 10}})
metadata = explain.ExplanationMetadata(
    inputs={"tenure": {}, "monthly_spend": {}, "plan": {}},
    outputs={"churn_probability": {}})
model = aiplatform.Model.upload(display_name="churn", artifact_uri=ARTIFACTS,
    serving_container_image_uri=IMAGE, explanation_parameters=params, explanation_metadata=metadata)
```
For TF models, input/output metadata names must match the SavedModel signature tensors. Set `input_baselines` deliberately (median row, or all-zeros only if zero is meaningful); attributions are relative to the baseline.

## Request explanations
```python
resp = endpoint.explain(instances=[{"tenure": 3, "monthly_spend": 80, "plan": "basic"}])
for a in resp.explanations[0].attributions:
    print(a.baseline_output_value, a.instance_output_value, dict(a.feature_attributions))
```
Attributions sum to `instance_output_value - baseline_output_value` (approximation error is reported). Batch: `batch_predict(..., generate_explanation=True)`.

## Cost and accuracy
Explanations multiply compute (path_count or step_count model evaluations per instance). Explain on demand or on a sample, not every production request. Increase `path_count`/`step_count` until the approximation error is small for your use.

## Explanation reports
For model reviews, aggregate attributions over a representative set: global mean |attribution| per feature, attributions per key segment, and example local explanations for false positives and negatives. Use them to spot leakage (an ID or timestamp with high attribution) and to feed attribution drift monitoring.

## Verify
- [ ] Attributions sum to output minus baseline within reported error.
- [ ] Baseline choice documented in the model card.
