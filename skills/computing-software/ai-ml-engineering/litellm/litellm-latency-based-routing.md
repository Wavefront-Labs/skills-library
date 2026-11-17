---
id: computing-software.ai-ml-engineering.litellm.litellm-latency-based-routing
name: litellm-latency-based-routing
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, latency-based-routing, routing-strategy-args, lowest-latency-buffer]
level: advanced
status: docs-checked
description: "Route to the lowest-latency deployment and tune the averaging window and buffer."
sources:
  - https://docs.litellm.ai/docs/routing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`routing_strategy: latency-based-routing` picks the deployment with the lowest response time. It caches and updates response times for each deployment based on when a request was sent and received.

```
router_settings:
  routing_strategy: latency-based-routing
  enable_pre_call_checks: true
```

Time window: how far back to consider when averaging latency for a deployment (`ttl`):

```
router_settings:
  routing_strategy_args: {"ttl": 10}
```

Lowest latency buffer: a buffer within which deployments are candidates. Docs example with five deployments at 0.07s, 0.1s, 0.1s, 0.1s and 4.66s: to avoid sending all requests to the 0.07s one, set a 50% buffer so the three 0.1s deployments are also considered.

```
router_settings:
  routing_strategy_args: {"lowest_latency_buffer": 0.5}
```

In the Python SDK, pass the same dict to `Router(..., routing_strategy_args=...)`.

Verify in the SDK: after two warm-up calls, `router.lowestlatency_logger.get_available_deployments(model_group=model, healthy_deployments=router.healthy_deployments)` returns the deployment the next call should use; the response `_hidden_params["model_id"]` matches its `model_info.id`.

Other strategies: `least-busy` picks the deployment with the fewest ongoing calls; `usage-based-routing` picks the lowest TPM usage for the minute and filters out deployments over their tpm/rpm (for Azure, RPM = TPM / 6).

## Checked

Method: docs-checked 2026-11-09 against the LiteLLM Router Load Balancing (docs/routing) page, Latency-Based, Rate-Limit Aware and Least-Busy sections.
