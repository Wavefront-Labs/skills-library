---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-support-bundle-and-component-metrics
name: grafana-alloy-support-bundle-and-component-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [support-bundle, support, component-id, disable-support-bundle, pprof, metrics-endpoint]
level: practitioner
status: docs-checked
description: "Generate an Alloy support bundle from /-/support, know its contents and redactions, and use component_id-labelled metrics on /metrics."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/troubleshoot/support_bundle.md", "https://github.com/grafana/alloy/blob/main/docs/sources/troubleshoot/component_metrics.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Support bundles and component metrics

## Support bundle
Not available in v1.4 and older, and not covered by backward-compatibility guarantees. `GET /-/support?duration=N` returns a compressed bundle. It is on by default; disable with `--server.http.disable-support-bundle`. `duration` is optional, must not exceed the HTTP server write timeout and defaults to it. The endpoint is only on the HTTP listen address (default `localhost:12345`). Everything is plain text, so inspect it before sharing.

Contents:
- `alloy-components.json` (from `/api/v0/web/components`) and `alloy-peers.json` (from `/api/v0/web/peers`).
- `alloy-environment.txt`: Go runtime variables; `HTTP_PROXY` and `HTTPS_PROXY` show as `<redacted>` if set.
- `alloy-logs.txt` during collection, `alloy-metadata.yaml` (version, OS, architecture, uptime), `alloy-runtime-flags.txt`.
- `alloy-metrics-sample-start.txt` and `alloy-metrics-sample-end.txt`.
- `pprof/` CPU, heap, goroutine, mutex and block profiles.
- `sources/` copies of local configs, and `sources/remote-config/remote.alloy` for the last remote configuration.

## Component metrics
Components may expose Prometheus metrics on `/metrics` of the Alloy HTTP server. Each carries a `component_id` label, for example `prometheus.remote_write.production`. They describe component state (for alerting and debugging), not the telemetry being processed.

## Checked
2026-11-04: confirmed against the Generate a support bundle and Component metrics pages. Removed: the claim that each component's reference page lists its metrics and not all expose any (not on the pages).
Method: documentation only; no commands were run.
