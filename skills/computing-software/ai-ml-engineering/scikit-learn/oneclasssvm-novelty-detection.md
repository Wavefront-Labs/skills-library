---
id: computing-software.ai-ml-engineering.scikit-learn.oneclasssvm-novelty-detection
name: oneclasssvm-novelty-detection
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, oneclasssvm, novelty-detection, sgdoneclasssvm, anomaly-detection, nu, rbf-kernel]
level: practitioner
status: verified
description: "Detect novel inputs with scikit-learn OneClassSVM and SGDOneClassSVM: scaling, nu and gamma tuning without labels, kernel approximation for scale, and novelty vs outlier setups."
sources:
  - https://scikit-learn.org/stable/modules/outlier_detection.html#novelty-detection
  - https://scikit-learn.org/stable/modules/generated/sklearn.svm.OneClassSVM.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDOneClassSVM.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Novelty detection with OneClassSVM

**Novelty detection**: training data is clean (normal only); flag new points unlike it. **Outlier detection**: training data is contaminated; find the odd ones in it. OneClassSVM is designed for novelty; IsolationForest / LOF are usually better for contaminated data.

## Fit
```python
from sklearn.svm import OneClassSVM
ocsvm = make_pipeline(StandardScaler(), OneClassSVM(kernel="rbf", nu=0.01, gamma="scale"))
ocsvm.fit(X_normal)
pred = ocsvm.predict(X_new)                 # +1 inlier, -1 novelty
score = ocsvm.decision_function(X_new)      # negative = outside the boundary
```
- Scale features: RBF distances are meaningless otherwise.
- `nu` ~ upper bound on the fraction of training points treated as outliers and lower bound on support vector fraction. Set it to the tolerated false-alarm rate on normal data (e.g. 0.01). On 5000 standard-normal training rows with `gamma="scale"`, nu=0.01 gave 1.1% of training rows as outliers, 2.6% flagged on fresh normal rows, and 2% of rows as support vectors; nu=0.1 gave 10%, 11.2% and 10.3%.
- `gamma` controls boundary smoothness: large gamma = tight boundary (overfits, flags many normal points); small = loose. With nu=0.01 the held-out false-alarm rate was 1.3% at gamma 0.01, 1.6% at 0.1, 17% at 1 and 92% at 10, while a far-away cluster was always caught (recall 1.0), so recall on obvious anomalies says nothing about gamma.

## Tuning without labelled anomalies
- Hold out normal data; choose gamma so the held-out false-positive rate is close to `nu`.
- If a few known anomalies exist, use them only for validation: maximise recall on them at the target false-positive rate.
- Alternatively threshold `decision_function` yourself at a chosen quantile of held-out normal scores, which decouples alarm rate from nu.

## Scale
Kernel OneClassSVM is O(n^2) to O(n^3); fit time with 20 features and nu=0.1 was 0.3 s at 10k, 1.5 s at 20k and 6.9 s at 40k rows (about 4.6x for doubling), so it is fine to ~10-50k samples. For more:
```python
from sklearn.kernel_approximation import Nystroem
from sklearn.linear_model import SGDOneClassSVM
big = make_pipeline(StandardScaler(), Nystroem(gamma=0.1, n_components=500, random_state=0),
                    SGDOneClassSVM(nu=0.01, random_state=0))
```
Linear time; `SGDOneClassSVM` has `partial_fit` for streaming (checked). On the same normal data it flagged 1.4% of fresh normal rows at nu=0.01.

## Other novelty options
- `LocalOutlierFactor(novelty=True)` then `predict` on new data (without `novelty=True`, `predict` does not exist: `AttributeError`). It flagged 1.3% of fresh normal rows.
- `IsolationForest` (works for novelty too, scales well, no scaling needed), but set `contamination` yourself: with the default `"auto"` threshold it flagged 18.9% of fresh standard-normal rows as novel.
- Autoencoder reconstruction error or density on embeddings for images/text.

## Gotchas
- High-dimensional raw features weaken RBF distances; reduce dimensions (PCA) or use learned embeddings.
- Calling `fit_predict` on the training set gives about `nu` outliers by construction; that is not a performance measure.
- Concept drift: periodically refit on recent verified-normal data.
