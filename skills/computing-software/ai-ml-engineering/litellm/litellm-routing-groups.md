---
id: computing-software.ai-ml-engineering.litellm.litellm-routing-groups
name: litellm-routing-groups
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, routing-groups, per-model-strategy, router-settings]
level: sme
status: docs-checked
description: "Apply different routing strategies to different model names in one router with routing_groups, which are also callable models."
sources:
  - https://docs.litellm.ai/docs/routing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A routing group binds a list of `model_name`s to a strategy and optional args. Models not claimed by a group use the router's top-level `routing_strategy`.

```
router_settings:
  routing_strategy: simple-shuffle   # for models in no explicit group
  routing_groups:
    - group_name: latency-sensitive
      models: [gpt-6.1-sol]
      routing_strategy: latency-based-routing
      routing_strategy_args:
        ttl: 3600
```

Rules:

- Each model_name may belong to at most one group; overlap raises ValueError at init.
- Ungrouped models use the top-level routing_strategy and routing_strategy_args (an implicit group named `default`, which is reserved).
- Each group can override routing_strategy_args.
- The group is resolved per request from the model name after the pre-routing hook.

A group is also callable as a model: request `model: <group_name>` and LiteLLM picks among every member's deployments using the group's strategy. Group names appear in /v1/models.

Access control treats the group as its own model name. Grant `<group_name>` on a key or team to let it list and call the group. Membership is not expanded in either direction: a key granted only the group cannot call members directly.

Two groups may use the same strategy with different args; each gets independent state. Update at runtime with `Router.update_settings(routing_groups=[...])` or the proxy's /config/update; per-group state is rebuilt. Groups can also be managed in the dashboard.

## Checked

Method: docs-checked 2026-11-09 against the LiteLLM Router Load Balancing (docs/routing) page, Routing Groups section.
