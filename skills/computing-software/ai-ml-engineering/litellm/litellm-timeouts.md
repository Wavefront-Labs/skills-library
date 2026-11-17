---
id: computing-software.ai-ml-engineering.litellm.litellm-timeouts
name: litellm-timeouts
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, request-timeout, stream-timeout, timeout-by-service-tier]
level: practitioner
status: docs-checked
description: "Set global, per-model, streaming and per-service-tier timeouts for LiteLLM requests, and per-request overrides."
sources:
  - https://docs.litellm.ai/docs/proxy/timeout
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The router timeout covers the entire length of the call and is passed down to the completion() call.

Global:

```
router_settings:
  timeout: 30
litellm_settings:
  request_timeout: 10
```

`litellm_settings.request_timeout` (or env var `REQUEST_TIMEOUT`) is the proxy-wide default when no router or deployment timeout is set.

Per model, under litellm_params:

```
      timeout: 300         # max time for the complete response
      stream_timeout: 30   # max time to wait for the first chunk of a stream
```

`stream_timeout` aborts hanging providers (for example a slow Bedrock start) so another model is retried.

Per service tier:

```
      timeout: 610
      stream_timeout: 610
      timeout_by_service_tier:
        flex: 900
      stream_timeout_by_service_tier:
        flex: 900
```

A request with `"service_tier": "flex"` then waits up to 900 seconds. Per attempt LiteLLM picks the first value set: a timeout sent with the request (`timeout` parameter or `x-litellm-timeout` header), then timeout_by_service_tier for the tier, then the deployment's timeout.

Per request: add `"timeout": 1` to the body (or `extra_body={"timeout": 1}` in the OpenAI SDK).

Testing: set `"mock_timeout": true` in a request to exercise retry and fallback logic; supported on /chat/completions and /completions only.

## Checked

2026-11-03. Confirmed on the timeout page (docs.litellm.ai/docs/proxy/timeout): router timeout, request_timeout and REQUEST_TIMEOUT, per-model timeout and stream_timeout, the service-tier timeouts and their precedence, the per-request timeout, and mock_timeout.

Method: documentation only; no commands were run.
