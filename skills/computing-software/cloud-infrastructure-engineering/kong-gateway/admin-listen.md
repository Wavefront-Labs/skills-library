---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.admin-listen
name: admin-listen
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, admin-listen, admin-api, listeners, kong-conf]
level: practitioner
status: docs-checked
description: "The kong.conf admin_listen setting: loopback defaults on 8001 and 8444, why to keep it off public interfaces, admin TLS certificate and body-size settings."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong.conf.default
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# admin_listen

Default:

```
admin_listen = 127.0.0.1:8001 reuseport backlog=16384, 127.0.0.1:8444 http2 ssl reuseport backlog=16384
```

Port 8001 is plain HTTP, 8444 is TLS. Both bind to loopback, which is deliberate: the Admin API can reconfigure the gateway, so do not bind it to a public interface without access control in front.

Related settings:
- `admin_ssl_cert` / `admin_ssl_cert_key`: comma-separated certificate and key for `admin_listen` values with TLS enabled (empty by default; usage as for `ssl_cert`).
- `nginx_admin_client_max_body_size`: Admin request body limit, default `10m`.
- `admin_access_log`: default `logs/admin_access.log`; in hybrid mode it also records data plane connections.
- `admin_error_log`: default `logs/error.log`.

Environment form: `KONG_ADMIN_LISTEN` (the `KONG_` prefix plus the uppercase setting name). Setting it to `off` disables the Admin API on that node.

## Checked

2026-11-04. Confirmed against kong.conf.default: the default `admin_listen` value, the advice to restrict access and avoid public interfaces, `off`, `admin_ssl_cert`/`admin_ssl_cert_key`, `nginx_admin_client_max_body_size` 10m, `admin_access_log` and `admin_error_log` defaults; and the Managing Kong Gateway configuration page for the `KONG_` prefix. Removed the claim that Kong generates the admin certificate, the `0.0.0.0` example value and the curl check, none of which the page states for this setting.
Method: documentation only; no commands were run.
