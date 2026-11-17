---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.stream-listen
name: stream-listen
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, stream-listen, tcp-proxy, tls-stream, kong-conf, stream]
level: practitioner
status: docs-checked
description: "Enable Kong's TCP/TLS stream proxy with stream_listen (off by default) and the related stream access log, error log and Nginx directive prefixes."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong.conf.default
  - https://developer.konghq.com/gateway/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# stream_listen

`stream_listen` is a comma-separated list of addresses and ports on which stream mode listens. It defaults to `off`. Per-pair suffixes include `ssl` (require TLS), `proxy_protocol`, `bind`, `reuseport` and `backlog=N`.

Stream-related logs:
- `proxy_stream_access_log`: default `logs/access.log basic`; `off` disables.
- `proxy_stream_error_log`: default `logs/error.log`.

Nginx directive prefixes for the stream module: `nginx_stream_`, `nginx_sproxy_` (stream proxy server), `nginx_supstream_` (stream upstream block).

Active health checks do not apply to Services using `tcp` or `tls` protocols.

## Checked

2026-11-04. Confirmed against kong.conf.default (`stream_listen` default and suffixes, both stream log defaults and `off`, the three stream namespaces) and the Health checks page (tcp/tls exclusion). Removed the example addresses and the Route and Service protocol-group paragraph, which these sources do not state.
Method: documentation only; no commands were run.
