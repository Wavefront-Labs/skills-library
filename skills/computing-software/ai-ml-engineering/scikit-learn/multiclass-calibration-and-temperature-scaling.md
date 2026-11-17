---
id: computing-software.ai-ml-engineering.scikit-learn.multiclass-calibration-and-temperature-scaling
name: multiclass-calibration-and-temperature-scaling
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, calibration, temperature-scaling, multiclass-calibration, expected-calibration-error, neural-network-calibration]
level: practitioner
status: verified
description: "Calibrate multiclass and neural-net probabilities: one-vs-rest calibration in scikit-learn, temperature scaling on logits, expected calibration error and reliability checks."
sources:
  - https://arxiv.org/abs/1706.04599
  - https://scikit-learn.org/stable/modules/calibration.html#multiclass-support
  - https://scikit-learn.org/stable/modules/generated/sklearn.calibration.CalibrationDisplay.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiclass calibration and temperature scaling

**Goal:** get trustworthy class probabilities from multiclass models, especially neural networks, which are typically overconfident.

## scikit-learn multiclass
`CalibratedClassifierCV` calibrates multiclass models **one-vs-rest**: each class's score gets its own sigmoid/isotonic calibrator, then probabilities are renormalised to sum to 1. With many classes and little data per class, per-class calibrators overfit; prefer sigmoid, or temperature scaling below. Since scikit-learn 1.8 temperature scaling is built in: `CalibratedClassifierCV(est, method="temperature", cv=3)` applies `softmax(logits/T)` with one `T` fitted to minimise log loss and supports multiclass natively (no one-vs-rest step); `method` accepts `'sigmoid'`, `'isotonic'`, `'temperature'` on 1.9.1 (all three ran on a 4-class random forest: log loss 0.617 raw, 0.592 sigmoid, 0.591 isotonic, 0.593 temperature; predicted labels changed for sigmoid/isotonic in about 5% of rows). Isotonic is not recommended for far fewer than about 1000 calibration samples (per the docstring).

## Temperature scaling (Guo et al., 2017)
Divide logits by a single learned scalar `T > 0` before softmax. One parameter, fitted by minimising NLL on a validation set; does not change argmax predictions (accuracy unchanged).
```python
import torch
logits_val = torch.tensor(val_logits)     # (N, C), from the trained model, held-out data
y_val = torch.tensor(val_labels)
log_t = torch.zeros(1, requires_grad=True)          # optimise log T to keep T positive
opt = torch.optim.LBFGS([log_t], lr=0.1, max_iter=200)
def closure():
    opt.zero_grad()
    loss = torch.nn.functional.cross_entropy(logits_val / log_t.exp(), y_val)
    loss.backward(); return loss
opt.step(closure)
T = log_t.exp().item()        # T > 1 softens overconfident logits; the value depends on the model (3.3 for logits I scaled up 3x, log loss 1.605 -> 1.061)
probs = torch.softmax(test_logits / T, dim=1)
```
Extensions: vector/matrix scaling (per-class parameters) - more flexible, more overfitting risk.

## Measuring calibration
- **ECE (expected calibration error):** bin by max predicted probability (e.g. 15 bins), average |accuracy - confidence| weighted by bin size. Sensitive to binning; report the bin count.
- **NLL / Brier score:** proper scoring rules; use them as the primary metric, ECE as a diagnostic.
- Reliability diagram of confidence vs accuracy; for binary per-class views use `CalibrationDisplay.from_predictions(y == k, probs[:, k])`.

## Gotchas
- Fit T on a held-out split, never on training logits.
- Label smoothing and mixup already reduce overconfidence; T may come out near 1 or below.
- Calibration under distribution shift degrades; re-fit T periodically on fresh labelled data.

## Verify
- [ ] NLL and ECE on test data improved after scaling; accuracy unchanged.
- [ ] Temperature value logged with the model version.
- [ ] Reliability diagram reviewed.
