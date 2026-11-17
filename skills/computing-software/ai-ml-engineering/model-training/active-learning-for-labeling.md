---
id: computing-software.ai-ml-engineering.model-training.active-learning-for-labeling
name: active-learning-for-labeling
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, active-learning, uncertainty-sampling, labeling-budget, modal, human-in-the-loop, minority-class]
level: practitioner
status: draft
description: "Spend a labelling budget efficiently with active learning: uncertainty, margin and diversity sampling, batch selection, cold start, stopping rules and finding rare-class examples."
sources:
  - https://burrsettles.com/pub/settles.activelearning.pdf
  - https://modal-python.readthedocs.io/en/latest/
  - https://arxiv.org/abs/1708.00489
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Active learning to collect labels

Instead of labelling random examples, the model picks the unlabelled examples whose labels would help most. Typical savings: same accuracy with a fraction of the labels, and many more rare-class examples per label spent.

## Loop
1. **Seed set**: label a small random/stratified set (a few hundred), plus keyword or rule-based searches to seed rare classes.
2. Train the model; score the unlabelled pool.
3. Select a batch by a query strategy; send to annotators.
4. Add labels, retrain, repeat. Keep a **random-sampled test set** fixed and separate for honest evaluation.

## Query strategies
| Strategy | Score | Notes |
|---|---|---|
| Least confidence | `1 - max p` | simple |
| Margin | `p1 - p2` (smallest first) | robust default for classification |
| Entropy | `-sum p log p` | multiclass |
| Query by committee / ensembles | disagreement among models | better uncertainty |
| Diversity (core-set, k-center) | cover the embedding space | avoids redundant batches (Sener and Savarese 2018) |
| Hybrid (uncertainty within clusters, BADGE) | both | best for large batch sizes |
| Rare-class targeting | highest predicted probability of the rare class | maximises positives found per label |

```python
from modAL.models import ActiveLearner
from modAL.uncertainty import margin_sampling
learner = ActiveLearner(estimator=LogisticRegression(max_iter=1000), query_strategy=margin_sampling, X_training=X0, y_training=y0)
idx, _ = learner.query(X_pool, n_instances=100)
learner.teach(X_pool[idx], y_new)
```

## Batch mode
Pure top-k uncertainty picks near-duplicates. Cluster the top uncertain candidates (k-means on embeddings) and pick one per cluster, or use BADGE.

## For minority classes
Mix strategies per batch: e.g. 50% highest rare-class probability (finds positives), 30% margin (refines boundary), 20% random (calibration and discovering unknown types).

## Stopping
Stop when held-out metric plateaus across rounds, when predictions on a fixed stability set stop changing, or when budget ends.

## Pitfalls
- The labelled set becomes biased (not representative): do not use it to estimate prevalence or as a test set; reweight if training models that need calibrated probabilities.
- Model-dependent: examples chosen for model A may not help model B.
- Annotation quality on hard (uncertain) items is lower; include adjudication or multiple annotators.
- Tools: modAL, small-text (text), Label Studio / Argilla / Prodigy integrate model-in-the-loop annotation.
