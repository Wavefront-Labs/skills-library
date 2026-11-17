---
id: computing-software.ai-ml-engineering.model-training.sagemaker-debugger-built-in-rules
name: sagemaker-debugger-built-in-rules
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, sagemaker-debugger, built-in-rules, vanishing-gradient, training-monitoring, aws-sagemaker, smdebug]
level: practitioner
status: draft
description: "Monitor SageMaker training jobs with Debugger built-in rules (vanishing gradient, overfit, loss not decreasing, overtraining) and actions to stop jobs, plus tensor analysis."
sources:
  - https://docs.aws.amazon.com/sagemaker/latest/dg/train-debugger.html
  - https://docs.aws.amazon.com/sagemaker/latest/dg/debugger-built-in-rules.html
  - https://docs.aws.amazon.com/sagemaker/latest/dg/debugger-built-in-actions.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# SageMaker Debugger built-in rules

SageMaker Debugger saves tensors (losses, weights, gradients, activations) from training jobs to S3 and evaluates **rules** on them in separate processing containers while training runs.

## Attach rules to an estimator
```python
from sagemaker.debugger import Rule, rule_configs, DebuggerHookConfig, CollectionConfig
actions = rule_configs.ActionList(rule_configs.StopTraining(), rule_configs.Email("ml-team@example.com"))
rules = [
    Rule.sagemaker(rule_configs.loss_not_decreasing(), actions=actions),
    Rule.sagemaker(rule_configs.vanishing_gradient()),
    Rule.sagemaker(rule_configs.exploding_tensor()),
    Rule.sagemaker(rule_configs.overfit(), rule_parameters={"patience_validation": "5"}),
    Rule.sagemaker(rule_configs.overtraining()),
    Rule.sagemaker(rule_configs.poor_weight_initialization()),
]
est = PyTorch(entry_point="train.py", ..., rules=rules,
              debugger_hook_config=DebuggerHookConfig(s3_output_path="s3://bucket/debug",
                  collection_configs=[CollectionConfig("gradients", parameters={"save_interval": "100"})]))
est.fit(inputs)
```
- Rules run on separate instances (default ml.t3.medium for many rules) and are billed separately; the free-of-charge built-in rules list is in the docs.
- Status: `est.latest_training_job.rule_job_summary()` shows `IssuesFound` / `NoIssuesFound` per rule; also visible in Studio and CloudWatch Events.

## Common built-in rules
| Rule | Fires when |
|---|---|
| `loss_not_decreasing` | loss fails to drop by a percentage over a window |
| `overfit` | validation loss rises while training loss falls |
| `overtraining` | no improvement for patience steps |
| `vanishing_gradient` / `exploding_tensor` | gradient magnitudes below threshold / NaN or huge values |
| `poor_weight_initialization` | activation variance problems at start |
| `dead_relu` | high fraction of inactive ReLUs |
| `class_imbalance`, `tensor_variance`, `weight_update_ratio` | as named |
Profiler rules (`LowGPUUtilization`, `CPUBottleneck`, `IOBottleneck`) are a separate set for system metrics.

## Actions
`StopTraining()` ends a failing job early (saves cost on doomed runs); `Email`/`SMS` notify through SNS. Rules with actions should have tuned parameters to avoid stopping healthy jobs early (e.g. warm-up phases with flat loss).

## Analyse tensors yourself
```python
from smdebug.trials import create_trial
trial = create_trial(est.latest_job_debugger_artifacts_path())
trial.tensor_names(collection="gradients"); trial.tensor("CrossEntropyLoss_output_0").values()
```

## Notes
- Framework support: TensorFlow, PyTorch, XGBoost in AWS deep learning containers; custom containers need the smdebug hook (`smd.Hook.create_from_json_file()`).
- Debugger tensor collection is in maintenance mode in newer SageMaker versions; the profiler moved to SageMaker Profiler. Check current docs; for new projects, W&B/TensorBoard gradient logging plus custom CloudWatch alarms is a common alternative.
