---
id: computing-software.networking-hardware-and-wireless.caddy.reverse-proxy-passive-health-and-events
name: reverse-proxy-passive-health-and-events
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [passive-health, fail-duration, max-fails, unhealthy-status, unhealthy-latency, events, reverse-proxy]
level: practitioner
status: docs-checked
description: "Mark reverse_proxy backends unhealthy from live traffic with fail_duration, max_fails, unhealthy_status, latency and request count, plus healthy and unhealthy events."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/reverse_proxy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let real requests demote failing backends.

Passive checks run inline with proxied requests and are enabled only by `fail_duration` greater than zero (default 0, off). The page suggests `30s` as a starting point.

- `fail_duration`: how long a failed request is remembered.
- `max_fails`: failures within that window needed to consider the backend down; at least 1, default 1.
- `unhealthy_status`: statuses that count as failures, as codes or classes, e.g. `404` or `5xx`.
- `unhealthy_latency`: a request taking this long counts as failed.
- `unhealthy_request_count`: the permissible simultaneous requests per backend; at that load the backend counts as overloaded and others are preferred. Keep it large: the proxy then caps total concurrency at `unhealthy_request_count x upstream count`, and further requests error with no upstream available.

Events: when an upstream changes state Caddy emits `healthy` (was unhealthy) or `unhealthy` (was healthy). The metadata `host` identifies the upstream and is usable as `{event.data.host}` with the `exec` event handler, so you can notify or log on a transition.

## Checked
2026-11-03. Confirmed against the Caddy reverse_proxy directive page: syntax, option names, defaults, limits and examples stated here. Removed: statements the page does not make.
Method: documentation only; no commands were run.
