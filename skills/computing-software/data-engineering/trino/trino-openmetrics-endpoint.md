---
id: computing-software.data-engineering.trino.trino-openmetrics-endpoint
name: trino-openmetrics-endpoint
category: computing-software
field: data-engineering
product: trino
tags: [openmetrics, prometheus, metrics-endpoint, openmetrics-jmx-object-names, scrape]
level: practitioner
status: docs-checked
description: "Scrape Trino metrics from the /metrics OpenMetrics endpoint, select JMX object names to expose, and run a Docker plus Prometheus demo."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/openmetrics.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino openmetrics endpoint

Trino exposes OpenMetrics (the standard that grew out of Prometheus) automatically at `/metrics` on each node. The endpoint uses the same authentication as the Web UI and client protocol. Test an unsecured server with:

```shell
curl -H X-Trino-User:foo localhost:8080/metrics
```

On a secured deployment the user needs read permission on system information. Every node, coordinator and workers, serves its own metrics independently.

Choose what is exported with `openmetrics.jmx-object-names` in `config.properties`. Separate object names with `|`. Names use the package namespace; `:*` exposes everything, `name` selects classes, `type` selects metric types. Examples from the docs:
- `trino.plugin.exchange.filesystem:name=FileSystemExchangeStats`
- `trino.plugin.exchange.filesystem.s3:name=S3FileSystemExchangeStorageStats`
- `io.trino.hdfs:*`
- `java.lang:type=Memory`

Local demo: create a Docker network `platform`, run `trinodb/trino:latest` with alias `trino` and port 8080, then run `prom/prometheus` on the same network with a mounted `prometheus.yml`:

```yaml
scrape_configs:
- job_name: trino
  basic_auth:
    username: trino-user
  static_configs:
    - targets:
      - trino:8080
```

Run a query, then in the Prometheus UI graph `trino_execution_name_QueryManager_RunningQueries`. Trino also has a Prometheus connector to query Prometheus data with SQL. Grafana Alloy or the Grafana agent with Cortex or Mimir storage are alternatives.

## Checked

2026-11-09. Pages read in full against this skill:
- https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/openmetrics.md

Confirmed (page read as raw markdown): /metrics endpoint and its authentication, system information permission, per-node metrics, openmetrics.jmx-object-names syntax and examples, and the Prometheus demo config. The Kubernetes scrape sections were read but are not covered by this skill.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
