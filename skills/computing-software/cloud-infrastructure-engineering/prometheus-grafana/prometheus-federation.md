---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-federation
name: prometheus-federation
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, federation, hierarchical-federation, cross-service-federation, federate-endpoint, honor-labels, match-params, aggregated-metrics, global-view, external-labels, recording-rules, remote-write-vs-federation, thanos, mimir, pca]
level: practitioner
status: docs-checked
description: "Use /federate correctly: hierarchical federation of pre-aggregated recording rules, honor_labels, cross-service pulls of a few series, and why raw series swamp the global server."
sources: ["https://prometheus.io/docs/prometheus/latest/federation/", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/#scrape_config"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Federation

**Goal:** a global Prometheus that holds a small, aggregated slice of many local servers'
data, without becoming a copy of all of them.

## 1. What `/federate` does
Any Prometheus serves `/federate`, which returns the **current value** of the selected series. At least one
`match[]` parameter is required; each is an instant vector selector (`up`, `{job="api-server"}`), and several are
unioned. Another Prometheus scrapes that endpoint like any target, so:
- it is sampled at the federating server's `scrape_interval`, not the source's;
- `honor_labels: true` is needed so source labels are not overwritten (by default conflicting labels are renamed
  `exported_job`, `exported_instance`, and so on);
- `honor_timestamps` defaults to `true`, so source timestamps are kept.

## 2. Hierarchical federation (the intended use)
Many per-datacenter servers collect detail; global servers collect only aggregated (job-level) data. Local servers
compute recording rules (`job:http_requests:rate5m`); the global server pulls only those `job:`-level series.
```yaml
# on the global Prometheus
scrape_configs:
  - job_name: federate
    scrape_interval: 60s
    scrape_timeout: 30s
    honor_labels: true
    metrics_path: /federate
    params:
      'match[]':
        - '{__name__=~"job:.*"}'          # aggregated recording rules only
        - '{job="prometheus"}'
    static_configs:
      - targets: ["prom-eu1:9090", "prom-us1:9090"]
```
Rules that keep it healthy:
- Federate **only recording rules** named for their aggregation level (`level:metric:op`).
  Never `{__name__=~".+"}`; that copies every series and every cardinality problem.
- Give source servers distinct `external_labels` (`cluster`, `region`) so global dashboards can group by them.
- Keep the federated `scrape_interval` at or above the source's rule `evaluation_interval`; faster just repeats values.
- Target the source servers directly, not a load balancer in front of an HA pair.

## 3. Cross-service federation
Pull a handful of series from another service's Prometheus so your rules and alerts can use both datasets in one
server (for example cluster resource usage for your service). Same config, narrower `match[]`.
Document ownership: when the other team renames a metric your alerts silently vanish. Alert on
`absent(federated_metric)`.

## 4. Federation vs remote_write vs Thanos/Mimir
| Need | Use |
|---|---|
| Global aggregated view, a few thousand series | federation |
| All raw series, long retention, HA dedupe, global PromQL | remote_write into Mimir / Thanos Receive, or Thanos Sidecar + Query |
| Querying across clusters without copying data | Thanos Query over sidecars |

Stop fighting federation when the `match[]` list grows past a screen.

## Gotchas
- Large federation scrapes hit `scrape_timeout` (default 10s globally); raise it on the federate job and watch
  `scrape_duration_seconds{job="federate"}`.
- `up{job="federate"}` only says the source answered, not that its rules are evaluating; check rule health on the
  source servers too.
- Float samples are federated as untyped; histogram samples keep their type. Native histograms need
  `scrape_native_histograms: true` on the federating scrape config.

## Verify
- [ ] `curl -g 'http://prom-eu1:9090/federate?match[]={__name__=~"job:.*"}'` returns hundreds or thousands of lines, not millions.
- [ ] Global server series count stays flat when a source cluster adds pods.
- [ ] Global dashboards group by `cluster` and show every source.

## Checked
2026-10-31. Confirmed against the Prometheus Federation page (`/federate`, required `match[]` selectors and their
union, hierarchical vs cross-service use cases, `honor_labels`, untyped float federation, `scrape_native_histograms`) and
the scrape_config reference (`honor_labels` renames to `exported_<label>`, `honor_timestamps` default true,
`scrape_timeout` default 10s; the Prometheus feature-flags page mentions `scrape_duration_seconds`). Removed: the claim that stale series appear as gaps after a source restart, the
claim that external labels are added to federated series, and the HA-pair flapping explanation (not on cited pages).
Method: documentation only; no commands were run.
