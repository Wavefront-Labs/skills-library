---
id: computing-software.ai-ml-engineering.litellm.litellm-routing-strategy-simple-shuffle
name: litellm-routing-strategy-simple-shuffle
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, routing-strategy, simple-shuffle, rpm-tpm-weight]
level: practitioner
status: docs-checked
description: "Default weighted-pick routing across deployments of one model_name using rpm, tpm, weight and daily limits."
sources:
  - https://docs.litellm.ai/docs/routing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Deployments sharing a `model_name` form a group and the Router load balances across them. `simple-shuffle` is the default and the recommended strategy for production: best performance with minimal latency overhead.

How it picks:

- If `rpm` or `tpm` is set on deployments, it makes a weighted pick based on them.
- If neither is set, it picks randomly.
- A `weight` param specifies which deployment gets picked more often.
- Daily limits `rpd` (requests per UTC day) and `tpd` (tokens per UTC day) go in litellm_params next to rpm and tpm; optional `daily_reset_time` ("HH:MM" UTC) moves when daily counts restart.

```
model_list:
  - model_name: gpt-6-luna
    litellm_params:
      model: azure/chatgpt-v-2
      api_key: os.environ/AZURE_API_KEY
      api_version: os.environ/AZURE_API_VERSION
      api_base: os.environ/AZURE_API_BASE
      rpm: 900
  - model_name: gpt-6-luna
    litellm_params:
      model: azure/chatgpt-functioncalling
      rpm: 10
```

Weights: `weight: 9` and `weight: 1` pick the first 90% of the time.
Select the strategy in router_settings: `routing_strategy: simple-shuffle`. Supported values include simple-shuffle, least-busy, usage-based-routing, latency-based-routing and cost-based-routing. The docs' proxy example also sets `redis_host`, `redis_password` and `redis_port` in router_settings.

Warning from the docs: usage-based routing is not recommended for production. It adds significant latency from the Redis operations used to track usage across deployments; use simple-shuffle for high-traffic scenarios.

`enable_pre_call_checks: true` filters deployments by context window and region.

## Checked

Method: docs-checked 2026-11-09 against the LiteLLM Router Load Balancing (docs/routing) page, weighted pick and usage-based warning sections; dropped the weight-ratio and load-test claims, which the page does not state.
