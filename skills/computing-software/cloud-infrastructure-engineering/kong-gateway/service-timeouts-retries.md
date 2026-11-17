---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.service-timeouts-retries
name: service-timeouts-retries
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, connect-timeout, read-timeout, retries, write-timeout, services]
level: practitioner
status: docs-checked
description: "Kong Service connect_timeout, read_timeout, write_timeout and retries: 60000 ms and 5 by default, which errors each timeout returns, and which methods retry."
sources:
  - https://developer.konghq.com/gateway/entities/service/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service timeouts and retries

| Field | Default | On expiry |
|---|---|---|
| `connect_timeout` | `60000` ms | TCP connect fails: Kong returns `502` and retries up to `retries` |
| `read_timeout` | `60000` ms | idle wait for the upstream response: `504` |
| `write_timeout` | `60000` ms | idle time between successive writes of the request body: `504` |
| `retries` | `5` | number of retry attempts |

Retry rule: idempotent methods (such as `GET`, `PUT`, `DELETE`) retry up to `retries`. Non-idempotent methods (such as `POST`, `PATCH`) do not retry unless `proxy_next_upstream non_idempotent` is set in the Nginx configuration.

`read_timeout` and `write_timeout` measure idle time, not total transfer time.

They are set per Service, as fields in the Service body.

Upstream `healthchecks` with passive checks can additionally mark Targets unhealthy on TCP failures and timeouts.

## Checked

2026-11-04. Confirmed against the Gateway Services page (502 on connect failure with retries, 504 on read and write timeouts, idle-time semantics, idempotent and non-idempotent method lists, proxy_next_upstream non_idempotent), services.lua (60000 ms and retries 5 defaults), and the health checks page (passive tcp_failures and timeouts counters).

Method: documentation only; no commands were run.
