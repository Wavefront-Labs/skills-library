---
id: computing-software.ai-ml-engineering.litellm.litellm-key-alias-pattern-and-limits
name: litellm-key-alias-pattern-and-limits
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, key-alias-pattern, upperbound-key-generate-params, default-key-generate-params]
level: practitioner
status: docs-checked
description: "Enforce key_alias naming, cap key parameters with upperbounds and set defaults for new keys in litellm_settings."
sources:
  - https://docs.litellm.ai/docs/proxy/virtual_keys
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Alias pattern: every `key_alias` sent to /key/generate, /key/service-account/generate, /key/update and /key/{key}/regenerate must match a regex.

```
litellm_settings:
  key_alias_pattern: "^[a-z0-9]+(-[a-z0-9]+)*$"
```

A mismatch fails with HTTP 400 naming the pattern. It replaces the built-in rule turned on by `enable_key_alias_format_validation`, so set one or the other. An update or regenerate that leaves key_alias unchanged is not checked.

Upperbounds:

```
litellm_settings:
  upperbound_key_generate_params:
    max_budget: 100
    budget_duration: "10d"
    duration: "30d"
    max_parallel_requests: 1000
    tpm_limit: 1000
    rpm_limit: 1000
```

A /key/generate with max_budget=200 is rejected with HTTP 400 (`max_budget is over max limit set in config`); values above the bound are not clamped. Omitting budget_duration (or sending null) creates the key with the upperbound value, so upperbounds also act as defaults and cannot be opted out of.

Defaults:

```
litellm_settings:
  default_key_generate_params:
    max_budget: 1.5
    models: ["azure-gpt-3.5"]
    team_id: "core-infra"
    allowed_routes: ["llm_api_routes", "/key/spend/report"]
```

They fill any field that is missing or null. Every route in the allowed_routes list is granted to eligible new keys whatever the owner's role, so list only routes you want them to reach.

## Checked

Method: docs-checked 2026-11-09 against docs.litellm.ai/docs/proxy/virtual_keys (key_alias_pattern, upperbound and default key params sections)
