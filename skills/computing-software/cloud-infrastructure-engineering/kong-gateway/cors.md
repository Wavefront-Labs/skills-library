---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.cors
name: cors
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, cors, preflight, access-control-allow-origin, plugins, browsers]
level: practitioner
status: docs-checked
description: "cors plugin config: origins, methods, headers, exposed_headers, credentials, max_age, preflight_continue, private_network and allow_origin_absent with defaults."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong/plugins/cors/schema.lua
  - https://developer.konghq.com/plugins/cors/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cors plugin

| Field | Default | Notes |
|---|---|---|
| `origins` | none | allowed origins for `Access-Control-Allow-Origin`; `*` allows all; entries may be PCRE regex; unset allows all |
| `methods` | all of CONNECT, DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT, TRACE | `Access-Control-Allow-Methods` |
| `headers` | none | `Access-Control-Allow-Headers` |
| `exposed_headers` | none | `Access-Control-Expose-Headers`; unset exposes no custom headers |
| `credentials` | `false` | send `Access-Control-Allow-Credentials: true` |
| `max_age` | none | seconds a preflight result may be cached |
| `preflight_continue` | `false` | proxy `OPTIONS` preflight to the upstream |
| `private_network` | `false` | send `Access-Control-Allow-Private-Network: true` |
| `allow_origin_absent` | `true` | skip CORS headers when the request has no Origin |

Compatible protocols: `grpc`, `grpcs`, `http`, `https`. The plugin cannot be scoped to a Consumer.

Browsers send an `Origin` header; the response must carry a matching `Access-Control-Allow-Origin` or the browser discards it.

Preflight requests cannot carry a custom Host header, so use this plugin only with Routes that match on paths or methods, not Routes that match only on `hosts`.

## Checked

2026-11-04. Confirmed against the plugin's schema.lua (field names, defaults, method list, PCRE or `*` origins, unset origins allow all) and the CORS plugin page (compatible protocols, Origin and Access-Control-Allow-Origin behaviour, Host-header limitation). The configuration reference page renders empty, so the schema is the source for fields. Replaced the protocols default claim with the page's compatible protocols.
Method: documentation only; no commands were run.
