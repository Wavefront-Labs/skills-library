---
id: computing-software.ai-ml-engineering.mlops.label-quality-and-annotation-workflows
name: label-quality-and-annotation-workflows
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, sagemaker-ground-truth, annotation-quality, data-labeling, inter-annotator-agreement, label-noise]
level: practitioner
status: draft
description: "Run labeling with SageMaker Ground Truth or similar tools and keep labels trustworthy: guidelines, gold questions, consensus, agreement metrics, audits and label-error detection."
sources:
  - https://docs.aws.amazon.com/sagemaker/latest/dg/sms.html
  - https://docs.aws.amazon.com/sagemaker/latest/dg/sms-annotation-consolidation.html
  - https://docs.cleanlab.ai/stable/tutorials/datalab/workflows.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Label quality and annotation workflows

**Goal:** training and evaluation labels are accurate enough that model errors are model errors, not labeling errors.

## Workflow
1. **Guidelines:** definitions, decision rules for edge cases, positive and negative examples, what to do when unsure ("skip / flag"). Version them.
2. **Pilot:** 100-200 items labeled by several annotators; measure agreement; fix the guideline where people disagree.
3. **Production labeling** with built-in quality controls.
4. **Audit** a random sample each batch by an expert.
5. **Feedback** to annotators on mistakes; update guidelines.

## SageMaker Ground Truth
- Workforces: private (your employees, via Cognito/OIDC), vendor, or public (Mechanical Turk - never for sensitive data).
- Built-in task types (classification, bounding box, segmentation, NER) or custom Liquid HTML templates.
- `NumberOfHumanWorkersPerDataObject` > 1 enables annotation consolidation (weighted voting for classification, box merging); the output manifest records consolidated labels with a confidence score.
- Automated data labeling trains a model on human labels and auto-labels confident items (active learning); verify its precision on an audit sample before trusting it.
- Ground Truth Plus is the managed-service option with expert labelers.
Output is an augmented manifest (JSON Lines) with label and metadata per object - version it with the dataset.

## Measuring quality
- **Gold questions:** items with known answers mixed into tasks; per-annotator accuracy, remove or retrain low scorers.
- **Agreement:** Cohen's kappa (2 annotators), Fleiss' kappa or Krippendorff's alpha (many). Low agreement means the task or guideline is ambiguous, not that annotators are bad.
- **Adjudication:** disagreements go to an expert; keep both raw and adjudicated labels.

## Finding label errors after the fact
Train with cross-validation to get out-of-sample predicted probabilities, then rank likely mislabeled items:
```python
from cleanlab.filter import find_label_issues
issues = find_label_issues(labels=y, pred_probs=oof_probs, return_indices_ranked_by="self_confidence")
```
Review the top-ranked items manually; relabel, do not auto-flip. Clean the evaluation set first - noisy test labels cap measurable accuracy.

## Gotchas
- Class imbalance: annotators drift toward the majority label; balance batches or use pre-filtering.
- Guideline changes mid-project create inconsistent labels; record guideline version per label.
- PII in data needs a private workforce and access controls.

## Verify
- [ ] Agreement and gold accuracy reported per batch.
- [ ] Every label has annotator, guideline version and timestamp.
