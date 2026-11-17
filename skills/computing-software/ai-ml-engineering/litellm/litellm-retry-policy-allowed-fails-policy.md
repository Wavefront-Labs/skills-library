---
id: computing-software.ai-ml-engineering.litellm.litellm-retry-policy-allowed-fails-policy
name: litellm-retry-policy-allowed-fails-policy
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, retry-policy, allowed-fails-policy, error-type]
level: advanced
status: docs-checked
description: "Set retry counts and cooldown thresholds per exception type with RetryPolicy and AllowedFailsPolicy."
sources:
  - https://docs.litellm.ai/docs/routing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: set retry counts and cooldown tolerance per error type instead of one number for all errors.
RetryPolicy sets `num_retries` by exception received. AllowedFailsPolicy sets allowed fails per minute before cooling a deployment down.

RetryPolicy has one field per error type: AuthenticationErrorRetries, TimeoutErrorRetries, RateLimitErrorRetries, ContentPolicyViolationErrorRetries, BadRequestErrorRetries, NotFoundErrorRetries, InternalServerErrorRetries, ServiceUnavailableErrorRetries, plus `DefaultRetries` for any error without its own field.

Proxy config:

```
router_settings:
  retry_policy: {
    "BadRequestErrorRetries": 3,
    "ContentPolicyViolationErrorRetries": 4,
    "NotFoundErrorRetries": 0,
    "DefaultRetries": 2
  }
  allowed_fails_policy: {
    "ContentPolicyViolationErrorAllowedFails": 1000,
    "RateLimitErrorAllowedFails": 100
  }
```

AllowedFailsPolicy also supports ServiceUnavailableErrorAllowedFails, BadGatewayErrorAllowedFails and NotFoundErrorAllowedFails.

SDK:

```
from litellm.router import RetryPolicy, AllowedFailsPolicy
retry_policy = RetryPolicy(AuthenticationErrorRetries=0, NotFoundErrorRetries=0, DefaultRetries=2)
router = litellm.Router(model_list=[...], retry_policy=retry_policy, allowed_fails_policy=AllowedFailsPolicy(RateLimitErrorAllowedFails=100))
```

Per deployment: put `allowed_fails_policy` under that deployment's `model_info`. A deployment-level policy takes full precedence over the router-level one for that deployment:

```
  model_info:
    allowed_fails_policy:
      RateLimitErrorAllowedFails: 0
      InternalServerErrorAllowedFails: 5
```
Error types without an entry fall back to `DefaultRetries`. AllowedFailsPolicy has the same shape: one `...AllowedFails` field per error type, set on the router or per deployment.

## Checked

Method: docs-checked 2026-11-09 against the LiteLLM Router Load Balancing (docs/routing) page, retries and Custom Retries/Cooldowns by Error Type sections.
