---
id: computing-software.networking-hardware-and-wireless.caddy.reverse-proxy-active-health-checks
name: reverse-proxy-active-health-checks
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [health-checks, active-health, health-uri, health-interval, health-status, health-body, reverse-proxy]
level: practitioner
status: docs-checked
description: "Configure reverse_proxy active health checks: health_uri or port, interval, passes and fails, expected status or body, headers, and per-handler counters."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/reverse_proxy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: probe backends on a timer and route only to healthy ones.

Enable by setting `health_uri` or `health_port`. Each `reverse_proxy` handler tracks its own results, so two handlers proxying to one upstream with different settings do not share pass/fail counts.

Settings and defaults:
- `health_uri <uri>`: path and optional query to request.
- `health_upstream <ip:port>`: probe a different address; use with `health_headers` and the `{http.reverse_proxy.active.target_upstream}` placeholder.
- `health_port <port>`: different port; ignored when `health_upstream` is set.
- `health_interval`: default `30s`.
- `health_passes` (consecutive successes to recover) and `health_fails` (consecutive failures to mark down): both default `1`.
- `health_timeout`: default `5s`.
- `health_method`: default `GET`.
- `health_status`: a 3-digit code or class such as `2xx`; default `200`.
- `health_request_body`: body to send; `{env.*}` is replaced, other braces (JSON) are sent as-is.
- `health_body`: substring or regexp the response body must match.
- `health_follow_redirects`: otherwise a redirect counts as a failure.
- `health_headers { <field> [<values...>] }`: set headers such as `Host` or authentication.

Active checks do not run for dynamic upstreams. Combine with `lb_policy first` for primary/secondary failover.

## Checked
2026-11-03. Confirmed against the Caddy reverse_proxy directive page: syntax, option names, defaults, limits and examples stated here. Removed: statements the page does not make.
Method: documentation only; no commands were run.
