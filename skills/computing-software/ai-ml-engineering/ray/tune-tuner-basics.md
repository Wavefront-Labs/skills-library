---
id: computing-software.ai-ml-engineering.ray.tune-tuner-basics
name: tune-tuner-basics
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, ray-tune, tuner, tune-report, tune-run-config]
level: practitioner
status: docs-checked
description: "Run hyperparameter tuning with ray.tune.Tuner: trainable function, TuneConfig, report metrics, ResultGrid and get_best_result."
sources:
  - https://docs.ray.io/en/latest/tune/getting-started.html
  - https://docs.ray.io/en/latest/tune/key-concepts.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tuner basics

```python
from ray import tune

def objective(config):
    for step in range(20):
        score = config["a"] * step - config["b"]
        tune.report({"score": score})                  # per-iteration metric dict

tuner = tune.Tuner(
    tune.with_resources(objective, {"cpu": 2}),
    param_space={"a": tune.uniform(0, 1), "b": tune.choice([1, 2, 3])},
    tune_config=tune.TuneConfig(metric="score", mode="max", num_samples=20,
                                max_concurrent_trials=4),
    run_config=tune.RunConfig(storage_path="<STORAGE_URI>", name="exp"),
)
results = tuner.fit()
best = results.get_best_result()
print(best.config, best.metrics["score"])
df = results.get_dataframe()
```
Resume: `tune.Tuner.restore(path, trainable=objective, resume_errored=True)` (see tune-checkpointing).

## Facts from the docs and API source
- A function trainable takes the sampled `config` dict and reports metrics with `tune.report`; the docs also show returning a final metrics dict or yielding.
- `tune.with_resources(trainable, {"cpu": 2})` or `{"gpu": 1}` sets per-trial resources; GPUs set `CUDA_VISIBLE_DEVICES` for the trial.
- `TuneConfig`: `num_samples` (trial count; with grid search the grid is repeated that many times), `max_concurrent_trials` (an upper bound on parallel trials; resources still limit it), `time_budget_s` (with `num_samples=-1`), `metric` and `mode`, `scheduler`, `search_alg`. The default scheduler is FIFO, with no early stopping.
- `fit()` returns a `ResultGrid`: `get_best_result(metric=None, mode=None, scope="last")` defaults to the `TuneConfig` metric and mode; `get_dataframe()`; `errors` and `num_errors` for failed trials; `num_terminated`.
- Ray Train trainers can be passed to `Tuner` for HPO over distributed training, with the search space under `param_space={"train_loop_config": {...}}`.

## Verify
`results.get_dataframe()` has one row per trial with config columns, and `results.errors` is empty.

## Checked
2026-11-03. Confirmed in Ray repo `tune/` docs (key concepts, trial resources, hyperparameter-optimization guide for Train) and `python/ray/tune/result_grid.py`. Fixed: draft used `train.report`/`train.RunConfig` and called `tune.report` deprecated, which is reversed in current docs. Removed: "tune.run is deprecated", `verbose=1` RunConfig tip, unconfirmed "returning a number gives one data point" gotcha, "launches as many trials as resources allow".
Method: documentation only; no commands were run.
