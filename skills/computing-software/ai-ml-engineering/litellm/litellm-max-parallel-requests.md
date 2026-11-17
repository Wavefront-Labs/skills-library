---
id: computing-software.ai-ml-engineering.litellm.litellm-max-parallel-requests
name: litellm-max-parallel-requests
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, max-parallel-requests, concurrency, rate-limit-429]
level: advanced
status: docs-checked
description: "Cap concurrent calls per deployment with max_parallel_requests; over-cap requests get an immediate 429, not a queue."
sources:
  - https://docs.litellm.ai/docs/routing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set per deployment under litellm_params, with a default under router_settings:

```
model_list:
  - model_name: gpt-6.1-sol
    litellm_params:
      model: openai/gpt-6.1-sol
      api_key: os.environ/OPENAI_API_KEY
      rpm: 2   # derives max_parallel_requests=2
router_settings:
  num_retries: 0   # optional, surfaces the 429 to the caller instead of retrying
  default_max_parallel_requests: 20   # for deployments with no max_parallel_requests, rpm or tpm
```

SDK: `"max_parallel_requests": 10` in litellm_params, or `Router(model_list=..., default_max_parallel_requests=20)`.

If tpm or rpm is set and no explicit limit, the limit is derived. Precedence: `max_parallel_requests`, then `rpm`, then `int(tpm / 1000 * 6)` (six concurrent requests per 1000 TPM, minimum 1), then the default.

Failure mode: a request arriving while every slot is in use fails right away with a 429 naming the deployment and its max_parallel_requests (`litellm.RateLimitError: Deployment has all max_parallel_requests slots in use ...`). There is no wait queue. With the config above, four simultaneous requests get two 200s and two immediate 429s.

## Checked

2026-11-03. Confirmed on the LiteLLM routing page (docs.litellm.ai/docs/routing): max_parallel_requests per deployment, default_max_parallel_requests (router_settings and Router()), the precedence including int(tpm / 1000 * 6), the immediate 429 message and the four-requests example. Removed an unconfirmed paragraph about earlier queuing behaviour.

Method: documentation only; no commands were run.
