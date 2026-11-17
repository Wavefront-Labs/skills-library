---
id: computing-software.messaging-and-integration.apache-zookeeper.prometheus-metrics-provider
name: prometheus-metrics-provider
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, prometheus, metrics, metricsprovider, grafana, monitoring]
level: practitioner
status: docs-checked
description: "Expose ZooKeeper metrics to Prometheus with PrometheusMetricsProvider on port 7000, scrape setup, the Grafana data source and the InfluxDB/Telegraf alternative."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperMonitor.html
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prometheus metrics

- The new metrics system, available since 3.6.0, covers znode, network, disk, quorum, leader election, client, security, failures, watch/session and request processor metrics; all are in `ServerMetrics.java`.
- Enable in `zoo.cfg`: `metricsProvider.className=org.apache.zookeeper.metrics.prometheus.PrometheusMetricsProvider`.
- `metricsProvider.httpPort` defaults to 7000 (the endpoint is `http://hostname:httpPort/metrics`); `metricsProvider.httpHost` defaults to 0.0.0.0 (new in 3.8.0); `metricsProvider.exportJvmInfo` defaults to true.
- Point the Prometheus scrape config at each server's metrics port. The guide's example uses `scrape_interval: 10s` and targets such as `192.168.10.32:7000`, with Prometheus listening on `:9090`.
- Grafana has built-in Prometheus support: add a Prometheus data source (the guide uses Type Prometheus, Url `http://localhost:9090`, Access proxy), then download and import the default ZooKeeper dashboard template and customise it.
- InfluxDB: configure the Apache ZooKeeper Telegraf plugin; an Apache ZooKeeper InfluxDB template includes the Telegraf configuration and a dashboard.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Monitor Guide (Prometheus, Grafana, InfluxDB) and the Administrator's Guide metricsProvider options. Removed: Grafana dashboard ID 10465 (not given on the cleaned page text) and the Prometheus "targets page" verify step.
