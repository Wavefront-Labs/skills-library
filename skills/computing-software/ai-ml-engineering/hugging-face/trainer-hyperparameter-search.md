---
id: computing-software.ai-ml-engineering.hugging-face.trainer-hyperparameter-search
name: trainer-hyperparameter-search
category: computing-software
field: ai-ml-engineering
product: hugging-face
tags: [hugging-face, trainer-hyperparameter-search, optuna, ray-tune, model-init, hyperparameter-tuning, transformers]
level: practitioner
status: gated
description: "Tune Transformers models with Trainer.hyperparameter_search: model_init, Optuna or Ray Tune backends, search spaces, objectives, pruning and reusing the best run."
sources:
  - https://huggingface.co/docs/transformers/hpo_train
  - https://huggingface.co/docs/transformers/main_classes/trainer#transformers.Trainer.hyperparameter_search
  - https://optuna.readthedocs.io/en/stable/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trainer.hyperparameter_search

## Setup: model_init instead of model
Each trial needs a fresh model, so pass a factory:
```python
def model_init(trial):
    return AutoModelForSequenceClassification.from_pretrained(ckpt, num_labels=2)
trainer = Trainer(model_init=model_init, args=TrainingArguments("hpo", eval_strategy="epoch",
                  save_strategy="no", report_to="none", fp16=True),   # fp16 needs a GPU; drop it on CPU
                  train_dataset=train_ds, eval_dataset=val_ds, processing_class=tokenizer,
                  data_collator=collator, compute_metrics=compute_metrics)
```

## Optuna backend
```python
def space(trial):
    return {"learning_rate": trial.suggest_float("learning_rate", 1e-5, 1e-4, log=True),
            "per_device_train_batch_size": trial.suggest_categorical("per_device_train_batch_size", [16, 32]),
            "num_train_epochs": trial.suggest_int("num_train_epochs", 2, 4),
            "weight_decay": trial.suggest_float("weight_decay", 0.0, 0.1),
            "warmup_steps": trial.suggest_float("warmup_steps", 0.0, 0.1)}   # float < 1 = fraction of steps
best = trainer.hyperparameter_search(direction="maximize", backend="optuna", hp_space=space, n_trials=20,
                                     compute_objective=lambda m: m["eval_f1"])   # ran with n_trials=2 on a tiny BERT (CPU)
best.hyperparameters, best.objective
```
- Keys must be `TrainingArguments` field names (or handled in `model_init(trial)` for model hyperparameters like dropout: read `trial.params` there). Trap on transformers 5.x: `warmup_ratio` is no longer a field, yet a search over it ran without error (the value is just set as an unused attribute), so the tuned value does nothing. Check with `hasattr(args, key)`.
- Default objective (`default_compute_objective`) is the eval loss if no metrics function is given, otherwise the sum of all metrics except `epoch` and the speed metrics (ran: `{eval_f1: 0.9, eval_acc: 0.8}` gives 1.7); always set `compute_objective` and matching `direction`.
- Pruning: Optuna prunes using intermediate evaluations reported each eval step; pass `pruner=optuna.pruners.MedianPruner()` as a keyword argument to `hyperparameter_search` (accepted in a 2-trial run on optuna 5.0.0).

## Ray Tune backend
`backend="ray"`, `hp_space=lambda _: {"learning_rate": tune.loguniform(1e-5, 1e-4)}`, `scheduler=ASHAScheduler(metric="objective", mode="max")`, `resources_per_trial={"gpu": 1}`. Use for multi-GPU parallel trials across a cluster (Ray was not installed or run here) (gated: unconfirmed, source is paywalled or blocked). The backends enum in transformers 5.20.2 is `optuna`, `ray` and `wandb`; `sigopt` is gone.

## Use the best result
```python
for k, v in best.hyperparameters.items(): setattr(trainer.args, k, v)
trainer.train()                      # (ran: setattr on trainer.args then train) final run with the best settings, then evaluate on the test set
```

## Practical advice
- Search LR first (log scale), then batch size/epochs; for fine-tuning BERT-like models, 1e-5 to 5e-5 and 2-4 epochs is the usual range.
- Subsample the training set for early trials, confirm on full data.
- Turn off checkpoint saving (`save_strategy="no"`) or disk fills up across trials.
- Seed variance matters: re-run the top 2-3 configs with several seeds before declaring a winner.
