---
id: computing-software.cloud-infrastructure-engineering.alertmanager.api-v2-overview
name: api-v2-overview
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, api-v2, openapi, route-prefix, connectrpc]
level: practitioner
status: docs-checked
description: "Alertmanager API v2: OpenAPI-generated, /api/v2 prefix, v1 removal in 0.27.0, route-prefix behaviour and the experimental ConnectRPC API."
sources: ["https://raw.githubusercontent.com/prometheus/alertmanager/main/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Alertmanager API v2

The current Alertmanager API is version 2. It is fully generated via the OpenAPI project and Go Swagger, except the HTTP handlers themselves. The specification is `api/v2/openapi.yaml` in the repository; any OpenAPI generator can produce clients for all major languages.

Access:
- APIv2 uses the `/api/v2` prefix, so the status endpoint is `/api/v2/status`.
- If `--web.route-prefix` is set, API routes get that prefix too: `--web.route-prefix=/alertmanager/` gives `/alertmanager/api/v2/status`.
- APIv1 was deprecated in `0.16.0` and removed as of `0.27.0`.

Experimental ConnectRPC API:
- Serves Connect and gRPC-Web under the route-prefix-aware `/api/` path.
- Native gRPC, health and reflection are served at the server root.
- The listener accepts native gRPC over exporter-toolkit TLS with HTTP/2 ALPN, and over plaintext h2c.
- h2c provides neither encryption nor peer authentication, so expose a plaintext listener only on a trusted network or behind a trusted TLS-terminating proxy. Use `--web.config.file` for TLS on direct exposure.

```
curl http://localhost:9093/api/v2/status
```

## Checked

2026-11-08. Confirmed against the Alertmanager README (API section): OpenAPI and Go Swagger generation, api/v2/openapi.yaml, the /api/v2 prefix, --web.route-prefix behaviour, APIv1 deprecated in 0.16.0 and removed in 0.27.0, and the experimental ConnectRPC paragraph. Removed: the alerts/groups routeLabels claim, which the README does not state.

Method: documentation only; no commands were run.
