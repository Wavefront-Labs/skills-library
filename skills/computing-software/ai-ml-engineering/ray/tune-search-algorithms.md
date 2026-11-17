---
id: computing-software.ai-ml-engineering.ray.tune-search-algorithms
name: tune-search-algorithms
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, tune-searcher, optuna-search, bayesopt, search-alg]
level: practitioner
status: docs-checked
description: "Plug Optuna, HyperOpt, BayesOpt or Ax searchers into Ray Tune, wrap with ConcurrencyLimiter, and combine with schedulers."
sources:
  - https://docs.ray.io/en/latest/tune/api/suggestion.html
  - https://docs.ray.io/en/latest/tune/key-concepts.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Search algorithms

```python
from ray import tune
from ray.tune.search import ConcurrencyLimiter
from ray.tune.search.optuna import OptunaSearch

algo = OptunaSearch()                                    # needs the optuna package
algo = ConcurrencyLimiter(algo, max_concurrent=4)        # for algorithms that parallelize poorly
tuner = tune.Tuner(
    objective,
    param_space={"lr": tune.loguniform(1e-4, 1e-2), "act": tune.choice(["relu", "gelu"])},
    tune_config=tune.TuneConfig(search_alg=algo, num_samples=100, metric="loss", mode="min"),
)
results = tuner.fit()
```

## Facts from the docs and API source
- Search algorithms wrap open-source libraries: `AxSearch`, `BayesOptSearch`, `TuneBOHB`, `HEBOSearch`, `HyperOptSearch`, `NevergradSearch`, `OptunaSearch`, `ZOOptSearch`. Tune converts the `param_space` to each library's format in most cases.
- The default (no `search_alg`) is `BasicVariantGenerator`: random and grid search.
- `TuneBOHB` should be paired with `HyperBandForBOHB` and needs `hpbandster` and `ConfigSpace` installed.
- `ConcurrencyLimiter(searcher, max_concurrent, batch=False)` limits concurrent suggestions; use it when an algorithm (such as naive Bayesian optimization) does not parallelize well.
- `OptunaSearch` takes `points_to_evaluate` (initial configs to run), `evaluated_rewards` (their known results, to skip re-running them) and `seed`. It rejects `seed` when you pass your own sampler; seed that sampler directly.
- `Repeater(search_alg, repeat)` runs each suggested config several times and averages the metric. The docs recommend not combining it with a trial scheduler.
- Save and restore: `search_alg.save(path)` / `restore(path)` on algorithms that implement them; Tune also saves searcher state in the experiment folder, and a second run with the same experiment folder overwrites it, so set a unique `RunConfig(name=...)`. `restore_from_dir(path)` loads from an experiment folder.
- Custom algorithms subclass `tune.search.Searcher` (`suggest`, `on_trial_result`, `on_trial_complete`, `save`, `restore`).
- `tune.create_searcher(name, ...)` builds a searcher from a string name.

## Verify
Plot best score versus trial order from `results.get_dataframe()`; a model-based searcher should trend better than random.

## Checked
2026-11-03. Confirmed in Ray repo `tune/api/suggestion.rst`, `python/ray/tune/search/optuna/optuna_search.py` and `search/concurrency_limiter.py`. Removed: `OptunaSearch(metric=, mode=)` shown as required (the docs set both on `TuneConfig`), "import errors appear per trial" and "more samples, not more workers" advice, `grid_search` blanket claim (docs say only that support varies), "searchers checkpoint with Tuner.restore", the `on_trial_start` logging tip. The seed argument is confirmed.
Method: documentation only; no commands were run.
