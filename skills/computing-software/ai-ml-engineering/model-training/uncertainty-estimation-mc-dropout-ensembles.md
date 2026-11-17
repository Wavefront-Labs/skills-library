---
id: computing-software.ai-ml-engineering.model-training.uncertainty-estimation-mc-dropout-ensembles
name: uncertainty-estimation-mc-dropout-ensembles
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, uncertainty-estimation, mc-dropout, deep-ensembles, epistemic-uncertainty, predictive-entropy]
level: practitioner
status: draft
description: "Estimate predictive uncertainty: deep ensembles, MC dropout at inference, predictive entropy vs mutual information, evaluating with selective prediction and calibration."
sources:
  - https://arxiv.org/abs/1612.01474
  - https://arxiv.org/abs/1506.02142
  - https://arxiv.org/abs/1906.02530
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Uncertainty estimation (deep ensembles, MC dropout)

**Why:** route low-confidence predictions to humans, detect inputs unlike the training data, and decide when to abstain.

## Deep ensembles (strongest simple baseline)
Train M = 3-10 models with different random seeds (and data order); average predicted probabilities.
```python
probs = torch.stack([m(x).softmax(-1) for m in models])      # (M, B, C)
mean_p = probs.mean(0)
entropy = -(mean_p * mean_p.clamp_min(1e-12).log()).sum(-1)               # total uncertainty
expected_entropy = -(probs * probs.clamp_min(1e-12).log()).sum(-1).mean(0)
mutual_info = entropy - expected_entropy                                   # epistemic (disagreement)
```
Cost: M x training and inference. Cheaper variants: snapshot ensembles, BatchEnsemble, multi-head models, or ensembling only the last layers.

## MC dropout
Keep dropout active at inference and run T stochastic forward passes:
```python
def enable_dropout(model):
    model.eval()
    for m in model.modules():
        if isinstance(m, torch.nn.Dropout): m.train()
enable_dropout(model)
probs = torch.stack([model(x).softmax(-1) for _ in range(30)])
```
Only works if the model was trained with dropout; BatchNorm must stay in eval mode (hence the selective enable). Usually weaker than ensembles.

## Other options
Temperature-scaled softmax confidence (cheap, decent for in-distribution), conformal prediction sets (coverage guarantees), evidential/Bayesian last layers, quantile regression for regression intervals.

## Evaluate uncertainty, not just accuracy
- Selective prediction: sort by uncertainty, plot accuracy vs coverage (risk-coverage curve); the area under it should improve.
- Calibration: ECE/reliability diagrams.
- Shift robustness: does uncertainty rise on corrupted or out-of-domain data?

## Verify
- [ ] Accuracy on the most confident 80% of predictions is clearly higher than overall accuracy.
