---
id: computing-software.ai-ml-engineering.litellm.litellm-session-affinity
name: litellm-session-affinity
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, session-affinity, optional-pre-call-checks, sticky-sessions]
level: advanced
status: docs-checked
description: "Pin every request of a conversation to the deployment that served its first request using the session_affinity pre-call check."
sources:
  - https://docs.litellm.ai/docs/routing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use it when deployments behind a model group do not share state (for example provider-side prompt caching) or a conversation must stay in one region. It narrows candidates to the pinned deployment before the routing strategy runs and works with any strategy except usage-based-routing (v1).

```
router_settings:
  routing_strategy: simple-shuffle
  optional_pre_call_checks: ["session_affinity"]
  deployment_affinity_ttl_seconds: 3600   # optional, default 3600
```

Send a session id on every request: header `x-litellm-session-id` (`x-litellm-trace-id` is interchangeable), any `x-<vendor>-session-id` header such as `x-claude-code-session-id`, or `metadata.session_id` in the body.

Verify: the `x-litellm-model-id` response header stays the same for every request with the same session id.

How it works:

- The first request of a new session is routed normally; its deployment becomes the pin (on the proxy also scoped to the caller, the virtual key).
- Each request refreshes the pin, so the TTL bounds idle time between turns, not conversation length.
- Pins live in the router cache: shared across instances with Redis, per instance without.
- If the pinned deployment is in cooldown, requests fall through to healthy deployments and the pin is kept.

Settings: `deployment_affinity` in optional_pre_call_checks pins by caller instead of or as well as session id (session pin has priority); `session_affinity_repin_on_failover: true` keeps the replacement (default false); `model_group_affinity_config` limits affinity to listed groups, e.g. `{"gpt-6.1-sol": ["session_affinity"]}`. TTL and model_group_affinity_config are read at startup, so restart after changing them.

## Checked

2026-11-03. Confirmed on the LiteLLM routing page (docs.litellm.ai/docs/routing): optional_pre_call_checks session_affinity, deployment_affinity_ttl_seconds default 3600, accepted session id headers and metadata.session_id, pin refresh and cooldown behaviour, session_affinity_repin_on_failover default false, model_group_affinity_config, and the usage-based-routing (v1) exception.

Method: documentation only; no commands were run.
