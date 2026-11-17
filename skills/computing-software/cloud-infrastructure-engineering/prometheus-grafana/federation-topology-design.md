---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.federation-topology-design
name: federation-topology-design
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, federation, federation-tree, federation-hierarchy, cross-service-federation-setup, federating-selected-series, global-view]
level: advanced
status: docs-checked
description: "Design hierarchical (per-DC to global) and cross-service Prometheus federation: what to federate, aggregation in leaves, and when not to federate."
sources: ["https://prometheus.io/docs/prometheus/latest/federation/", "https://www.robustperception.io/federation-what-is-it-good-for/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Federation topology design

## Hierarchical federation (tree)
```
 global-prom  <- scrapes /federate of each DC, only aggregated rule outputs
   |-- dc1-prom  <- per-datacenter server, instance-level detail, recording rules
   |-- dc2-prom
```
Rules of thumb:
1. Lower levels do the heavy lifting: recording rules aggregate away `instance` and leave `job:`-prefixed series
   (for example `job:node_memory_MemTotal:sum = sum without(instance)(node_memory_MemTotal{job="node"})`). Only these
   go up a level.
2. The global server federates with a naming-convention selector such as `match[]={__name__=~"^job:.*"}`, so a new
   aggregating rule needs no config change. Do not pull large swathes of series, or all of them.
3. Push alerting as deep down the hierarchy as possible: a target-down alert belongs on the Prometheus that scrapes
   the target, not on a global server several steps away. Global alerting is for cross-DC conditions.
4. Two levels is usual; three or four are not unheard of (Robust Perception).
5. Every Prometheus in an organisation should have unique `external_labels` (for example `datacenter: eu-west-1`).
   Use `sum without(datacenter)(job:node_memory_MemTotal:sum)` for the fleet-wide view.

## Cross-service federation
One service's Prometheus pulls a few series from another's so alerts and queries can use both datasets in one server
(Prometheus docs example: service-level metrics server pulls cluster resource usage for its own service from the
cluster Prometheus).
```yaml
- job_name: federate-db-team
  honor_labels: true
  metrics_path: /federate
  params:
    'match[]': ['{__name__=~"job:mysql_.*",cluster="db1"}']
  static_configs: [{targets: ['db-prom:9090']}]
```
`/federate` needs at least one `match[]` instant vector selector; several are unioned. `honor_labels: true` stops the
scraping server overwriting the source's labels. Request the series by name, and ask the owning team first: reaching
into another team's Prometheus is like using undocumented library internals (Robust Perception). It is usually only done
for alerting, since Grafana can use several data sources in one graph.

## When not to federate
Using federation to pull large swathes of series (or all of them) into one Prometheus and alert and graph only there
is unsuitable, for three reasons given by Robust Perception:
- Scaling: one global server is limited to what one machine handles; the federation request is also heavy to serve.
- Reliability: moving the data needed for alerting adds a failure point, particularly over WAN links.
- Correctness: federated data arrives some time after the scrape and may miss samples through races.

If a Prometheus is only being used as a proxy for another, make the scraping server alert and graph, or scrape via a
proxy using `proxy_url`.

## Verify
- [ ] Federation `match[]` selectors name aggregated (`job:`-style) series, not everything.
- [ ] Alerts that can run on the scraping Prometheus do run there.
- [ ] Each Prometheus has unique `external_labels` identifying its datacenter or cluster.

## Checked
Checked 2026-11-08 against the Prometheus Federation page (/federate, match[], honor_labels, hierarchical and
cross-service use cases, example scrape config) and the Robust Perception federation post (two to four levels, job:
rule naming, unique external labels, reasons not to federate). Removed: the claim that three levels is a practical
maximum with one scrape interval of delay per level, the "few hundred thousand series per scrape" ceiling, the
Thanos/Mimir recommendation figures, the HA replica advice, and the numeric verify thresholds, none of which either page
states.
Method: documentation only; no commands were run.
