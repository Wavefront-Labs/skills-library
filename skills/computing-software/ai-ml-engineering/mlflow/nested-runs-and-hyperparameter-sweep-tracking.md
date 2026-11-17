---
id: computing-software.ai-ml-engineering.mlflow.nested-runs-and-hyperparameter-sweep-tracking
name: nested-runs-and-hyperparameter-sweep-tracking
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, nested-runs, hyperparameter-tuning, optuna, hyperopt, autologging, parent-run, child-run, experiment-tracking, parallel-coordinates, sweep-comparison, mlflow-ui]
level: practitioner
status: gated
description: "Track hyperparameter sweeps in MLflow with nested parent/child runs so hundreds of trials stay comparable and queryable, instead of flattening into an unsearchable experiment."
sources:
  - https://mlflow.org/docs/latest/tracking.html#organizing-runs-in-experiments
  - https://optuna.readthedocs.io/en/stable/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tracking hyperparameter sweeps in MLflow: nested runs done right

**Goal:** run a sweep of dozens to hundreds of trials (via Optuna, Hyperopt, Ray Tune, or a hand-rolled loop) and end up with a comparable, queryable set of MLflow runs — not hundreds of flat, indistinguishable entries or one run whose metrics got overwritten by the next trial.

## 1. The nested-run pattern
```python
with mlflow.start_run(run_name="sweep") as parent:
    for trial_params in search_space:
        with mlflow.start_run(run_name=f"trial-{trial_params['id']}", nested=True):
            mlflow.log_params(trial_params)
            model = train(trial_params)
            metrics = evaluate(model)
            mlflow.log_metrics(metrics)
    # after all trials: log the winner's params/metrics on the parent for easy top-level comparison
    best = max(results, key=lambda r: r["val_auc"])
    mlflow.log_params({"best_" + k: v for k, v in best["params"].items()})
    mlflow.log_metrics({"best_" + k: v for k, v in best["metrics"].items()})
```
- (Optuna/Hyperopt/Ray integrations were not run here (gated: unconfirmed, source is paywalled or blocked); the manual loop was.)
- `nested=True` is what makes a child run show up grouped under its parent in the MLflow UI (indented) instead of as a sibling at the top level — forgetting it produces hundreds of flat, unrelated-looking runs in the experiment list with no way to tell which sweep they belonged to.
- Log the **search space definition itself** (as a parameter or an artifact — the Optuna/Hyperopt config) on the parent run, not just the per-trial sampled values — six months later, "what were we even searching over" is unanswerable from child runs alone.

## 2. Autologging interacting with manual nested runs
- `mlflow.autolog()` (or framework-specific `mlflow.sklearn.autolog()`, `mlflow.pytorch.autolog()`) automatically starts a run if none is active — inside a sweep loop, call `mlflow.start_run(nested=True)` explicitly around each trial **before** the training call, so autolog logs into the trial's child run rather than creating its own top-level run or logging into whatever run happened to be active.
- Autologging a library that itself loops internally (e.g. a cross-validation call that fits multiple folds) can create more runs than you expect per trial — check the actual run count after a small test sweep (3–5 trials). In MLflow 3.17.1 with `mlflow.sklearn.autolog()` a parent plus two nested trials, each calling `fit` and `cross_val_score(cv=3)`, produced exactly 3 runs (tested), and a bare `fit` with no active run created a new top-level run before launching the full sweep, so you're not surprised by 10x the expected run count in the tracking server.

## 3. Making hundreds of trials actually comparable afterward
- Log a **consistent metric name and consistent params schema** across all trials in a sweep — if one trial's code path logs `val_auc` and a later code change logs `val_auc_roc`, the MLflow UI's comparison table and `mlflow.search_runs()` filtering silently can't group them, and you lose half your sweep from any later analysis without an error telling you why.
- Use `mlflow.search_runs(experiment_ids=[...], filter_string="tags.sweep_id = '...'")` (a tag, matching the tagging step below; tested: children carry the `mlflow.parentRunId` tag and the tag filter returned all 3 trials, while a `params.` filter only matched the one run that logged the id as a param) to pull a sweep's runs into a DataFrame for parallel-coordinate plots or custom analysis — the MLflow UI's built-in comparison view (select runs → "Compare") is fine for a quick look but gets hard to read with hundreds of trials (gated: unconfirmed, source is paywalled or blocked).
- Tag the sweep (`mlflow.set_tag("sweep_id", uuid)`) on every child run at trial-start so you can retrieve exactly "runs belonging to sweep X" later — relying on timestamp ranges or run-name string matching to reconstruct which runs belonged together is fragile once multiple sweeps run concurrently or overlap in time.
- For an early-stopped sweep (Optuna pruning, Hyperopt's `STATUS_FAIL`/early stop), explicitly log the trial's final status (`mlflow.set_tag("trial_status", "pruned")`) — otherwise a pruned trial with a partial/undertrained metric looks identical in the comparison view to a trial that ran to completion and genuinely underperformed, and you'll misread the sweep's results.

## Verify
- [ ] Every trial run uses `nested=True` and appears grouped under its sweep's parent run in the UI.
- [ ] The search space/sweep config is logged once (on the parent), not only implicitly via the scatter of child-run params.
- [ ] Autologging confirmed (via a small test sweep) to log into the intended child run, not create extra top-level runs.
- [ ] Metric and parameter names are consistent across all trials in the sweep — checked with `search_runs`, not assumed.
- [ ] Every trial is tagged with a sweep id, retrievable independent of timestamp.
- [ ] Early-stopped/pruned trials are tagged distinctly from fully-trained trials before comparing results.
