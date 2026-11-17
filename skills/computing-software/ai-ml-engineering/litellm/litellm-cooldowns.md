---
id: computing-software.ai-ml-engineering.litellm.litellm-cooldowns
name: litellm-cooldowns
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, cooldown-time, allowed-fails, disable-cooldowns]
level: practitioner
status: docs-checked
description: "Configure how many failures cool a deployment down and for how long, per router or per deployment."
sources:
  - https://docs.litellm.ai/docs/routing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Cooldowns apply to individual deployments, not model groups; a cooled deployment is removed from the pool while healthy ones keep serving.

Router level:

```
router_settings:
  allowed_fails: 3     # cool a deployment down once it fails more than 3 calls
  cooldown_time: 30    # seconds
```

Defaults: `allowed_fails` not set; `cooldown_time` 5 seconds (DEFAULT_COOLDOWN_TIME_SECONDS in constants.py).

With no allowed_fails the router cools down on these triggers, each for 5 seconds by default:

- 429: immediately
- failure rate above 50% in the current minute
- non-retryable errors 401, 404, 408

Setting any allowed_fails value (3 included) in router_settings or Router(...) makes the router count failures instead of using those rules.

Per deployment: set under `model_info` (a deployment value overrides the router for that deployment only):

```
  model_info:
    allowed_fails: 1
    cooldown_time: 0   # disable cooldowns for this deployment
```

`allowed_fails` must go under model_info, not litellm_params, because litellm_params is copied into the request sent to the provider and would leak a router-only setting.

Disable all cooldowns: `router_settings: disable_cooldowns: True`.

Symptom when every deployment is cooled: `No deployments available for selected model, Try again in 60 seconds. Passed model=...`.

Deployments recover automatically when the cooldown expires and failure counters reset once healthy. A deployment id is a hash of its litellm_params.

## Checked

2026-11-03. Confirmed on the LiteLLM routing page (docs.litellm.ai/docs/routing): allowed_fails and cooldown_time, defaults (allowed_fails unset, 5 seconds), the three default cooldown triggers, per-deployment settings under model_info, disable_cooldowns, the No deployments available message, and the deployment id hash.

Method: documentation only; no commands were run.
