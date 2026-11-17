---
id: computing-software.ai-ml-engineering.model-training.population-based-training
name: population-based-training
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, population-based-training, pbt, ray-tune, hyperparameter-schedules, hpo]
level: practitioner
status: draft
description: "Run population-based training: exploit/explore cycles, perturbation intervals, checkpoint requirements, Ray Tune PBT/PB2 setup and when PBT beats static search."
sources:
  - https://docs.ray.io/en/latest/tune/examples/pbt_guide.html
  - https://arxiv.org/abs/1711.09846
  - https://docs.ray.io/en/latest/tune/api/schedulers.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Population-based training (PBT)

**Idea:** train a population of models in parallel; periodically, poor performers copy weights and hyperparameters from good ones (exploit) and then perturb those hyperparameters (explore). The result is a hyperparameter **schedule** found within one training budget.

## When it fits
- Long training runs where good hyperparameters change over time (learning rate, augmentation strength, RL entropy coefficients).
- You can run 8-32 trials concurrently.
- Not for cheap models (plain random search/ASHA is simpler) or hyperparameters that cannot change mid-training (architecture, batch size usually).

## Ray Tune setup
```python
from ray import tune
from ray.tune.schedulers import PopulationBasedTraining

pbt = PopulationBasedTraining(
    time_attr="training_iteration", perturbation_interval=4,          # iterations between exploits
    hyperparam_mutations={"lr": tune.loguniform(1e-5, 1e-2),
                          "weight_decay": [0.0, 0.01, 0.05, 0.1],
                          "mixup_alpha": tune.uniform(0.0, 0.4)},
    quantile_fraction=0.25, resample_probability=0.25)

tuner = tune.Tuner(train_fn,
    tune_config=tune.TuneConfig(scheduler=pbt, metric="val_acc", mode="max", num_samples=16),
    param_space={"lr": tune.loguniform(1e-4, 1e-2), "weight_decay": 0.01, "mixup_alpha": 0.2})
results = tuner.fit()
```

## Trainable requirements
- Report metrics every iteration and **save/restore checkpoints** (model, optimizer, step) via `ray.tune.report(..., checkpoint=...)` and `tune.get_checkpoint()`; exploitation is implemented by loading another trial's checkpoint.
- Read hyperparameters from `config` each time you (re)start, and apply new values to the optimizer (`for g in opt.param_groups: g["lr"] = config["lr"]`).

## PB2
`PB2` uses a Gaussian-process bandit instead of random perturbations: better with small populations (4-8).

## Pitfalls
- Greedy exploitation on noisy metrics copies lucky trials; use smoothed metrics and not-too-short perturbation intervals.
- The output is a schedule; to reproduce, replay the logged hyperparameter history of the best trial (`results.get_best_result().metrics_dataframe`).

## Verify
- [ ] Compare the best PBT trial with the best trial of a random search of equal total compute.
