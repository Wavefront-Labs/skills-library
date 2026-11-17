---
id: computing-software.ai-ml-engineering.model-training.hyperparameter-search-strategies
name: hyperparameter-search-strategies
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [hyperparameter-tuning, bayesian-optimization, optuna, grid-search, random-search, hyperband, early-stopping, learning-rate-search, search-space-design, tpe, successive-halving]
level: advanced
status: gated
description: "Choose and run a hyperparameter search efficiently: why random beats grid, when Bayesian/TPE methods pay off, and using early stopping (Hyperband/ASHA) to cut wasted compute."
sources:
  - https://arxiv.org/abs/1603.06560
  - https://optuna.readthedocs.io/en/stable/
  - https://jmlr.org/papers/v13/bergstra12a.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hyperparameter search strategies — spending compute where it helps

**Goal:** find good hyperparameters without either wasting a cluster-week on an exhaustive grid or stopping a lucky-but-unrepresentative single run.

## 1. Why grid search is usually the wrong default
- **Grid search scales exponentially with dimensions** and wastes evaluations on unimportant parameters — if only 2 of your 6 hyperparameters actually matter for the metric, grid search still spends equal budget exploring the other 4, because every combination of all 6 gets a point. Bergstra & Bengio (2012, JMLR 13) showed **random search finds comparably good configurations with far fewer trials** (paper not re-read this session (gated: unconfirmed, source is paywalled or blocked)) precisely because it doesn't waste samples on a full Cartesian product — it covers each dimension's range more efficiently when most dimensions don't matter much.
- Use grid search only when the space is small (2–3 parameters, a handful of values each) and you want the full picture for a paper/report, not for genuine optimization under a compute budget.

## 2. Picking a method by budget and space
- **Random search**: the right default when you have a modest budget (tens of trials) and little prior belief about which regions of the space are good — simple, trivially parallelizable, no coordination needed between trials.
- **Bayesian optimization / TPE** (Optuna's default sampler, confirmed: `create_study().sampler` is `TPESampler`; Hyperopt not run (gated: unconfirmed, source is paywalled or blocked)): builds a probabilistic model of which regions of the space look promising based on completed trials, and samples the next trial accordingly — pays off once you have enough budget ("typically 20+ trials" is a rule of thumb (gated: unconfirmed, source is paywalled or blocked)) for the model to learn something useful, and the search space isn't trivially small. Sequential by nature (each trial informs the next), which limits parallelism unless using batch-suggestion variants.
- **Hyperband / ASHA (successive halving)**: for trials that are themselves iterative (training runs with a per-epoch validation metric), allocate a small budget to many configurations, kill the worst-performing fraction early, and give the survivors more budget — dramatically cuts wasted compute versus running every trial to completion, because most bad configurations reveal themselves early (within the first 10-20% of training) and don't need a full run to be ruled out. Optuna implements this as `optuna.pruners.HyperbandPruner` and `SuccessiveHalvingPruner` (both exist; a 40-trial TPE + `HyperbandPruner` run pruned 25 trials and found lr = 0.00102 for an objective minimised at 0.001); Ray Tune's ASHA scheduler was not checked (gated: unconfirmed, source is paywalled or blocked).
- Combine: **TPE/Bayesian sampling + Hyperband pruning** (Optuna supports both together) gets the sample-efficiency of Bayesian search and the early-stopping savings of Hyperband in one search — this is the practical default for anything beyond a toy sweep.

## 3. Search space design — the part people under-invest in
- **Use log-uniform scale for learning rate, weight decay, and other multiplicative-effect parameters** (`trial.suggest_float("lr", 1e-5, 1e-1, log=True)` inside the objective; there is no module-level `optuna.suggest_float`, tested) — a linear-scale search over `[1e-5, 1e-1]` puts about 90% of its samples (0.897 in a 10,000-draw simulation) in the `[1e-2, 1e-1]` decade; log-scale spreads samples evenly across orders of magnitude, which is where learning rate's effect actually lives.
- Start with a **wide range** and narrow based on a first cheap sweep's results, rather than guessing a narrow range up front — a range that's too narrow silently caps the search below the true optimum with no warning, since every trial just converges to one edge of the range and nothing in the output flags that as suspicious. Check whether the best trials cluster at a range boundary; if so, widen and re-search.
- Correlated hyperparameters (batch size and learning rate; model depth and dropout) searched independently waste trials in the "good LR for small batch, now sampled with a huge batch" dead zones — either search the ratio/derived quantity directly, or use conditional search spaces that scale one parameter's range based on another's sampled value.
- Fix everything you're not tuning (seed for weight init if comparing configs fairly — or explicitly average over seeds if you're not, and never mix the two: comparing seeded-once results across configs without accounting for seed variance misattributes noise to the hyperparameter).

## 4. Common mistakes
- Tuning hyperparameters against the **test set** instead of a validation set (or against the same validation set repeatedly used for the final reported number) — this is leakage; the final reported metric needs a held-out set the search never touched, same discipline as in computing-software.ai-ml-engineering.model-training.data-splits-and-evaluation.
- Not logging every trial's full config and result (tie into computing-software.ai-ml-engineering.mlflow.nested-runs-and-hyperparameter-sweep-tracking) — without this, you can't tell afterward whether the search actually converged or you got lucky on trial 3.
- Re-running the exact same search after a code change and assuming results are comparable — a preprocessing or architecture change shifts the whole landscape; old best-hyperparameters are a reasonable starting point, not a guaranteed-still-optimal one.

## Verify
- [ ] Search method matches budget and space size (random for small budgets/few params, TPE+Hyperband for anything larger and iterative).
- [ ] Learning-rate-like parameters searched on a log scale; range widened if best trials cluster at a boundary.
- [ ] Final reported metric comes from a held-out set the search never touched.
- [ ] Every trial's config and result is logged somewhere queryable, not just the winner.
- [ ] Seed variance across repeated runs of the same config is known, so it isn't misread as a hyperparameter effect.
