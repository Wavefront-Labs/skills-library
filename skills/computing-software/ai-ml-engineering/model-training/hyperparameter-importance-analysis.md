---
id: computing-software.ai-ml-engineering.model-training.hyperparameter-importance-analysis
name: hyperparameter-importance-analysis
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, hyperparameter-importance, fanova, optuna, parallel-coordinates, hpo-analysis, sensitivity]
level: practitioner
status: draft
description: "Find which hyperparameters matter after a search with Optuna importance (fANOVA, PED-ANOVA), slice and parallel coordinate plots, then shrink the search space for the next round."
sources:
  - https://optuna.readthedocs.io/en/stable/reference/importance.html
  - https://proceedings.mlr.press/v32/hutter14.html
  - https://optuna.readthedocs.io/en/stable/reference/visualization/index.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Hyperparameter importance analysis

After 50-200 trials, ask which hyperparameters actually moved the metric. Usually 1-3 dominate (Hutter et al. 2014, fANOVA): tune those, fix the rest.

## Optuna
```python
import optuna
from optuna.importance import get_param_importances, FanovaImportanceEvaluator, PedAnovaImportanceEvaluator
imp = get_param_importances(study, evaluator=FanovaImportanceEvaluator(seed=0))
# {'learning_rate': 0.62, 'num_leaves': 0.21, 'subsample': 0.08, ...}
optuna.visualization.plot_param_importances(study)
optuna.visualization.plot_slice(study, params=["learning_rate", "num_leaves"])
optuna.visualization.plot_contour(study, params=["learning_rate", "num_leaves"])
optuna.visualization.plot_parallel_coordinate(study)
```
- **fANOVA**: fits a random forest on (params -> objective) and decomposes variance into per-parameter and interaction contributions. Default evaluator.
- **PED-ANOVA**: importance within the top-performing quantile of trials (`PedAnovaImportanceEvaluator(baseline_quantile=0.1)`); answers "what matters among good configurations".
- **MeanDecreaseImpurity**: faster, cruder.
- For multi-objective studies pass `target=lambda t: t.values[0]`.

## Reading plots
- Slice plot: objective vs one parameter across trials. A clear trend or optimum band = important; flat cloud = unimportant (fix it to a sensible default).
- Contour: interactions (e.g. learning rate optimum shifts with batch size).
- Parallel coordinates: color by objective; see which value ranges the best trials share.

## Caveats
- Importance is relative to the **search space you chose**. A parameter with a narrow range looks unimportant. Widen ranges before concluding.
- TPE/BO concentrate trials near good regions, biasing estimates; random-search trials give cleaner importance estimates. A few dozen random trials at the start (`n_startup_trials`) help.
- Noisy objectives (seed variance) inflate the noise floor: importance of every parameter may be low.
- Conditional parameters (only present for some choices) need care; fANOVA in Optuna handles them only partially.

## Next round
1. Fix unimportant parameters at good defaults.
2. Narrow ranges of important ones to the region of the top 10% trials (with margin).
3. Re-run with multiple seeds for the finalists.

## Other tools
W&B Sweeps parameter-importance panel (correlation + random-forest importance), Ray Tune with `ExperimentAnalysis.dataframe()` then your own fANOVA (`fanova` package), DeepCAVE for HPO run analysis.
