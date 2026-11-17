---
id: computing-software.ai-ml-engineering.litellm.litellm-fallbacks-basics
name: litellm-fallbacks-basics
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, fallbacks, router-settings, default-fallbacks]
level: practitioner
status: docs-checked
description: "Configure fallbacks from one model group to another, in order, plus default_fallbacks, in the LiteLLM proxy."
sources:
  - https://docs.litellm.ai/docs/proxy/reliability
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Fallbacks are LiteLLM's automatic failover. If a call fails after `num_retries`, LiteLLM falls back to another model group. They are typically from one `model_name` to another.

```
router_settings:
  fallbacks: [{"gpt-6-luna": ["gpt-6.1-sol"]}]
```

The same key also works under `litellm_settings`. A list is tried in order: `["gpt-6-luna", "gpt-6.1-sol", "claude-sonnet-5"]` tries gpt-6-luna first, then gpt-6.1-sol and so on.

Three types:

- `fallbacks`: all remaining errors, such as RateLimitError, 429, 500.
- `context_window_fallbacks`: litellm.ContextWindowExceededError; messages are mapped across providers.
- `content_policy_fallbacks`: litellm.ContentPolicyViolationError, also mapped across providers.

```
router_settings:
  content_policy_fallbacks: [{"claude-sonnet-5": ["my-fallback-model"]}]
  context_window_fallbacks: [{"claude-sonnet-5": ["my-fallback-model"]}]
```

Default fallbacks apply when a specific model group is misconfigured or bad:

```
litellm_settings:
  default_fallbacks: ["claude-opus"]
```

A model-specific entry such as `{"small-model": ["claude-opus"]}` overrides the default.

A combined retry setup from the docs: `litellm_settings: num_retries: 3, request_timeout: 10, fallbacks: [...]` plus `router_settings: allowed_fails: 3, cooldown_time: 30`.

A fallback on another provider or API key cannot decrypt encrypted reasoning from the failed deployment's earlier turns.

Testing: from Proxy v1.85.0 the mock_testing_fallbacks flags are stripped from incoming requests. Trigger a real provider error in a non-production environment and send a normal request.

## Checked

Method: docs-checked 2026-11-09 against the full LiteLLM Fallbacks (proxy/reliability) page: quick start, explanation, content policy, context window, default fallbacks and advanced sections.
