---
id: computing-software.cloud-infrastructure-engineering.linkerd.proxy-metrics-endpoint
name: proxy-metrics-endpoint
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, proxy, metrics, prometheus, observability]
level: advanced
status: docs-checked
description: "Scrape proxy Prometheus metrics at /metrics on port 4191 and know the core request, response and latency series."
sources:
  - https://linkerd.io/2.19/reference/proxy-metrics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each proxy serves Prometheus metrics at `/metrics` on its metrics port, `:4191` by default.

Process-level metrics:

- `proxy_build_info`: constant gauge with build date, proxy version and similar.
- `rustls_info`: gauge describing the TLS library, with labels `tls_suites`, `tls_kx_groups`, `tls_rand`, `tls_key_provider` and `tls_fips`.
- `tokio_rt_*`: counters and gauges for the asynchronous runtime.

Protocol-level metrics:

- `request_total`: requests received, incremented when the request stream begins.
- `response_total`: responses received, incremented when the response stream ends.
- `response_latency_ms`: histogram of response latency measured as time to first byte, from when the proxy processes request headers to the first data frame of the response (or end of stream if there is no data). This reflects application behaviour when a server returns headers immediately but is slow to start the body.
- `route_request_total`, `route_response_latency_ms` and `route_response_total`: the same, collected at route level, so they lack the `authority`, `tls`, `grpc_status_code` and outbound labels and instead have `dst` and `rt_route`.

Latency measurements are not exported to Prometheus until the stream completes, so they can be labeled with the response classification. `request_total`, `response_total` and `response_latency_ms` carry the labels `authority`, `direction` and `tls`; for `direction=inbound` the `authority` label is omitted to stop clients creating unbounded metric series.

Other series on the page include the transport metrics `tcp_open_total`, `tcp_close_total`, `tcp_open_connections`, `tcp_read_bytes_total` and `tcp_write_bytes_total`, and the identity metrics `identity_cert_expiration_timestamp_seconds` and `identity_cert_refresh_count`.

## Checked

2026-11-08. Confirmed against: https://linkerd.io/2.19/reference/proxy-metrics/. Endpoint and port, process-level and protocol-level metric names and definitions, rustls_info labels, TTFB latency definition, label rules, transport and identity metric names.

Removed or reworded: The port-forward example, `linkerd diagnostics proxy-metrics` and the `linkerd-admin` scraping advice (not on the cited page).

Method: documentation only; no commands were run.
