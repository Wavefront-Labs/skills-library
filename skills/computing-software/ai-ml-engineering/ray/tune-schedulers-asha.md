---
id: computing-software.ai-ml-engineering.ray.tune-schedulers-asha
name: tune-schedulers-asha
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, asha-scheduler, early-stopping, population-based-training, hyperband]
level: practitioner
status: docs-checked
description: "Stop poor trials early with ASHAScheduler in Ray Tune (time_attr, max_t, grace_period, reduction_factor) and use PBT; schedulers vs searchers."
sources:
  - https://docs.ray.io/en/latest/tune/api/schedulers.html
  - https://docs.ray.io/en/latest/tune/key-concepts.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ASHA and schedulers

```python
from ray import tune
from ray.tune.schedulers import ASHAScheduler, PopulationBasedTraining

asha = ASHAScheduler(time_attr="training_iteration", max_t=100,
                     grace_period=10, reduction_factor=3, brackets=1)
tuner = tune.Tuner(trainable, param_space=space,
    tune_config=tune.TuneConfig(metric="val_loss", mode="min", num_samples=50, scheduler=asha))

pbt = PopulationBasedTraining(
    time_attr="training_iteration", metric="loss", mode="min", perturbation_interval=1,
    hyperparam_mutations={"lr": [1e-3, 5e-4, 1e-4, 5e-5, 1e-5], "alpha": tune.uniform(0.0, 1.0)})
```
The trainable must call `tune.report` regularly so the scheduler can compare trials.

## Facts from the docs and API source
- Every scheduler takes a `metric` (a key in the result dict) and a `mode`; set them on `TuneConfig` (as above) or on the scheduler.
- `ASHAScheduler` (alias of `AsyncHyperBandScheduler`) defaults: `time_attr="training_iteration"`, `max_t=100`, `grace_period=1`, `reduction_factor=4`, `brackets=1`, `stop_last_trials=True`. Trials stop once `time_attr` reaches `max_t`; `grace_period` is the minimum age before a trial can be stopped, in `time_attr` units. The docs say one bracket is the recommended default.
- The docs recommend ASHA over the standard `HyperBandScheduler` (better parallelism, no straggler problem on eliminations).
- If a result lacks `time_attr` or the metric, ASHA returns CONTINUE for it, so a misspelled metric name quietly disables early stopping.
- `MedianStoppingRule` stops a trial whose performance is below the median of other trials at similar points in time.
- PBT: top trials are checkpointed; low performers clone a top performer's config, perturb it, and resume from its checkpoint, so the trainable must support save and restore (see tune-checkpointing).
- Schedulers decide when to stop or mutate trials; search algorithms (see tune-search-algorithms) decide what to try. The default scheduler is FIFO (no early stopping).

## Verify
In the `ResultGrid` dataframe (`results.get_dataframe()`), many trials end at low `training_iteration`, a few reach `max_t`.

## Checked
2026-11-03. Confirmed in Ray repo `tune/api/schedulers.rst` and `python/ray/tune/schedulers/async_hyperband.py` (defaults, assertions, on_trial_result). Fixed: `train.report` replaced with `tune.report`; `grace_period=5` example kept as per-trial choice but doc example uses 10. Removed: `time_total_s` fractional-time claim and the "missing key raises" claim (source returns CONTINUE), PBT `loguniform` mutation example (docs show `tune.uniform`).
Method: documentation only; no commands were run.
