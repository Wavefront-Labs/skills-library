---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.plugin-execution-phases
name: plugin-execution-phases
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, plugin-phases, access-phase, log-phase, plugins, lua]
level: advanced
status: docs-checked
description: "Kong plugin execution phases: HTTP rewrite, access, response or header_filter/body_filter, log; stream preread; WebSocket phases; and the response-phase restriction."
sources:
  - https://developer.konghq.com/gateway/entities/plugin/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Plugin execution phases

HTTP request phases in order: `rewrite`, `access`, then `response` (or `header_filter` and `body_filter`), then `log`.

Other phases:
- WebSocket: `ws_handshake`, `ws_client_frame`, `ws_upstream_frame`, `ws_close`
- Stream: `preread`, then `log`
- `certificate`: runs during the TLS handshake
- `init_worker`: at worker startup
- `configure` (v3.4+): whenever the plugin iterator is rebuilt

Rules:
- `rewrite` runs only for global plugins, because the Service and Consumer are not yet identified at that point.
- A plugin implementing `response` automatically enables buffered proxy mode.
- Kong will not start if a plugin implements `response` together with `header_filter` or `body_filter`.

## Checked

2026-11-04. Confirmed against the Plugins entity page: both phase tables (HTTP, WebSocket, stream), the rewrite global-only rule, buffered proxy mode, the startup refusal with `response` plus a filter phase, and `configure` as v3.4+. Removed the pre-function and post-function paragraph (phase fields, `loadstring`, at-least-one rule), which this page does not cover.
Method: documentation only; no commands were run.
