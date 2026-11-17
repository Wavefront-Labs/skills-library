---
id: computing-software.ai-ml-engineering.ray.rllib-multi-agent
name: rllib-multi-agent
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, multi-agent-rl, multiagentenv, policy-mapping-fn, rl-module-spec]
level: practitioner
status: docs-checked
description: "Set up multi-agent RL in RLlib: MultiAgentEnv, policies, policy_mapping_fn, shared vs separate policies, and per-agent spaces."
sources:
  - https://docs.ray.io/en/latest/rllib/multi-agent-envs.html
  - https://docs.ray.io/en/latest/rllib/rllib-env.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-agent RL

RLlib's `MultiAgentEnv` closely follows the gymnasium API (it subclasses `gymnasium.Env`) but `reset()` and `step()` return dictionaries mapping agent IDs to each agent's value.

```python
import gymnasium as gym
import numpy as np
from ray.rllib.env.multi_agent_env import MultiAgentEnv

class Tag(MultiAgentEnv):
    def __init__(self, config=None):
        super().__init__()
        self.agents = self.possible_agents = ["chaser", "runner"]
        self.observation_spaces = {a: gym.spaces.Box(-1, 1, (4,), np.float32) for a in self.agents}
        self.action_spaces = {a: gym.spaces.Discrete(4) for a in self.agents}

    def reset(self, *, seed=None, options=None):
        return {a: self.observation_spaces[a].sample() for a in self.agents}, {}

    def step(self, action_dict):
        obs = {a: self.observation_spaces[a].sample() for a in action_dict}
        rewards = {a: 0.0 for a in action_dict}
        terminateds = {"__all__": False}
        truncateds = {"__all__": False}
        return obs, rewards, terminateds, truncateds, {}
```

Training config (from the docs, all agents using the same algorithm class):

```python
import random
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.core.rl_module.multi_rl_module import MultiRLModuleSpec
from ray.rllib.core.rl_module.rl_module import RLModuleSpec

config = (
    PPOConfig()
    .environment(env="my_multiagent_env")
    .multi_agent(
        policy_mapping_fn=lambda agent_id, episode, **kwargs: (
            "traffic_light" if agent_id.startswith("traffic_light_")
            else random.choice(["car1", "car2"])
        ),
        algorithm_config_overrides_per_module={
            "car1": PPOConfig.overrides(gamma=0.85),
            "car2": PPOConfig.overrides(lr=0.00001),
        },
    )
    .rl_module(
        rl_module_spec=MultiRLModuleSpec(rl_module_specs={
            "car1": RLModuleSpec(),
            "car2": RLModuleSpec(),
            "traffic_light": RLModuleSpec(),
        }),
    )
)
algo = config.build()
```

## Notes from the docs
- `self.possible_agents` lists all agent IDs that may appear. If agents are static, set `self.agents` equal to it; otherwise adjust `self.agents` in `reset()` and `step()` as agents enter or leave.
- Set per-agent spaces in `self.observation_spaces` and `self.action_spaces`. For many agents sharing spaces, override `get_observation_space(agent_id)` and `get_action_space(agent_id)` instead.
- The special agent ID `__all__` in the terminated or truncated dict ends the episode for all agents.
- The env controls which agents exist at each step, so it may start with a subset and add or remove agents later.
- `policy_mapping_fn(agent_id, episode, **kwargs)` returns the module ID for an agent. Mapping every agent to one ID gives parameter sharing.
- `config.multi_agent(policies_to_train=[...])` excludes other policies from updates, which allows mixing learning and non-learning policies.
- Training stats are reported per policy in the result dict from `train()`.
- Multi-agent setups are not vectorizable yet.
- RLlib wraps third-party APIs: Farama PettingZoo and DeepMind OpenSpiel.

## Checked
Checked 2026-11-09 against the RLlib multi-agent environments page (read in full) and rllib-env (scaling and registration sections). Removed unconfirmed items: the old `policies={...}` set argument form, the result key `learners/chaser_p`, the picklable-mapping-function advice and the "old stack still works" remark.

Method: docs-checked 2026-11-09 against docs.ray.io multi-agent-envs and rllib-env pages; documentation only, no commands were run.
