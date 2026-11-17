---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.federation-vs-remote-write-vs-thanos
name: federation-vs-remote-write-vs-thanos
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [federation-vs-remote-write, federation, remote-write, thanos, mimir, global-view]
level: advanced
status: docs-checked
description: "Compare Prometheus federation, remote write to Mimir, Thanos sidecar and Thanos Receive for a global view, based on what each doc states."
sources: ["https://prometheus.io/docs/prometheus/latest/federation/", "https://thanos.io/tip/thanos/quick-tutorial.md/", "https://grafana.com/docs/mimir/latest/get-started/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Federation vs remote write vs Thanos

| Option | What the docs say it does |
|---|---|
| Federation | A server scrapes selected series from another server's `/federate` endpoint; suited to aggregated series up a hierarchy or a few cross-service series, not to pulling everything |
| Remote write to Mimir | Prometheus (or Grafana Alloy `prometheus.remote_write`) pushes to Mimir at `/api/v1/push`; query Mimir as a Prometheus data source at `/prometheus` |
| Thanos Sidecar | Runs next to Prometheus, uploads its blocks to an object storage bucket and exposes a gRPC Store API to Thanos Query |
| Thanos Receiver | Receives data from Prometheus remote write, exposes it and/or uploads it to object storage |

## Choosing
- Federation: only a small set of aggregated recording-rule series (`job:` level) to a global server. Pulling large
  swathes of series hurts scaling, reliability and correctness (see federation-topology-design).
- Sidecar: when Prometheus with local storage already runs and you want backup to object storage plus a global query
  layer. Thanos recommends it when you need to scale out Prometheus; Prometheus stays the collection and alerting
  foundation. Rolling it out has little to no impact on the running Prometheus.
  The Querier must be able to reach each Store API over gRPC; that is the only required communication between nodes.
- Receiver: when data arrives by remote write, to scale out or integrate other remote-write-compatible sources.
- Mimir: Prometheus `remote_write` with `url: http://<mimir>:9009/api/v1/push` (port 9009 in the demo config).

## Thanos pieces to plan for
- Store Gateway serves historical data from the bucket, so Prometheus retention can be decreased.
- Compactor compacts, downsamples and applies retention in the bucket; it must run as a singleton and not while data
  in the bucket is edited by hand.
- Ruler/Rule evaluates alerts and recording rules that need a global view, on top of a Thanos Querier.
- Every Prometheus needs a globally unique set of `external_labels`; set `replica` and run Query with
  `--query.replica-label replica` to deduplicate HA pairs.
- Sidecar requires Prometheus's reload endpoint: start Prometheus with `--web.enable-lifecycle`.

## Verify
- [ ] Each Prometheus has unique `external_labels`.
- [ ] Query can reach every Sidecar's gRPC Store API (Stores page lists them).
- [ ] You tested what a WAN or backend outage loses with your own configuration, because the pages do not publish
  figures for it.

## Checked
Checked 2026-11-08 against the Prometheus Federation page, the Thanos Quick Tutorial (components, sidecar, Store API,
Receiver, Compactor singleton, Ruler, replica label, `--web.enable-lifecycle`) and the Mimir get-started guide
(remote_write URL, port 9009, `/prometheus` data source URL, Alloy remote write). Removed: the comparison grid cells
for freshness, multi-tenancy, NAT and firewall behaviour and moving parts, the VictoriaMetrics, Cortex and Mimir ruler
mentions, the agent-mode default advice, the "WAL about 2h" figure and the 30-minute and 30-day verify targets, which
none of the pages state.
Method: documentation only; no commands were run.
