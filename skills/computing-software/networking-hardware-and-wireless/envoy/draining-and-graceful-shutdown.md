---
id: computing-software.networking-hardware-and-wireless.envoy.draining-and-graceful-shutdown
name: draining-and-graceful-shutdown
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, draining, drain-listeners, graceful, healthcheck-fail, drain-strategy, shutdown]
level: practitioner
status: docs-checked
description: "Gracefully shed Envoy connections before shutdown using drain_listeners?graceful, healthcheck/fail and drain time options."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/operations/draining.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# draining and graceful shutdown
Envoy drains during hot restart, when the graceful sequence is started via the admin `drain_listeners?graceful` endpoint, after `healthcheck/fail`, and when LDS modifies or removes listeners. Draining behaviour comes from server options plus per-listener config.

By default Envoy closes listeners immediately at shutdown. Use the admin endpoints before stopping the process:

```
curl -X POST localhost:9901/healthcheck/fail          # LB sees failing health check
curl -X POST 'localhost:9901/drain_listeners?graceful'
sleep 30                                              # >= --drain-time-s
curl -X POST localhost:9901/quitquitquit
```
`drain_listeners` alone stops listeners at once with no graceful behaviour and stops accepting new connections immediately. With `?graceful`, Envoy discourages requests for `--drain-time-s` while still accepting new connections until the timeout. `--drain-strategy` chooses how request discouraging behaves: `gradual` (default) raises the share of requests encouraged to drain to 100 percent as the drain time elapses, `immediate` encourages all requests at once. The HTTP connection manager adds `Connection: close` to HTTP/1 requests and sends an HTTP/2 GOAWAY.

Gotchas: all admin mutations must be POST; a GET has no effect and returns 400. `healthcheck/fail` requires the HTTP health check filter and makes it fail health check requests regardless of its configuration. With `drain_listeners?skip_exit` listeners keep accepting new connections while existing ones drain. Only the Redis, Mongo and Thrift network filters (Thrift needs the `envoy.reloadable_features.thrift_connection_draining` runtime feature) and the HTTP connection manager support graceful draining. A listener's `drain_type` is `default` or `modify_only`; `modify_only` skips draining on admin health fail.

## Checked
2026-11-03. Confirmed against draining.rst, the admin interface and cli.rst (--drain-strategy). Removed or corrected: the 'confirm' note and the server.live / total_listeners_draining verify step.
Method: documentation only; no commands were run.
