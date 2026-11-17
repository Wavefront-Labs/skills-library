---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.route-fields-defaults
name: route-fields-defaults
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, route-entity, https-redirect-status-code, request-buffering, protocols, routes]
level: practitioner
status: docs-checked
description: "Kong Route schema defaults: protocols http/https, strip_path true, preserve_host false, https_redirect_status_code 426, request and response buffering true."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong/db/schema/entities/routes.lua
  - https://developer.konghq.com/gateway/entities/route/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Route fields and defaults

| Field | Default | Constraint |
|---|---|---|
| `protocols` | `http`, `https` | at least one; must come from one group: {http, https}, {tcp, tls, udp}, {tls_passthrough}, {grpc, grpcs} |
| `strip_path` | `true` | |
| `preserve_host` | `false` | |
| `regex_priority` | `0` | `0` means unset; cannot be used with a non-empty `expression` |
| `path_handling` | `v0` | `v0` or `v1`; `v1` triggers a deprecation warning |
| `https_redirect_status_code` | `426` | one of 426, 301, 302, 307, 308 |
| `request_buffering` | `true` | |
| `response_buffering` | `true` | |

`sources` and `destinations` (for stream Routes) cannot be set together with `expression` and cannot be combined with `priority`.

Matching fields: `paths`, `hosts`, `methods`, `headers`, `snis`.

In Gateway 3.14+ the routes docs show Routes accepting HTTPS only by default; add `http` to `protocols` to allow plain HTTP.

See also: route matching priority, regex paths, and path handling skills.

## Checked

2026-11-04. Confirmed against the routes.lua schema (protocol groups and default, https_redirect_status_code one_of and default 426, strip_path, preserve_host, buffering defaults, regex_priority, path_handling v0/v1 and v1 deprecation, expression exclusivity checks) and the Route entity page (3.14+ HTTPS-only default).

Method: documentation only; no commands were run.
