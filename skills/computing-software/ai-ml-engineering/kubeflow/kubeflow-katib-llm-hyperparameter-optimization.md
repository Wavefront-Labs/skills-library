---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-katib-llm-hyperparameter-optimization
name: kubeflow-katib-llm-hyperparameter-optimization
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [llm, huggingface, fine-tuning, lora, trainer-resources]
level: advanced
status: docs-checked
description: "Tune LLM fine-tuning hyperparameters with Katib (alpha): HuggingFace and S3 providers, katib.search parameters, TrainerResources and supported objective metric."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/katib/user-guides/llm-hp-optimization.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Katib llm hyperparameter optimization

Alpha feature. Prerequisites: Training Operator control plane (install it before Katib so namespace labels and the PyTorchJob CRD are set up), Katib control plane, and a Katib Python SDK with LLM support. A custom objective function does not support distributed training and does not need the Training Operator.

Load models and datasets through the storage initializer: HuggingFace (`HuggingFaceModelParams`, `HuggingFaceDatasetParams`, `HuggingFaceTrainerParams` from `kubeflow.storage_initializer.hugging_face`) or S3-compatible storage (`S3DatasetParams`).

Only `training_parameters` and `lora_config` can be tuned; other fields are static. Define search spaces with `katib.search.double(min, max, step)`, `katib.search.int(min, max, step)` and `katib.search.categorical(list)`:

```python
trainer_params = HuggingFaceTrainerParams(
    training_parameters=TrainingArguments(
        output_dir="results",
        learning_rate=katib.search.double(min=1e-05, max=5e-05),
        num_train_epochs=3),
    lora_config=LoraConfig(r=katib.search.int(min=8, max=32), lora_alpha=16),
)
```

`tune()` accepts `model_provider_parameters`, `dataset_provider_parameters`, `trainer_parameters`, `storage_config`, `algorithm_name`, `objective_metric_name`, `max_trial_count`, `parallel_trial_count`, `resources_per_trial` and more.

Rules: the only supported objective metric is `train_loss`. With external models you must set `resources_per_trial` as `katib.TrainerResources(num_workers, num_procs_per_worker, resources_per_worker={...})`; `num_workers` above 1 enables distributed training through PyTorchJob.

## Checked

Confirmed the alpha status, prerequisites and install order, the provider classes, the tunable fields, the katib.search functions, the tune() parameter names, the train_loss restriction and the TrainerResources rule. Nothing removed.

Method: docs-checked 2026-11-09 against the raw kubeflow/website Katib llm-hp-optimization.md page, read in full.
