---
id: computing-software.systems-network-administration.netbird.local-metrics-endpoint
name: local-metrics-endpoint
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, prometheus, local-metrics, grafana-dashboard, mdm-metrics]
level: practitioner
status: docs-checked
description: "Expose the NetBird client Prometheus metrics endpoint locally: enabling flags, address, security cautions, available metrics, Grafana dashboard and MDM keys."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/client/local-metrics.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The daemon can serve a Prometheus `/metrics` endpoint, off by default, bound to `127.0.0.1:9191`. Nothing is sent anywhere.

Configure:
- Enable: `netbird up --enable-local-metrics`.
- Address: `--local-metrics-address 127.0.0.1:9300`.
- Disable: `--enable-local-metrics=false`.
- Stored per profile. If already connected, `netbird up` ignores these flags: run `netbird down` first.
- Verify: `curl http://127.0.0.1:9191/metrics`.

Security: no authentication, and it exposes peer names, latencies and connectivity. Keep it on loopback. Non-loopback binds need root (Linux/macOS) or administrator (Windows) and log a warning; if exposed, use a firewall rule or an authenticating reverse proxy.

Prometheus: a scrape job with static target `127.0.0.1:9191`.

Metrics: gauges for management and signal connectivity (1 or 0), known peers, connected peers by `connection_type` (`p2p` or `relay`), latency per directly connected peer (relayed peers have none); histograms for connection stage, sync message, sync phase and login duration, which reset on restart. The `peer` label on latency is the only high-cardinality one.

Grafana: import NetBird's `client.json` dashboard.

MDM keys: `enableLocalMetrics` (boolean) and `localMetricsAddress` (string); an MDM-supplied address skips the privilege check.

## Checked

2026-11-04: read the Local Metrics Endpoint page in full. Confirmed the flags, default address, profile storage, the already-connected note, security and privilege rules, scrape config, metric types and labels, the cardinality note, the Grafana dashboard and the MDM keys. Nothing removed.

Method: documentation only; no commands were run.
