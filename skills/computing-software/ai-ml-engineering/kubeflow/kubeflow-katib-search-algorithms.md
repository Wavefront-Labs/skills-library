---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-katib-search-algorithms
name: kubeflow-katib-search-algorithms
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [algorithms, bayesian-optimization, hyperband, tpe, cmaes, pbt, grid-search, random-search]
level: practitioner
status: docs-checked
description: "Katib hyperparameter search algorithms by name (grid, random, bayesianoptimization, hyperband, tpe, multivariate-tpe, cmaes, sobol, pbt), their frameworks and settings."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/katib/user-guides/hp-tuning/configure-algorithm.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Katib search algorithms

Set the algorithm name in `.spec.algorithm.algorithmName` with `algorithmSettings` as needed.

- `grid`: exhaustive; best when variables are discrete and few. Uses Optuna. Setting: `random_state`.
- `random`: for many discrete variables or costly evaluations; Hyperopt, Goptuna or Optuna. Prefer quasi-random (`sobol`) when many continuous variables.
- `bayesianoptimization`: Gaussian process regression via Scikit-Optimize. Suitable for low dimensions and slow evaluations. Settings: `base_estimator` (GP, RF, ET, GBRT), `n_initial_points` (10), `acq_func` (gp_hedge), `acq_optimizer` (sampling or lbfgs, default auto), `random_state`.
- `hyperband`: relies on early stopping to evaluate more configurations quickly.
- `tpe`: Tree of Parzen Estimators. Settings: `n_EI_candidates`, `gamma` (0 to 1), `prior_weight` (above 0), `random_state`.
- `multivariate-tpe`: Optuna; models dependencies among parameters. Settings: `n_ei_candidates`, `n_startup_trials`, `random_state`.
- `cmaes`: continuous spaces; settings `sigma`, `restart_strategy` (none, ipop, bipop).
- `sobol`: low-discrepancy sequence via Goptuna.
- `pbt`: population based training. Needs a PVC with ReadWriteMany access and `resumePolicy: FromVolume`. Settings: `suggestion_trial_dir`, `n_population`, `resample_probability`, `truncation_threshold`.

Custom algorithm: Katib uses an ask-and-tell pattern. Implement the Suggestion gRPC service from `api.proto` (a `GetSuggestions` method, optional `ValidateAlgorithmSettings`), serve it on port 6789, build an image, and add an entry under `runtime.suggestions` in `katib-config` with `algorithmName` and `image`.

## Checked

2026-11-08. Confirmed against the HP tuning algorithms page: algorithm names, frameworks, settings and defaults, the PBT requirements and the custom algorithm steps. Added the acq_optimizer values.
Method: docs-only read of cited pages, 2026-11-08
