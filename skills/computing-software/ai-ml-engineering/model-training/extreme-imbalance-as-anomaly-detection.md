---
id: computing-software.ai-ml-engineering.model-training.extreme-imbalance-as-anomaly-detection
name: extreme-imbalance-as-anomaly-detection
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, extreme-imbalance, anomaly-detection, rare-events, one-class, fraud-detection, precision-at-k]
level: practitioner
status: draft
description: "Handle extreme class imbalance (under 0.1% positives) by reframing as anomaly or rare-event detection: unsupervised and semi-supervised detectors, hybrid scoring and evaluation."
sources:
  - https://scikit-learn.org/stable/modules/outlier_detection.html
  - https://github.com/yzhao062/pyod
  - https://imbalanced-learn.org/stable/user_guide.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Extreme imbalance framed as anomaly detection

When positives are a tiny fraction (1 in 1,000 to 1 in 1,000,000) and few in number (dozens to hundreds), supervised classifiers learn little about the positive class, and new positive types (new fraud patterns) are missed entirely.

## Decide the framing
| Positives available | Positive types | Approach |
|---|---|---|
| Thousands+ | stable | supervised with class weights / focal loss, PR-AUC evaluation |
| Tens to hundreds | stable | supervised on aggressive features + anomaly score as a feature |
| Few or none | changing / unknown | unsupervised or semi-supervised anomaly detection |

## Unsupervised detectors
- `IsolationForest(contamination="auto")`: fast, robust default for tabular data.
- `LocalOutlierFactor(novelty=True)`: local density; good when normal data has clusters of different density.
- `OneClassSVM` / `SGDOneClassSVM` on scaled features: clean normal training data needed.
- Autoencoders / reconstruction error for high-dimensional data (images, sensor sequences).
- PyOD provides 40+ detectors with a common API (`ECOD`, `COPOD` are parameter-free and fast).
Train on data believed normal (filter known positives out) for novelty-style detection.

## Semi-supervised hybrid
1. Unsupervised anomaly scores as features.
2. Supervised model on labelled positives + features + anomaly scores.
3. Rank by a blend; review top-ranked cases.
Anomaly scores catch novel patterns, the classifier catches known ones.

## Evaluation
- ROC AUC is misleading at extreme imbalance (huge negative count makes FPR small). Use **PR-AUC (average precision)**, **precision@k** where k = daily review capacity, and **recall at fixed alert budget**.
- Few positives make metrics noisy: bootstrap confidence intervals; use time-based splits so test positives come from a later period.
- Human-in-the-loop: measure investigator hit rate on alerts.

## Operations
- Thresholds set by alert capacity (top N per day) rather than probability.
- Feedback loop: confirmed cases become labels; retrain the supervised part regularly; monitor drift of anomaly score distributions.
- Exploration: sample a few random low-score cases for review to estimate missed positives (otherwise you only learn about what you flagged).
