---
id: computing-software.ai-ml-engineering.litellm.litellm-retries-precedence
name: litellm-retries-precedence
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, num-retries, retry-after, x-litellm-num-retries]
level: practitioner
status: docs-checked
description: "Where num_retries can be set, which one wins, and why max_retries has no effect on router calls."
sources:
  - https://docs.litellm.ai/docs/routing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
LiteLLM retries failed requests in sync and async paths. RateLimitError uses exponential backoff; generic errors retry immediately.

```
router = Router(model_list=model_list, num_retries=3, retry_after=5)  # waits min 5s before retrying
```

`num_retries` can come from four places, highest priority first:

1. the `x-litellm-num-retries` request header (proxy only)
2. `num_retries` in the request body
3. `num_retries` in a deployment's litellm_params in model_list
4. `num_retries` in litellm_settings (router-wide default)

A caller can always raise or lower the count for one request, including 0 to disable retries. A deployment value applies when the request carries none and overrides the global default.

`num_retries` is not `max_retries`. num_retries is LiteLLM's own retry loop; max_retries is the provider SDK's internal retry count. For calls through the router, LiteLLM owns retries and pins the provider client to `max_retries: 0`, so max_retries in the request body or litellm_params has no effect on a proxy request. This is deliberate: it stops a deployment `num_retries: N` from being applied twice and turning one request into (1 + N) ** 2 upstream calls. Use num_retries to control attempts.

Proxy example: `litellm_settings: num_retries: 3` retries 3 times on each model_name.

## Checked

2026-11-03. Confirmed on the LiteLLM routing page (docs.litellm.ai/docs/routing): exponential backoff for RateLimitError, retry_after, the four-level num_retries precedence, num_retries versus max_retries, and the (1 + N) ** 2 explanation.

Method: documentation only; no commands were run.
