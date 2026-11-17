---
id: computing-software.ai-ml-engineering.litellm.litellm-deployment-order-priority
name: litellm-deployment-order-priority
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, deployment-order, priority, failover]
level: practitioner
status: docs-checked
description: "Prioritise deployments within a model group with litellm_params.order so lower orders are tried first."
sources:
  - https://docs.litellm.ai/docs/routing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set `order` in litellm_params. Lower values mean higher priority. When several deployments share an order, the routing strategy picks among them.

```
model_list:
  - model_name: gpt-6.1-sol
    litellm_params:
      model: azure/gpt-4-primary
      api_key: os.environ/AZURE_API_KEY
      order: 1  # highest priority
  - model_name: gpt-6.1-sol
    litellm_params:
      model: azure/gpt-4-fallback
      api_key: os.environ/AZURE_API_KEY_2
      order: 2  # tried when order=1 fails
```

Behaviour:

- When a request to an order=1 deployment fails (connection error, 404, 429 and so on), the router tries order=2, then order=3, and so on.
- Each order level gets its own retries before escalating.
- Context window errors use a matching `context_window_fallbacks` rule before later orders. When no rule matches the requested group, later orders and then generic fallbacks remain available.
- A hop to a deployment that cannot decrypt the failed deployment's encrypted reasoning (another provider or API key) drops those reasoning items and keeps their summaries, so the hop answers instead of failing with `invalid_encrypted_content`.

Order and weight together: the order filter runs before the weighted pick, so weighted failover re-picks only among deployments in the current minimum-order tier. Promotion to the next tier happens through order-based fallback.

Weight (`weight: 2` picks a deployment twice as often as `weight: 1`) works with the simple-shuffle strategy, the default.

## Checked

2026-11-03. Confirmed on the LiteLLM routing page (docs.litellm.ai/docs/routing): order in litellm_params with lower meaning higher priority, escalation on failure with per-level retries, context window fallback precedence, the invalid_encrypted_content reasoning handling, order before weight, and weight with simple-shuffle.

Method: documentation only; no commands were run.
