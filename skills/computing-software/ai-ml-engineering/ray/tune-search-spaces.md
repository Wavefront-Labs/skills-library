---
id: computing-software.ai-ml-engineering.ray.tune-search-spaces
name: tune-search-spaces
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, tune-search-space, tune-uniform, tune-grid-search, tune-sample-from]
level: practitioner
status: docs-checked
description: "Define Tune search spaces: uniform, loguniform, choice, randint, quniform, grid_search, sample_from and nested dict param_space."
sources:
  - https://docs.ray.io/en/latest/tune/api/search_space.html
  - https://docs.ray.io/en/latest/tune/tutorials/tune-search-spaces.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Search spaces

```python
from ray import tune
import numpy as np

param_space = {
    "lr": tune.loguniform(1e-4, 1e-2),
    "momentum": tune.uniform(0.5, 0.99),
    "batch_size": tune.choice([32, 64, 128]),
    "layers": tune.randint(1, 6),                      # upper bound exclusive
    "dropout": tune.quniform(0.0, 0.5, 0.1),           # rounded to multiples of 0.1
    "optim": tune.grid_search(["adam", "sgd"]),        # every value is run
    "alpha": tune.sample_from(lambda _: np.random.uniform(100)),
    "beta": tune.sample_from(lambda config: config["alpha"] * np.random.normal()),
}
tune.Tuner(trainable, param_space=param_space, tune_config=tune.TuneConfig(num_samples=10))
```

## Facts from the docs
- Other distributions: `qloguniform`, `randn`, `qrandn`, `qrandint`, `lograndint`, `qlograndint`. `randint(-9, 15)` is inclusive-exclusive; `lograndint(1, 10)` samples integers in log space.
- `grid_search` values are all evaluated, and `num_samples=N` repeats the whole grid N times: a 3x3 grid with `num_samples=10` gives 90 trials, each with fresh random values for sampled parameters.
- `tune.sample_from(func)` calls `func` once per trial. The function takes a `config` dict holding the values already sampled for the trial, so `config["alpha"]` makes `beta` conditional on `alpha`. A function that ignores its input is written `lambda _: ...`.
- Not all search algorithms support every domain; `sample_from` and `grid_search` are often unsupported. The default `BasicVariantGenerator` supports all distributions.
- Avoid large objects as search space values; use `tune.with_parameters` or load data inside the trainable from storage every node can reach.

## Verify
`results.get_dataframe()` has `config/lr` values spread across the log range and the expected trial count (grid size times `num_samples`).

## Checked
2026-11-03. Confirmed in Ray repo `tune/api/search_space.rst` and `tune/tutorials/tune-search-spaces.md`. Fixed: `sample_from` dependency syntax `spec.config.a` is not in the docs; they use `lambda config: config["alpha"] ...`. Removed: "ordering across keys is by dependency" and "log scale preferred" advice, the "loguniform bounds must be positive" and per-searcher grid_search compatibility claims (docs only say support varies), `10 ** randint` example.
Method: documentation only; no commands were run.
