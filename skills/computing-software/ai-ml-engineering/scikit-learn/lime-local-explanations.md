---
id: computing-software.ai-ml-engineering.scikit-learn.lime-local-explanations
name: lime-local-explanations
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, lime, local-explanations, explainable-ai, model-interpretability, tabular-explainer]
level: practitioner
status: verified
description: "Explain individual predictions with LIME for tabular and text models: LimeTabularExplainer setup, kernel width, discretisation, stability checks and when SHAP is better."
sources:
  - https://github.com/marcotcr/lime
  - https://lime-ml.readthedocs.io/en/latest/
  - https://arxiv.org/abs/1602.04938
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LIME local explanations

LIME perturbs one instance, gets model predictions for the perturbations, weights them by proximity, and fits a small linear model. The linear coefficients are the explanation for that prediction.

## Tabular
```python
from lime.lime_tabular import LimeTabularExplainer
explainer = LimeTabularExplainer(
    training_data=X_train.values, feature_names=list(X_train.columns),
    class_names=["no", "yes"], categorical_features=cat_idx, categorical_names=cat_names,
    mode="classification", discretize_continuous=True, random_state=0)
exp = explainer.explain_instance(X_test.values[i], pipe.predict_proba, num_features=8, num_samples=5000)
exp.as_list()                    # [('income > 49953.47', 0.13), ('region=b', -0.05), ...]
exp.show_in_notebook()           # or exp.as_pyplot_figure() (the figure ran; show_in_notebook exists)
```
- `predict_fn` takes a NumPy array of raw features; wrap a full Pipeline so preprocessing is applied (convert back to DataFrame inside the wrapper if the pipeline selects columns by name: `lambda a: pipe.predict_proba(pd.DataFrame(a, columns=cols))`, ran). `num_features` above the number of available features just returns all of them (3 here). lime from PyPI imported and ran on Python 3.14.
- Categorical features must be integer-encoded in `training_data` with `categorical_features` indices.

## Text
```python
from lime.lime_text import LimeTextExplainer
exp = LimeTextExplainer(class_names=classes).explain_instance(doc, pipe.predict_proba, num_features=10)
```
Perturbs by removing words; works with any text pipeline that accepts raw strings (ran on a TF-IDF + logistic regression pipeline; top words for one post were stop words such as `be` and `to`, a reminder to check fidelity).

## Knobs that change the answer
- `kernel_width` (default `sqrt(number of columns) * 0.75`, per the docstring): defines "local". Different widths can flip signs: on a 3-feature test instance, `kernel_width=0.3` gave income -0.377, 1.3 (default) +0.134 and 10 gave +0.227, with surrogate R^2 of 0.62, 0.02 and 0.04.
- `num_samples`: more samples = more stable: the standard deviation of the three weights across 6 seeds was 0.05 to 0.06 at 200 samples and 0.01 to 0.02 at 5000.
- `discretize_continuous`: binned explanations ("age > 50") are easier to read but depend on training quartiles.

## Check stability
Run `explain_instance` several times with different `random_state`; if top features or signs change, do not trust the explanation (across 5 seeds the `age <= 31` weight flipped between -0.01 and +0.02 while `income > 49953` stayed 0.11 to 0.13). Report the local model's `exp.score` (R^2 of the surrogate) as fidelity; low values mean the linear surrogate is a poor local fit (0.018 for the default-width explanation above, so that explanation should not be trusted).

## LIME vs SHAP
| | LIME | SHAP |
|---|---|---|
| Speed | fast per instance | TreeSHAP exact and fast for trees; KernelSHAP slow |
| Consistency | can be unstable | axioms (additivity, consistency) |
| Global view | no | aggregate SHAP values |
Prefer SHAP (TreeExplainer) for tree models; LIME is useful for model-agnostic text/image explanations and quick audits.

## Gotchas
- Perturbations sample features independently: unrealistic combinations for correlated features (age 10 with 30 years of employment).
- Explanations describe the model, not causation in the world.
