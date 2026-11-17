---
id: computing-software.ai-ml-engineering.scikit-learn.sgdclassifier-and-partial-fit-out-of-core
name: sgdclassifier-and-partial-fit-out-of-core
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, sgdclassifier, partial-fit, out-of-core, sgdregressor, online-learning]
level: practitioner
status: verified
description: "Train linear models on data larger than memory with SGDClassifier/SGDRegressor and partial_fit: loss choice, learning-rate schedules, scaling in chunks and hashing features."
sources:
  - https://scikit-learn.org/stable/modules/sgd.html
  - https://scikit-learn.org/stable/computing/scaling_strategies.html
  - https://scikit-learn.org/stable/auto_examples/applications/plot_out_of_core_classification.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SGDClassifier and partial_fit for out-of-core learning

## Model choice via loss
```python
from sklearn.linear_model import SGDClassifier
clf = SGDClassifier(loss="log_loss", penalty="l2", alpha=1e-5, learning_rate="optimal", random_state=0)
```
- `loss="hinge"` = linear SVM (no `predict_proba`: AttributeError), `"log_loss"` = logistic regression (gives `predict_proba`), `"modified_huber"` = robust with probabilities (checked), `"squared_hinge"` and `"perceptron"` also have no `predict_proba`; `"squared_error"`/`"huber"`/`"epsilon_insensitive"` in `SGDRegressor` (all three fitted).
- `alpha` is regularisation strength (like 1/(C*n)); grid 1e-7 to 1e-2.
- `penalty="elasticnet"` with `l1_ratio` for sparse models.

## Out-of-core loop
```python
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.preprocessing import StandardScaler
vec = HashingVectorizer(n_features=2**20, alternate_sign=False)    # stateless: no fit, fixed width
classes = np.array([0, 1])                                         # all classes, required on first call
for epoch in range(3):
    for chunk in pd.read_csv("big.csv", chunksize=100_000):
        X = vec.transform(chunk["text"]); y = chunk["label"].values
        clf.partial_fit(X, y, classes=classes)
```
- `classes` must be given on the first `partial_fit` call (the model can't know unseen labels): omitting it raises `classes must be passed on the first call to partial_fit.`.
- Feature extraction must be stateless or pre-fitted: `HashingVectorizer`, `FeatureHasher`, or a scaler fitted incrementally (`StandardScaler.partial_fit` over a first pass).
- Shuffle: SGD assumes i.i.d. order. Data sorted by time or label makes it chase the last chunks. In a test on 2,500 posts (two newsgroups, hashing vectoriser) the same 1,500 training rows fed in five 300-row chunks sorted by label gave 0.486 held-out accuracy, against 0.916 when shuffled (3 epochs). Shuffle files/chunks, or at least within chunks.
- `partial_fit` does one pass per call and ignores `max_iter`/early stopping (with `max_iter=1, tol=None` it gave `n_iter_=1`, `t_=301` after one 300-row call); the learning rate schedule still uses the internal step count `t_` (4501 after 3 epochs of 1,500 rows).

## Learning rate
- `learning_rate="optimal"` (default for classifier) works well with scaled data.
- For streaming with drift, `learning_rate="constant"`/`"adaptive"` with `eta0` keeps adapting; `"invscaling"` decays.
- `average=True` (ASGD) averages weights; it is documented as helping stability, but on the 1,500-row test a single `fit(average=True)` scored 0.904, against 0.916 for the plain `partial_fit` loop, so it was no better there.

## Scaling is mandatory
SGD is sensitive to feature scale in general (scikit-learn advises scaling); in a quick test with 10 dense features scaled by 1 to 1e3 the unscaled and scaled fits both reached 0.99 training accuracy, so verify on your data. Dense features: fit `StandardScaler` (via `partial_fit` pass; `StandardScaler.partial_fit` over four 500-row chunks reproduced the full-data mean) and transform each chunk. Sparse text: TF normalisation or `MaxAbsScaler`.

## Evaluate progressively
Hold out a fixed validation chunk; after each chunk, score it and log. Or "test-then-train" (prequential): score each new chunk before calling `partial_fit` on it.

## Other incremental estimators
`MultinomialNB`, `BernoulliNB`, `Perceptron`, `PassiveAggressiveClassifier`, `MiniBatchKMeans`, `IncrementalPCA`, `MLPClassifier` all have `partial_fit` (checked with `hasattr`; `PassiveAggressiveClassifier`'s signature on 1.9.1 is `C`-based with `loss='hinge'`).

## Verify
On a sample that fits in memory, compare SGD's held-out score against `LogisticRegression` on the same features; it should be close with enough epochs. In the test SGD (`alpha=1e-5`, 3 epochs) scored 0.916 and `LogisticRegression(C=1)` 0.853 on the same hashed features, so the gap depends on matching the regularisation (`alpha` vs `C`) rather than on SGD being less accurate.
