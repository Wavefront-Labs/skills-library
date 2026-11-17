---
id: computing-software.ai-ml-engineering.mlflow.mlflow-models-evaluate-classical
name: mlflow-models-evaluate-classical
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, mlflow-models-evaluate, model-evaluation, evaluate, shap, baseline-comparison, validation-thresholds]
level: practitioner
status: verified
description: "Evaluate classical models with mlflow.models.evaluate: model types, default metrics and plots, custom metrics, SHAP explainer artifacts and threshold gates vs a baseline."
sources:
  - https://mlflow.org/docs/latest/ml/evaluation/
  - https://mlflow.org/docs/latest/api_reference/python_api/mlflow.models.html#mlflow.models.evaluate
  - https://mlflow.org/docs/latest/ml/evaluation/model-eval/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# mlflow.models.evaluate for classical models

**What it does:** runs a model on an evaluation dataset and logs standard metrics, plots (confusion matrix, ROC, PR, calibration, lift) and optional SHAP explanations to a run.

## Usage
```python
import mlflow
eval_df = X_test.assign(label=y_test)
with mlflow.start_run():
    info = mlflow.sklearn.log_model(model, name="model", input_example=X_test.head())
    result = mlflow.models.evaluate(
        info.model_uri, eval_df, targets="label",
        model_type="classifier",                    # or "regressor"
        evaluators=["default"],
        evaluator_config={"default": {"log_model_explainability": True,   # keyed by evaluator name
                                      "explainability_nsamples": 500, "pos_label": 1}})
print(result.metrics["roc_auc"], list(result.artifacts))
```
Passing a flat `evaluator_config` together with `evaluators=["default"]` raises `MlflowException: ... evaluator_config must be a dict containing mapping from evaluator name to individual evaluator config dict` (tested on MLflow 3.17.1). SHAP plots need the `shap` package installed (with it, the artifacts were roc_curve_plot, precision_recall_curve_plot, lift_curve_plot, calibration_curve_plot, confusion_matrix and three shap plots).

Static predictions instead of a model: omit the model and pass `data=df, predictions="pred_col", targets="label"` (evaluate outputs from any system; tested, returned `accuracy_score`).

## Custom metrics
```python
from mlflow.models import make_metric
def expected_cost(eval_df, _builtin_metrics):
    fp = ((eval_df["prediction"] == 1) & (eval_df["target"] == 0)).sum()
    fn = ((eval_df["prediction"] == 0) & (eval_df["target"] == 1)).sum()
    return 5 * fp + 100 * fn
cost = make_metric(eval_fn=expected_cost, greater_is_better=False, name="expected_cost")
mlflow.models.evaluate(..., extra_metrics=[cost])
```

## Gates vs a baseline
In MLflow 3.17.1 `mlflow.models.evaluate` no longer has `baseline_model` or `validation_thresholds` parameters (checked its signature). Compare two results with `mlflow.validate_evaluation_results(candidate_result=..., baseline_result=..., validation_thresholds={"roc_auc": MetricThreshold(threshold=0.85, min_absolute_change=0.005, greater_is_better=True)})`, with `from mlflow.models import MetricThreshold`. `greater_is_better` is required and `min_absolute_change` must be positive (a 0 value raised `MetricThresholdClassException`). A failing candidate raised `ModelValidationFailedException`, importable from `mlflow.models.evaluation.validation` (it is not exported from `mlflow.models`). Use this in CI before registering or promoting a version.

## Notes
- Large eval sets with SHAP are slow; subsample explainability.
- GenAI evaluation moved to `mlflow.genai.evaluate` with scorers; use `mlflow.models.evaluate` for tabular/classical models.

## Verify
- [ ] Run page shows metrics and plots; failing thresholds raise `ModelValidationFailedException` in a deliberately bad test (a label-flipped dataset gave ROC AUC 0.03 and failed the 0.85 threshold).
