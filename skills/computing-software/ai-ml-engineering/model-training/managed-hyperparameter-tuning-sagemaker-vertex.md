---
id: computing-software.ai-ml-engineering.model-training.managed-hyperparameter-tuning-sagemaker-vertex
name: managed-hyperparameter-tuning-sagemaker-vertex
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, hyperparameter-tuning, sagemaker-automatic-model-tuning, vertex-vizier, hyperparametertuner, warm-start, cloud-ml]
level: practitioner
status: draft
description: "Run managed HPO on SageMaker Automatic Model Tuning and Vertex AI: ranges and scaling, metric reporting, strategies, parallelism trade-offs and warm starts."
sources:
  - https://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning.html
  - https://sagemaker.readthedocs.io/en/stable/api/training/tuner.html
  - https://cloud.google.com/vertex-ai/docs/training/hyperparameter-tuning-overview
  - https://cloud.google.com/vertex-ai/docs/training/using-hyperparameter-tuning
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Managed hyperparameter tuning: SageMaker AMT and Vertex AI

**Goal:** run a tuning job where the cloud schedules trials, collects the metric and suggests the next point - without writing your own scheduler.

## SageMaker Automatic Model Tuning
```python
from sagemaker.tuner import HyperparameterTuner, ContinuousParameter, IntegerParameter, CategoricalParameter
tuner = HyperparameterTuner(
    estimator=est,                                    # any SageMaker Estimator
    objective_metric_name="validation:auc",
    objective_type="Maximize",
    metric_definitions=[{"Name": "validation:auc", "Regex": "val_auc=([0-9\\.]+)"}],   # for script mode
    hyperparameter_ranges={
        "lr": ContinuousParameter(1e-5, 1e-2, scaling_type="Logarithmic"),
        "max_depth": IntegerParameter(3, 10),
        "optimizer": CategoricalParameter(["adam", "sgd"]),
    },
    strategy="Bayesian",              # Random | Hyperband | Grid
    max_jobs=40, max_parallel_jobs=4,
    early_stopping_type="Auto",
)
tuner.fit({"train": s3_train, "validation": s3_val})
tuner.best_training_job()
```
- Script mode: the metric reaches AMT only through the regex over CloudWatch logs - print it exactly in that format. Built-in algorithms publish their own metric names.
- `Hyperband` strategy stops weak trials early using intermediate metrics; your script must emit the metric each epoch.
- **Warm start**: `warm_start_config=WarmStartConfig(WarmStartTypes.IDENTICAL_DATA_AND_ALGORITHM, parents={"old-tuning-job"})` reuses previous results; `TRANSFER_LEARNING` when data or algorithm changed.

## Vertex AI hyperparameter tuning (Vizier)
```python
from google.cloud.aiplatform import hyperparameter_tuning as hpt
job = aiplatform.HyperparameterTuningJob(
    display_name="xgb-hpt", custom_job=custom_job,
    metric_spec={"auc": "maximize"},
    parameter_spec={"lr": hpt.DoubleParameterSpec(min=1e-5, max=1e-2, scale="log"),
                    "depth": hpt.IntegerParameterSpec(min=3, max=10, scale="linear")},
    max_trial_count=40, parallel_trial_count=4,
)
job.run()
```
Report the metric from the training code:
```python
import hypertune
hypertune.HyperTune().report_hyperparameter_tuning_metric(hyperparameter_metric_tag="auc", metric_value=auc, global_step=epoch)
```
Trial hyperparameters arrive as command-line args (`--lr=...`); parse them with argparse.

## Choosing parallelism
Bayesian optimisation learns from completed trials. With `max_parallel_jobs` equal to `max_jobs`, it degrades to random search. A ratio of ~1:10 (4 parallel of 40) keeps most of the benefit; raise parallelism only when wall-clock matters more than trial efficiency.

## Gotchas
- Log-scale anything spanning orders of magnitude (LR, regularisation); linear scaling wastes most trials at the top of the range.
- The objective is computed on whatever split your script reports. Report a validation metric, never test.
- Each trial is a full job with its own container start and data download; for small models, overhead dominates. Use in-process tuning (Optuna) inside a single job instead.
- Trials that crash count against `max_jobs`; test the training script on one trial first.

## Verify
- [ ] One manual trial runs and emits the metric in the expected format.
- [ ] Best trial re-trained and evaluated on a held-out test set.
- [ ] Search ranges not hit at the edges by the best trials (otherwise widen and rerun with warm start).
