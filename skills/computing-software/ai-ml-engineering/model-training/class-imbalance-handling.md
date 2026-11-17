---
id: computing-software.ai-ml-engineering.model-training.class-imbalance-handling
name: class-imbalance-handling
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [class-imbalance, oversampling, undersampling, smote, class-weights, focal-loss, resampling, threshold-tuning, pr-auc, rare-event-modeling, anomaly-detection, fraud-detection]
level: advanced
status: gated
description: "Handle imbalanced classification correctly: why accuracy lies, resampling vs class weighting vs threshold tuning, and the specific ways SMOTE and oversampling cause leakage."
sources:
  - https://imbalanced-learn.org/stable/
  - https://arxiv.org/abs/1708.02002
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Handling class imbalance without fooling yourself

**Goal:** build and evaluate a model on a dataset where the positive class is rare (fraud, churn, defect detection) without the standard metric and resampling traps that make an imbalanced-data model look better than it is.

## 1. Fix the metric before fixing the data
- **Accuracy is close to useless on imbalanced data** — a dataset with 0.5% positive class gets 99.5% accuracy by predicting "negative" always. If you're still reporting accuracy as the headline metric on an imbalanced problem, that's the first thing to fix, not the resampling strategy.
- Use **PR-AUC (precision-recall AUC)** over ROC-AUC when positives are rare and false positives are costly relative to the rare-class base rate — ROC-AUC can look deceptively good on severe imbalance because the false-positive rate axis is dominated by the huge negative class (simulated: 0.48% positives and a score shifted by 1.5 gave ROC-AUC 0.862 but average precision 0.068 against a 0.0048 base rate); PR-AUC is sensitive to exactly the tradeoff (precision at a given recall) that usually matters in these problems.
- Report metrics **at a specific, chosen operating threshold** relevant to the business decision (e.g. "precision at 80% recall," or "review-queue size at this threshold"), not just an aggregate AUC — a model's AUC can be fine while its behavior at the threshold anyone will actually deploy is unacceptable.

## 2. Resampling: what it does and does not fix
- **Random oversampling** (duplicate minority-class rows) and **SMOTE** (synthesize new minority-class points by interpolating between real minority neighbors) both rebalance the *training* distribution so the loss function stops being dominated by the majority class — they do not create new information, and SMOTE's interpolated points can land in regions that don't correspond to real minority-class examples, especially in high dimensions or with categorical features (plain SMOTE assumes continuous features; `SMOTENC` and `SMOTEN` exist in imbalanced-learn 0.14.2 for mixed and categorical data).
- **The most common SMOTE leakage bug**: applying SMOTE (or any oversampling) **before** the train/validation split, or inside cross-validation folds incorrectly — synthetic points generated from the full dataset can have near-neighbors that leak into the validation fold, inflating validation metrics in a way that doesn't hold on real unseen data. Tested on pure noise (600 rows, 20 features, 5% positives, 1-NN): SMOTE before 5-fold CV gave average precision 0.78, while `imblearn.pipeline.make_pipeline(SMOTE(), KNN)` gave 0.051, equal to the 0.05 base rate. Oversampling must happen **only on the training fold**, after the split, refit inside each CV fold independently (imbalanced-learn's `Pipeline` with a sampler step handles this correctly if used; a manual SMOTE call before `train_test_split` does not).
- **Random undersampling** (drop majority-class rows) is simpler and avoids synthetic-data risk, but throws away real data — viable when the majority class is large enough that the dropped rows don't matter, risky when every majority example carries information the model needs.
- **Class weighting** (`class_weight="balanced"` in scikit-learn, or a weighted loss: `nn.CrossEntropyLoss(weight=...)` and `nn.BCEWithLogitsLoss(pos_weight=...)` run in PyTorch 2.14; Keras not checked (gated: unconfirmed, source is paywalled or blocked)) achieves a similar rebalancing effect on the loss function without touching the data at all — often the simplest correct choice, and avoids the leakage risk of resampling entirely, since no synthetic/duplicated rows exist to leak. Try this before reaching for SMOTE; it's less code and less failure surface.

## 3. Alternatives worth knowing beyond basic resampling/weighting
- **Focal loss** (Lin et al., arXiv 1708.02002, "Focal Loss for Dense Object Detection"; down-weights the loss contribution of easy, already-well-classified examples, used widely in object detection) helps when the imbalance is extreme and most majority examples are "easy" — the model spends more of its gradient budget on the hard/rare cases rather than endlessly reinforcing already-correct majority predictions.
- **Threshold tuning instead of retraining**: for many production decisions, moving the classification threshold (rather than changing the training process at all) after training on the natural class distribution is simpler, avoids resampling risk entirely, and the model's predicted probabilities stay calibrated to the real-world base rate — calibration is often more valuable downstream (e.g. for ranking cases by risk) than a resampled model's.
- **Anomaly-detection framing** (one-class models, isolation forests) instead of binary classification is worth considering when positives are extremely rare and/or qualitatively different rather than just underrepresented (e.g. fraud patterns that don't look like a "hard" version of normal transactions, but a structurally different thing) — classification resampling techniques assume the rare class is learnable from its own examples; if there aren't enough even after oversampling, anomaly detection reframes the problem usefully.

## Verify
- [ ] Reported metric is PR-AUC, precision/recall at a stated threshold, or another imbalance-aware metric — not raw accuracy as the headline number.
- [ ] Any resampling (SMOTE, oversampling, undersampling) is applied only inside the training fold, after the split, refit per CV fold — verified by checking the pipeline, not assumed.
- [ ] Class weighting was tried and compared before reaching for synthetic oversampling.
- [ ] The chosen operating threshold is explicit and tied to a real business tradeoff, not left at the default 0.5.
- [ ] If calibrated probabilities matter downstream, confirmed the resampling/weighting choice didn't break calibration (check a reliability diagram).
