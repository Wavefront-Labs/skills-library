---
id: computing-software.ai-ml-engineering.scikit-learn.isolationforest-and-localoutlierfactor-anomaly-detection
name: isolationforest-and-localoutlierfactor-anomaly-detection
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, isolationforest, localoutlierfactor, anomaly-detection, novelty-detection, contamination]
level: practitioner
status: gated
description: "Detect anomalies with IsolationForest and LocalOutlierFactor in scikit-learn: contamination vs score thresholds, novelty mode, scaling and evaluating with few labels."
sources:
  - https://scikit-learn.org/stable/modules/outlier_detection.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.LocalOutlierFactor.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IsolationForest / LocalOutlierFactor anomaly detection

## Outlier vs novelty detection
- **Outlier detection**: training data contains anomalies; find them in that same data.
- **Novelty detection**: train on clean data; flag new points that differ. LOF needs `novelty=True` for this.

## IsolationForest
```python
from sklearn.ensemble import IsolationForest
iso = IsolationForest(n_estimators=300, max_samples=256, contamination="auto", random_state=0, n_jobs=-1)
iso.fit(X_train)
scores = -iso.score_samples(X_new)      # higher = more anomalous
flags = iso.predict(X_new)              # -1 anomaly, 1 normal (threshold from contamination)
```
- Anomalies are isolated in fewer random splits. Scale-invariant per feature (no scaling needed), fast, handles many dimensions.
- `max_samples` defaults to `"auto"` = `min(256, n_samples)` (scikit-learn docstring); small subsamples work well, and larger ones can mask anomalies in dense regions (gated: unconfirmed, source is paywalled or blocked).
- Weak at local anomalies inside dense regions and at anomalies defined by feature combinations along axis-oblique directions.

## LocalOutlierFactor
```python
from sklearn.neighbors import LocalOutlierFactor
lof = LocalOutlierFactor(n_neighbors=35, contamination="auto")     # outlier mode
flags = lof.fit_predict(Xs); lof_scores = -lof.negative_outlier_factor_
lof_nov = LocalOutlierFactor(n_neighbors=35, novelty=True).fit(Xs_clean)
new_scores = -lof_nov.score_samples(Xs_new)
```
- Compares local density to neighbours': finds local anomalies that global methods miss.
- Needs scaling; distance-based, slow for very large n; `n_neighbors` 20-50 typical.
- In outlier mode `lof.predict` does not exist, and in novelty mode `fit_predict` does not exist: both raise "This 'LocalOutlierFactor' has no attribute ..." (tested). `n_neighbors` defaults to 20.

## Thresholds, not contamination
`contamination` only sets the threshold on scores (fraction flagged in training). It doesn't change the model (for IsolationForest; scores were identical for `contamination=0.1` and `"auto"` in a test). In production, pick a threshold from the score distribution and alert budget: e.g. flag top 0.5% per day, or a score cutoff validated on labelled incidents.

## Evaluation with few labels
- If you have some labelled anomalies, compute PR-AUC / precision@k on scores (not ROC-AUC, which looks good under heavy imbalance).
- No labels: review the top-k flagged items with domain experts; track stability of scores over time.
- Compare against simple baselines: z-scores per feature, Mahalanobis distance (`EllipticEnvelope`), reconstruction error from PCA.

## Gotchas
- Categorical features: one-hot inflates dimensions; IsolationForest handles ordinal encoding better than LOF.
- Duplicated points distort LOF (zero distances): 10 identical points among 60 gave a maximum LOF around 2e9 with `n_neighbors=5` (tested); dedupe or add tiny jitter.
- Seasonal/time-dependent normality: build features relative to context (deviation from same hour last week) before scoring.

## Verify
Inject synthetic anomalies (shifted copies of real rows) into a validation set and confirm they rank near the top.
