---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.status-listen
name: status-listen
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, status-listen, status-api, monitoring, kong-conf]
level: practitioner
status: docs-checked
description: "The kong.conf status_listen setting for Kong's read-only status API: default 127.0.0.1:8007, disabling it, and its access and error log settings."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong.conf.default
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# status_listen

The Status API is a read-only endpoint that lets monitoring tools retrieve metrics, healthiness and other non-sensitive information about the current node. Default:

```
status_listen = 127.0.0.1:8007 reuseport backlog=16384
```

Set `status_listen` to `off` to disable it. Per-address suffixes: `ssl`, `http2`, `proxy_protocol`.

Logs:
- `status_access_log` defaults to `off`.
- `status_error_log` defaults to `logs/status_error.log`.

Nginx directives for this server block use the `nginx_status_` prefix.

In hybrid mode, read-only Upstream and Target endpoints are exposed on the data plane status API, because data planes have no Admin API of their own.

## Checked

2026-11-04. Confirmed against kong.conf.default (default value, `off`, suffixes, both log defaults, the `nginx_status_` namespace) and the Hybrid mode page (data plane Status API endpoints). Removed advice about exposing the loopback bind.
Method: documentation only; no commands were run.
