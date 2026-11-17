---
id: computing-software.ai-ml-engineering.litellm.litellm-weighted-failover
name: litellm-weighted-failover
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, enable-weighted-failover, max-fallbacks, same-group-retry]
level: advanced
status: docs-checked
description: "Retry on a different deployment inside the same model group before using fallbacks, with enable_weighted_failover."
sources:
  - https://docs.litellm.ai/docs/routing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default a failed deployment sends the router to the next entry in `fallbacks` (a different model group). With `enable_weighted_failover` the router first retries inside the same model group, re-picking another deployment by weight. Useful for regional copies of the same model (for example Azure eastus2 and swedencentral).

```
router_settings:
  routing_strategy: simple-shuffle
  enable_weighted_failover: true
```

The SDK equivalent is `Router(..., enable_weighted_failover=True)`.

Behaviour:

- Only active with `routing_strategy` simple-shuffle (the default).
- On a retryable failure the failing deployment id is excluded and a new one is picked from remaining peers, respecting weight, rpm and tpm.
- Exclusions accumulate across hops, so a deployment that just failed is not picked again in the same request chain.
- Capped by `max_fallbacks` (default 5).
- Not triggered for ContextWindowExceededError or ContentPolicyViolationError, which keep their own fallback paths.
- Async only: honoured by `router.acompletion()` and other async entrypoints; sync `router.completion()` falls through to regular fallbacks.
- Cooldowns still apply independently once a deployment crosses allowed_fails.

If the group also uses `order`, the order filter runs first, so re-picks stay within the current minimum-order tier.

Only after all peers are exhausted does the router fall through to the group's configured fallbacks.

## Checked

2026-11-03. Confirmed on the LiteLLM routing page (docs.litellm.ai/docs/routing): enable_weighted_failover in router_settings and Router(), simple-shuffle only, exclusion accumulation, max_fallbacks default 5, the ContextWindowExceededError and ContentPolicyViolationError exceptions, async-only behaviour, cooldown interaction, and order filtering first.

Method: documentation only; no commands were run.
