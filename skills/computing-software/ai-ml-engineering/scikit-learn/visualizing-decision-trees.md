---
id: computing-software.ai-ml-engineering.scikit-learn.visualizing-decision-trees
name: visualizing-decision-trees
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, plot-tree, export-graphviz, export-text, decision-tree, model-interpretability, dtreeviz]
level: practitioner
status: verified
description: "Visualise scikit-learn decision trees with plot_tree, export_text and export_graphviz: readable depth limits, feature/class names, and reading splits, impurity and values."
sources:
  - https://scikit-learn.org/stable/modules/tree.html#tree
  - https://scikit-learn.org/stable/modules/generated/sklearn.tree.plot_tree.html
  - https://scikit-learn.org/stable/modules/generated/sklearn.tree.export_graphviz.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Visualising trees (plot_tree / export_graphviz)

## Matplotlib: plot_tree
```python
from sklearn.tree import plot_tree
fig, ax = plt.subplots(figsize=(24, 10))
plot_tree(clf, max_depth=3, feature_names=feature_names, class_names=[str(c) for c in clf.classes_],
          filled=True, rounded=True, impurity=True, proportion=False, fontsize=9, ax=ax)
fig.savefig("tree.png", dpi=150, bbox_inches="tight")
```
- `max_depth` here only limits drawing, not the model (a depth-4 iris tree drew 17 text boxes with `max_depth=3`). The root box reads `petal width (cm) <= 0.8 | gini = 0.667 | samples = 150 | value = [50, 50, 50] | class = 0`.
- In a Pipeline: `plot_tree(pipe[-1], feature_names=pipe[:-1].get_feature_names_out())` (with NumPy input the names come out as `x0..x3`; fit on a DataFrame to keep column names). Thresholds are in the transformed space (scaled or one-hot columns), so scaling makes them hard to read: trees do not need scaling; drop scalers for interpretable trees.

## Text: export_text
```python
from sklearn.tree import export_text
print(export_text(clf, feature_names=list(feature_names), max_depth=4, show_weights=True))
```
Good for logs, code review and diffs between model versions (output is `|--- petal width (cm) <= 0.80` / `|   |--- weights: [50.00, 0.00, 0.00] class: 0`, with `truncated branch of depth N` beyond `max_depth`).

## Graphviz
```python
from sklearn.tree import export_graphviz
export_graphviz(clf, out_file="tree.dot", feature_names=feature_names, class_names=class_names, filled=True, rounded=True)
```
The file starts `digraph Tree { node [shape=box, style="filled, rounded", ...] ;` and each node label repeats the plot_tree fields (checked).

## Reading a node
- `feature <= threshold`: left branch is True.
- `gini`/`entropy`/`squared_error`: impurity at that node.
- `samples`: training rows reaching it (`proportion=True` shows it as a percentage, `samples = 100.0%`, and `value` as fractions, `[0.333, 0.333, 0.333]`).
- `value`: class counts in the plot with `proportion=False` (`[50, 50, 50]`) / mean target for regression. The raw `clf.tree_.value` array holds fractions on 1.9.1 (row sums to 1.0, shape `(n_nodes, n_outputs, n_classes)`), use `n_node_samples` for counts.
- `class`: majority class.

## Programmatic access
`clf.tree_` has arrays `feature`, `threshold`, `children_left`, `children_right`, `value`, `n_node_samples` (all ran); `clf.apply(X)` gives the leaf per sample; `clf.decision_path(X)` the nodes visited (a sparse matrix, 1 for each visited node). Use these to explain a single prediction path.

## Ensembles
A random forest or GBM has hundreds of trees; plotting one tree explains almost nothing. Use permutation importance, SHAP or partial dependence, or distil to a single shallow surrogate tree trained on the ensemble's predictions (report the surrogate's fidelity).
