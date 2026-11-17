---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.access-error-logs
name: access-error-logs
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, proxy-access-log, admin-access-log, proxy-error-log, kong-conf, logging]
level: practitioner
status: docs-checked
description: "kong.conf access and error log settings for the proxy, stream proxy, Admin and Status APIs, their default paths, and how to disable them with off."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong.conf.default
  - https://developer.konghq.com/gateway/logs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Access and error log settings

| Setting | Default |
|---|---|
| `proxy_access_log` | `logs/access.log` |
| `proxy_error_log` | `logs/error.log` |
| `proxy_stream_access_log` | `logs/access.log basic` |
| `proxy_stream_error_log` | `logs/error.log` |
| `admin_access_log` | `logs/admin_access.log` |
| `admin_error_log` | `logs/error.log` |
| `status_access_log` | `off` |
| `status_error_log` | `logs/status_error.log` |

Paths are relative to `prefix`. Setting an access log to `off` disables it. Error log granularity follows `log_level`.

`admin_access_log` also records data plane connections in hybrid mode.

A log format and filter can be given in the value, as in the docs example:

```
proxy_access_log = logs/access.log show_everything if=$keeplog
```

(or `KONG_PROXY_ACCESS_LOG`). That named `show_everything` format and the `$keeplog` map are defined in a custom Nginx template, and a restart is required. Custom templates affect only Nginx access logs, not logging plugins.

## Checked

2026-11-04. Confirmed against kong.conf.default (all eight access/error log settings and defaults, `off`, relative-to-`prefix`, `log_level` granularity, `admin_access_log` data plane entries) and the Kong Gateway logs page (`proxy_access_log` format and `if=$keeplog` example, custom Nginx template, restart, Nginx-only scope). Nothing removed.
Method: documentation only; no commands were run.
