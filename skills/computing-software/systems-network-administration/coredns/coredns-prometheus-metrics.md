---
id: computing-software.systems-network-administration.coredns.coredns-prometheus-metrics
name: coredns-prometheus-metrics
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, prometheus, metrics, monitoring, observability]
level: practitioner
status: docs-checked
description: "Export CoreDNS metrics with the prometheus plugin, its default address, core counters, label meanings and runtime_metrics."
sources:
  - https://coredns.io/plugins/metrics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: scrape CoreDNS with Prometheus.

The plugin is named `prometheus` in the Corefile. Syntax:

```
prometheus [ADDRESS] {
    runtime_metrics
}
```

The default address is `localhost:9153` and the path is fixed to `/metrics`. It can be used once per server block. `runtime_metrics` exports the full Go runtime/metrics set (about 100 scalars and 8 histograms); it is a process-wide latch.

Core series:
- `coredns_build_info`, `coredns_panics_total`
- `coredns_dns_requests_total{server, zone, view, proto, family, type}`
- `coredns_dns_request_duration_seconds`, `..._request_size_bytes`, `..._response_size_bytes`
- `coredns_dns_do_requests_total`
- `coredns_dns_responses_total{server, zone, view, rcode, plugin}`
- `coredns_dns_https_responses_total` (status 200, 404, 400, 500)
- `coredns_plugin_enabled`

Labels: `server` is `<scheme>://[<bind>]:<port>`, e.g. `dns://:53`; `proto` is udp or tcp; `family` is 1 for IPv4 and 2 for IPv6; `type` holds common qtypes plus `other`; `plugin` is the plugin that wrote the reply.

Queries that never enter the plugin chain are exported under the fake plugin name `dropped`. Other plugins add their own series.

## Checked

2026-11-03. Page read: https://coredns.io/plugins/metrics/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: the operational-notes paragraph (repeated content, plugin list and handler claim not on the page).

Method: documentation only; no commands were run.
