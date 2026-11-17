---
id: computing-software.ai-ml-engineering.ray.rllib-custom-environments
name: rllib-custom-environments
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, rllib-env, gymnasium-env, register-env, env-config]
level: practitioner
status: docs-checked
description: "Train RLlib on a custom Gymnasium environment: register_env, env_config, observation/action spaces, and reset/step API gotchas."
sources:
  - https://docs.ray.io/en/latest/rllib/rllib-env.html
  - https://gymnasium.farama.org/api/env/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom environments

RLlib uses Farama's Gymnasium API for single-agent training. An environment is given to the config either as a registered string, a `gymnasium.Env` subclass, or a Tune-registered creator.

```python
import gymnasium as gym
import numpy as np
from ray.rllib.algorithms.ppo import PPOConfig
from ray.tune.registry import register_env

class Walk(gym.Env):
    def __init__(self, config=None):
        self.n = (config or {}).get("n", 10)
        self.observation_space = gym.spaces.Box(0, self.n, shape=(1,), dtype=np.float32)
        self.action_space = gym.spaces.Discrete(2)

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.pos = 0
        return np.array([self.pos], np.float32), {}      # observation, info

    def step(self, action):
        self.pos += 1 if action else -1
        terminated = self.pos >= self.n
        truncated = self.pos < 0
        obs = np.array([self.pos], np.float32)
        return obs, float(terminated), terminated, truncated, {}

# Option 1: pass the class; env_config becomes the constructor's config argument
config = PPOConfig().environment(Walk, env_config={"n": 20})

# Option 2: register a creator with Tune and refer to it by name
register_env("walk", lambda cfg: Walk(cfg))
config = PPOConfig().environment("walk", env_config={"n": 20}).env_runners(num_env_runners=2)
algo = config.build()
```

## Notes from the RLlib docs
- A `gymnasium.Env` subclass passed to `.environment()` must accept a single `config` argument in its constructor, which may default to `None`.
- A `register_env` creator must take a single `config` parameter and return a single non-vectorized `gymnasium.Env`.
- Always register through Ray Tune: gymnasium's own registry is incompatible with distributed Ray, so remote actors cannot see envs registered there.
- Inside a creator, `config.worker_index`, `config.vector_index` and `config.num_workers` identify the EnvRunner, so envs can differ between runners.
- Configure logging inside the environment (it runs in Ray workers); use `logging.getLogger("ray.rllib")`.
- Scale with `env_runners(num_env_runners=...)` (parallel actors) and `env_runners(num_envs_per_env_runner=...)` (vectorized copies per runner); `remote_worker_envs=True` steps sub-environments as separate processes. Multi-agent setups are not vectorizable yet.
- For environments needing more than 1 CPU per runner, set `num_cpus_per_env_runner` and `num_gpus_per_env_runner`.
- Gymnasium convention: `reset` returns an observation and an info dict; `step` returns observation, reward, terminated, truncated and info.

## Verify
`algo.train()` runs and returns a result dict.

## Checked
Checked 2026-11-09 against the RLlib environments page (read in full) and the Gymnasium Env API page (downloaded; confirmed the terminated/truncated step API in outline only). Removed unconfirmed items: `check_env`, `TimeLimit`, the float32/float64 mismatch claim, the `episode_len_mean` check and the claim that old four-tuple envs fail.

Method: docs-checked 2026-11-09 against docs.ray.io rllib-env and gymnasium.farama.org api/env pages; documentation only, no commands were run.
