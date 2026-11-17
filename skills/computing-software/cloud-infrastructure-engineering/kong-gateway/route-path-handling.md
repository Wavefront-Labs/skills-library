---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.route-path-handling
name: route-path-handling
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, path-handling, strip-path, preserve-host, routes, upstream-path]
level: practitioner
status: docs-checked
description: "Kong Route strip_path, preserve_host and path_handling: how the upstream path and Host header are built, defaults true/false/v0, with the docs examples."
sources:
  - https://developer.konghq.com/gateway/entities/route/
  - https://raw.githubusercontent.com/Kong/kong/master/kong/db/schema/entities/routes.lua
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# strip_path, preserve_host and path_handling

**strip_path** (default `true`): removes the matched path prefix before proxying. `/service/path/to/resource` becomes `/path/to/resource` for a Route path of `/service`.

**preserve_host** (default `false`): by default the upstream receives the Service's host in the `Host` header. With `true`, the client's header is kept, so `Host: service.com` reaches the upstream.

**path_handling** (default `v0`; `v0` recommended): controls how Service path, Route path and request path combine. Docs example: Service path `/s`, Route path `/fv0` and request `req` produce `/s/fv0/req` under `v0`. `v1` is deprecated (a warning is logged) and unsupported with expressions.

A Service `path` is the base path used in requests to the upstream.

## Checked

2026-11-04. Confirmed against the Route entity page (strip_path and preserve_host examples, path_handling v0/v1 semantics, v1 unsupported in the expressions router, the /s, /fv0, req example row giving /s/fv0/req) and routes.lua (defaults, v1 deprecation warning).

Method: documentation only; no commands were run.
