---
id: computing-software.cloud-infrastructure-engineering.contour.contour-listener-config-hardening
name: contour-listener-config-hardening
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [listener-config, connection-balancer, max-requests-per-io-cycle, http2-max-concurrent-streams, max-request-body-bytes, socket-options, runtime-settings]
level: advanced
status: docs-checked
description: "Contour listener config block: connection-balancer, per-connection limits, HTTP/2 stream limits for CVE mitigation, max request body, socket options, runtime-settings."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/configuration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Contour listener config and hardening knobs

The `listener` block tunes Envoy listeners:

```yaml
listener:
  connection-balancer: exact
  max-requests-per-connection: 1000
  per-connection-buffer-limit-bytes: 32768
  max-requests-per-io-cycle: 10
  http2-max-concurrent-streams: 100
  max-connections-to-accept-per-socket-event: 1
  max-request-body-bytes: 10485760
  socket-options:
    tos: 64
    traffic-class: 64
```

- `connection-balancer: exact` balances connections between threads in one Envoy.
- `max-requests-per-io-cycle` caps requests processed per connection per I/O cycle; the docs name it as a mitigation for CVE-2023-44487 when abusive traffic is seen (sets runtime `http.max_requests_per_io_cycle`).
- `http2-max-concurrent-streams` sets SETTINGS_MAX_CONCURRENT_STREAMS; the docs recommend not setting it below 100.
- `max-connections-to-accept-per-socket-event`: low values recommended; unset accepts all pending connections at once.
- `max-request-body-bytes` (min 1) rejects larger bodies with 413 on all routes.
- `socket-options.tos` (IPv4) and `traffic-class` (IPv6): 0-255, 0 unset; setting the wrong family for an IPv6-only or IPv4-only listener errors.

`runtime-settings` is a map of arbitrary Envoy runtime keys, for disabling a new Envoy feature that breaks things. Contour-managed keys (`re2.max_program_size.*`, `http.max_requests_per_io_cycle`, listener connection limits) cannot be overridden; unknown keys are not validated.

## Checked

2026-11-04. Confirmed against the Contour Configuration Reference (configuration.md): the fields, defaults, flags and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
