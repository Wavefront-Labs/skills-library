---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-prometheus-metrics-and-usage
name: crowdsec-prometheus-metrics-and-usage
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [prometheus, metrics, metrics-level, grafana, usage-metrics, pprof]
level: advanced
status: docs-checked
description: "Expose CrowdSec Prometheus metrics, choose a metrics level and use bouncer usage metrics reported to the Local API."
sources: ["https://docs.crowdsec.net/docs/observability/prometheus", "https://docs.crowdsec.net/docs/observability/usage_metrics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
CrowdSec exposes Prometheus metrics at `http://127.0.0.1:6060/metrics` by default; edit `listen_addr` in `config.yaml` to let an external Prometheus scrape it. All counters are "since CrowdSec start".

## Level

The `level` parameter: `none` registers no metrics, `aggregated` registers only aggregates (per-machine and per-bouncer LAPI metrics, per-node parser metrics, decision and alert gauges and LAPI response time are absent), `full` (default) registers everything. Acquisition metrics only appear for configured datasources.

## Key metrics

- Scenarios: `cs_buckets`, `cs_bucket_instantiation_total`, `cs_bucket_overflowed_total`, `cs_bucket_underflowed_total` (created but expired for lack of events), `cs_bucket_canceled_total`, `cs_bucket_poured_total`.
- Parsers: `cs_node_hits_total`, `cs_node_hits_ok_total`, `cs_node_hits_ko_total`, `cs_node_wl_hits_total`, `cs_parser_hits_total`, `_ok_total`, `_ko_total`.
- `cs_postoverflow_queue_depth`: how full the postoverflow queues are.

The metrics can be scraped by a Prometheus server and visualised with Grafana.

## Usage metrics

From CrowdSec 1.6.3, Log Processors and remediation components report usage to LAPI (support rolls out per bouncer). Firewall bouncers report dropped bytes and packets; HTTP-based bouncers such as OpenResty count handled requests. Traffic is broken down by decision origin: `crowdsec`, `CAPI`, `cscli`, `cscli-import`, `appsec`, `console` and `lists:NAME`. View with `cscli metrics show bouncers`. Numbers differ from `cscli decisions list` because of query filters and because firewall blocking makes attackers give up.

## Checked

2026-11-03. Confirmed against the Prometheus and Usage Metrics pages: default endpoint, metrics levels (none, aggregated, full default), metric names listed, 1.6.3 requirement, per-bouncer rollout, origin list including lists:XXX, and why numbers differ from cscli decisions list. Removed: the prometheus_uri and /debug pprof claims (the /debug port is on the network-management page, not this one).

Method: documentation only; no commands were run.
