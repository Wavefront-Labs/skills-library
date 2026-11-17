---
id: computing-software.ai-ml-engineering.model-training.choosing-validation-and-test-set-sizes
name: choosing-validation-and-test-set-sizes
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, test-set-size, validation-set, data-splits, confidence-intervals, statistical-power]
level: practitioner
status: verified
description: "Size validation and test sets from the precision you need: binomial standard errors, minimum positives for rare classes, detecting a given improvement and small-data alternatives."
sources:
  - https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets
  - https://www.deeplearning.ai/
  - https://scikit-learn.org/stable/modules/cross_validation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Choosing validation and test set sizes

**Wrong question:** "70/15/15 or 80/10/10?" **Right question:** how precisely must I measure the metric, and what difference between models must I detect?

## Precision of an accuracy-like metric
Standard error of a proportion p measured on n samples: `SE = sqrt(p (1 - p) / n)`; 95% CI is about +/- 2 SE.
| n | SE at p = 0.90 | 95% CI half-width |
|---|---|---|
| 1,000 | 0.0095 | +/- 1.9 points |
| 10,000 | 0.0030 | +/- 0.6 points |
| 100,000 | 0.00095 | +/- 0.2 points |
To detect a 0.5-point improvement you need roughly 10k+ test examples (the table values and the 13,830 below were computed and match) (paired comparisons on the same test set need fewer; use McNemar).

## Rare classes
What matters is the number of **positives**. Recall measured on 50 positives has SE up to 7 points. Aim for several hundred positives in validation and test (a rule of thumb, not a derived figure; the SE at 50 positives, sqrt(0.25/50) = 0.0707, was computed); if impossible, use cross-validation and report intervals.

## Practical rules
- Big data (millions): 1-2% each for validation and test may suffice (tens of thousands of samples); give the rest to training (rule of thumb; check it against the SE table for your metric).
- Small data (under ~10k): use k-fold CV (or repeated CV) for model selection and keep a modest final test set; report CIs.
- Test set must reflect the deployment distribution (time period, geography, traffic mix) more than it must be large; a big unrepresentative test set gives precise wrong answers.
- Validation set used for many tuning decisions overfits gradually; refresh or keep a separate untouched test set.

## Quick calculator
```python
import math
def n_for_halfwidth(p, halfwidth, z=1.96): return math.ceil(z**2 * p * (1 - p) / halfwidth**2)
n_for_halfwidth(0.9, 0.005)   # ~13,830 examples for +/- 0.5 points
```

## Verify
- [ ] Every reported test metric includes its CI or SE; decisions use differences larger than the noise.
