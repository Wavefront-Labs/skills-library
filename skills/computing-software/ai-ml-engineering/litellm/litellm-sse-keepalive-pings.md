---
id: computing-software.ai-ml-engineering.litellm.litellm-sse-keepalive-pings
name: litellm-sse-keepalive-pings
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, keepalive-seconds, sse-keepalive, streaming]
level: advanced
status: docs-checked
description: "Keep idle streaming connections alive through load balancers with keepalive_seconds and sse_keepalive_ping_interval_seconds."
sources:
  - https://docs.litellm.ai/docs/proxy/timeout
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Problem: load balancers and reverse proxies close connections that look idle, even while the client waits for a legitimate slow response (long thinking). Timeouts cap run time; keepalives address idleness.

Per deployment:

```
model_list:
  - model_name: claude-opus
    litellm_params:
      model: anthropic/claude-opus-5
      api_key: os.environ/ANTHROPIC_API_KEY
      keepalive_seconds: 15
```

Once a stream is silent for longer than `keepalive_seconds`, the proxy sends an SSE comment frame (`: ping`) down the connection.

Client overrides: `keepalive_seconds` in a request body (or the `x-litellm-keepalive-seconds` header) has no effect unless the deployment sets `allow_client_keepalive_override: true`. With it, a request can change the default or disable it with 0. A deployment-level `keepalive_seconds: 0` is a hard disable.

Proxy-wide default, applying to every deployment and pass-through route:

```
litellm_settings:
  sse_keepalive_ping_interval_seconds: 15
```

A deployment's own keepalive_seconds still wins, and a deployment-level 0 still disables. Before the upstream answers, a per-deployment value is used only when every deployment behind the requested model name has the same one.

Side effects, which is why it is off until you set an interval: the same setting covers silence before the upstream answers (some providers withhold headers until the first token), so the response opens early. The status line is committed before the outcome is known, so a later failure arrives as an SSE error frame under a 200, and the `x-litellm-*` response headers are absent on a stream that pinged.

## Checked

Method: docs-checked 2026-11-09 against docs.litellm.ai/docs/proxy/timeout (keepalive section, read in full)
