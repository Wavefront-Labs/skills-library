---
id: computing-software.ai-ml-engineering.ray.rllib-algorithm-config
name: rllib-algorithm-config
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, algorithm-config, ppo-config, rllib, env-runners]
level: practitioner
status: docs-checked
description: "Configure and train RL algorithms in RLlib with AlgorithmConfig builders (environment, env_runners, training, resources, evaluation)."
sources:
  - https://docs.ray.io/en/latest/rllib/rllib-algorithms.html
  - https://docs.ray.io/en/latest/rllib/package_ref/algorithm-config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AlgorithmConfig

An `AlgorithmConfig` subclass (for example `PPOConfig`) is built with chained setter methods; `build_algo()` (the API reference lists it as the builder method) or `build()` (used in the PPO docs example) creates the Algorithm.

```python
from ray.rllib.algorithms.ppo import PPOConfig

config = (
    PPOConfig()
    .environment("CartPole-v1")
    .env_runners(num_env_runners=4, num_envs_per_env_runner=2)
    .training(lr=3e-4, gamma=0.99, train_batch_size_per_learner=4000, num_epochs=10)
    .learners(num_learners=1, num_gpus_per_learner=0)
    .evaluation(evaluation_interval=5, evaluation_num_env_runners=1)
    .debugging(seed=1)
)
algo = config.build()
algo.train()
```

Tune integration (from the PPO docs): pass the config object itself.

```python
from ray import tune

tune.Tuner(
    "PPO",
    run_config=tune.RunConfig(stop={"training_iteration": 1}),
    param_space=config,
).fit()
```

## Parameters (from the API reference)
- `env_runners`: `num_env_runners` is the number of EnvRunner actors for parallel sampling; `num_envs_per_env_runner` is the number of environments stepped per runner.
- `training`: `gamma` is the discount factor; `lr` is a float or schedule; `train_batch_size_per_learner` is per Learner, so the effective batch is `num_learners` x that value; `num_epochs` is complete passes over the train batch. Algorithm-specific options (for PPO `clip_param`, `kl_coeff`, `lambda_` and others) go in the same `training()` call.
- `learners`: `num_learners` is the number of Learner workers; with `num_learners=0` RLlib creates one local Learner. `num_gpus_per_learner` sets GPUs per Learner; for 4 GPUs where the model fits on one, use `num_learners=4`, `num_gpus_per_learner=1`.
- `evaluation`: `evaluation_interval` runs evaluation every N training iterations; `evaluation_num_env_runners` sets the number of parallel evaluation EnvRunners.
- `debugging(seed=...)` sets the random seed (combined with the worker index per worker).
- `framework(...)` exists on the config for the deep-learning framework choice.

## Gotchas
- RLlib's API changed between releases (older `rollouts` and `num_rollout_workers` naming versus `env_runners`; the new stack is enabled by `enable_rl_module_and_learner` and `enable_env_runner_and_connector_v2`). Match code to the docs for your installed version.
- Some evaluation settings only apply on the new stack, so read the parameter text for your version.

## Checked
Checked 2026-11-09 against the RLlib algorithms page (PPOConfig example, Tuner example) and the AlgorithmConfig API reference (environment, training, env_runners, learners, evaluation, debugging, framework sections searched; learners and training text read). Removed unconfirmed items: `rllib train` CLI, `save()` flow, result dict keys, the CartPole score target, `to_dict` Tune usage, the "GPU only in learners" claim and the `api_stack(...)` call.

Method: docs-checked 2026-11-09 against docs.ray.io rllib-algorithms and algorithm-config pages; documentation only, no commands were run.
