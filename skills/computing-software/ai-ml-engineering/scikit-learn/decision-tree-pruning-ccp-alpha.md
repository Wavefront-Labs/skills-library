---
id: computing-software.ai-ml-engineering.scikit-learn.decision-tree-pruning-ccp-alpha
name: decision-tree-pruning-ccp-alpha
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, ccp-alpha, decision-tree-pruning, decisiontreeclassifier, export-text, cost-complexity-pruning]
level: practitioner
status: verified
description: "Control and prune decision trees: max_depth/min_samples_leaf pre-pruning, cost_complexity_pruning_path and ccp_alpha selection by CV, and readable rules with export_text."
sources:
  - https://scikit-learn.org/stable/modules/tree.html
  - https://scikit-learn.org/stable/auto_examples/tree/plot_cost_complexity_pruning.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.tree.export_text.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Decision tree pruning (ccp_alpha) and export_text

**Goal:** a single interpretable tree that generalizes, e.g. for policy rules or explaining a segment.

## Pre-pruning
`max_depth`, `min_samples_leaf` (often the most effective single knob; choose it from the CV curve and domain meaning, a fraction of samples rather than a fixed count for rule extraction), `min_samples_split`, `max_leaf_nodes`, `min_impurity_decrease`. Unrestricted trees memorize the training set.

## Post-pruning: minimal cost-complexity
```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
path = DecisionTreeClassifier(random_state=0).cost_complexity_pruning_path(X_tr, y_tr)
alphas = path.ccp_alphas[:-1]                     # last alpha prunes to the root (1 node, tested)
scores = [cross_val_score(DecisionTreeClassifier(ccp_alpha=a, random_state=0), X_tr, y_tr, cv=5).mean()
          for a in alphas]
best = alphas[int(np.argmax(scores))]
tree = DecisionTreeClassifier(ccp_alpha=best, random_state=0).fit(X_tr, y_tr)
```
Use the one-standard-error rule (largest alpha whose score is within one std of the best) for an even simpler tree. Alternatively put `ccp_alpha` in a GridSearchCV over the path values.

## Read the rules
```python
from sklearn.tree import export_text
print(export_text(tree, feature_names=list(feature_names), show_weights=True, decimals=2))
```
`plot_tree(tree, feature_names=..., class_names=..., filled=True, max_depth=3)` for a figure.

## Notes
- Trees do not need scaling; `DecisionTreeClassifier` accepts NaN natively since scikit-learn 1.3 (fit on data with NaN worked on 1.9.1, tested, also with `splitter="random"`).
- `class_weight="balanced"` for imbalanced classes changes split choices; check leaf class proportions.
- Single trees are high-variance: small data changes produce different trees. For prediction quality use ensembles; for explanation, report stability (fit on bootstrap samples and compare top splits).
- `criterion="log_loss"`/`"entropy"` vs `"gini"` rarely matters.

## Verify
- [ ] CV score vs alpha plot saved; final tree depth and leaf count reported.
- [ ] Rules reviewed with a domain expert for nonsensical splits (leakage signals).
