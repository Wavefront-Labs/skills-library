---
id: computing-software.data-engineering.trino.trino-openmetrics-kubernetes-scraping
name: trino-openmetrics-kubernetes-scraping
category: computing-software
field: data-engineering
product: trino
tags: [kubernetes-scraping, helm-chart, prometheus-relabel, coordinator-metrics, worker-metrics]
level: advanced
status: docs-checked
description: "Scrape both Trino coordinator and worker pods on Kubernetes with Helm chart annotations and Prometheus relabelling, including dropping granular metrics."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/openmetrics.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino openmetrics kubernetes scraping

To see the whole cluster you must scrape the coordinator and every worker. With the Trino Helm chart, annotate both so Prometheus can discover them:

```yaml
coordinator:
  annotations:
    prometheus.io/trino_scrape: "true"
worker:
  annotations:
    prometheus.io/trino_scrape: "true"
```

Then define two Prometheus jobs, `trino-metrics-worker` and `trino-metrics-coordinator`, each with `kubernetes_sd_configs` of role `pod` and a 10s interval and timeout. Key relabel steps from the docs:
- keep only pods whose annotation `__meta_kubernetes_pod_annotation_prometheus_io_trino_scrape` is `true`;
- keep only container `trino-worker` (or `trino-coordinator`) so sidecars are not scraped;
- a `hashmod` of `__address__` over `$(SHARDS)` and keeping `$(SHARD)` to split scraping across Prometheus shards;
- copy pod and container names into `pod` and `container` labels.

Reduce cardinality with `metric_relabel_configs` that drop names matching `.+_FifteenMinute.+|.+_FiveMinute.+|.+IterativeOptimizer.+|.*io_airlift_http_client_type_HttpClient.+`.

Authentication differs. Workers: scheme `http`, a `basic_auth` username with system information permission and deliberately no password. Coordinator: scheme `https`, a username plus `password_file`, and a relabel rule replacing `__address__` with the HTTPS ingress address. The sample sets `insecure_skip_verify: true` in `tls_config`, which you should replace with proper CA trust in production.

## Checked

2026-11-04. Read against the Trino docs page `admin/openmetrics.md` (GitHub source of the public docs): property names, defaults, allowed values, error messages, examples and behaviour described above match it. Nothing needed removing.
Method: documentation only; no commands were run.
