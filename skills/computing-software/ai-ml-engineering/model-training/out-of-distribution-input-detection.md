---
id: computing-software.ai-ml-engineering.model-training.out-of-distribution-input-detection
name: out-of-distribution-input-detection
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, ood-detection, out-of-distribution, energy-score, mahalanobis, open-set, model-monitoring]
level: practitioner
status: draft
description: "Detect out-of-distribution inputs at inference: max softmax, energy and Mahalanobis scores, embedding kNN distance, threshold setting on in-distribution data and evaluation."
sources:
  - https://arxiv.org/abs/1610.02136
  - https://arxiv.org/abs/2010.03759
  - https://github.com/kkirchheim/pytorch-ood
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Out-of-distribution input detection

Classifiers give confident predictions on inputs unlike anything they were trained on (a cat photo to a chest X-ray model). OOD detection flags such inputs so the system can abstain or route to a human.

## Scores (higher = more in-distribution unless noted)
| Method | Score | Needs |
|---|---|---|
| Max softmax probability (MSP) | `max softmax(logits)` | nothing; baseline (Hendrycks and Gimpel 2017) |
| Energy | `T * logsumexp(logits / T)` | nothing; usually better than MSP (Liu et al. 2020) |
| Max logit | `max logits` | nothing; strong for large label sets |
| Mahalanobis | distance to class-conditional Gaussian of penultimate features (lower = in-dist) | training features |
| kNN on embeddings | distance to k-th nearest training embedding (normalised features) | feature bank |
| ODIN | temperature scaling + input perturbation | gradient at inference |
```python
logits = model(x)
energy = torch.logsumexp(logits, dim=1)          # T=1
feats = F.normalize(backbone(x), dim=1)
d_knn = faiss_index.search(feats.numpy(), k=50)[0][:, -1]
```

## Thresholds
Set on **in-distribution validation data only**: choose the threshold that keeps e.g. 95% of in-distribution inputs (TPR 95%). Then measure on OOD sets.

## Evaluation
- Build OOD test sets that resemble realistic failures: other domains, corrupted inputs, new classes (near-OOD) and unrelated data (far-OOD).
- Metrics: AUROC (ID vs OOD), FPR@95%TPR, AUPR.
- Near-OOD (new but similar classes) is much harder than far-OOD; report both.

## Improving detectability
- Train with outlier exposure (an auxiliary dataset of OOD examples, push uniform predictions on them).
- Better backbones / pretraining usually improve OOD detection more than clever scores.
- For tabular data: density / isolation forest on inputs, or distance in feature space; also check simple range and schema validation first (unseen categories, out-of-range values).
- LLM/text: embedding distance to training distribution, or perplexity under a reference model.

## Production
- Log OOD score distribution over time; rising OOD rate signals drift.
- Decide the action: abstain, fallback model, human review. Measure the business cost of both false alarms and misses.
- Libraries: pytorch-ood, OpenOOD benchmarks, Alibi Detect (outlier and drift detectors).
