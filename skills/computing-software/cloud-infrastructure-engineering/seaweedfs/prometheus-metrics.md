---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.prometheus-metrics
name: prometheus-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [prometheus, metricsport, push-gateway, metrics-port]
level: practitioner
status: docs-checked
description: "Expose SeaweedFS metrics to Prometheus by push (-master.metrics.address) or pull (-metricsPort per server) and graph them in Grafana."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/System-Metrics
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# prometheus metrics

Pull: give each server its own port and scrape it.
```bash
weed master -metricsPort=1235
weed volume -metricsPort=1236
weed filer  -metricsPort=1237
weed server -metricsPort=1234
```
Push through a Prometheus Push Gateway (master gives the address to filers and volume servers, which report directly):
```bash
weed master -master.metrics.address=localhost:9091
weed server -master.metrics.address=https://example.com
```
Set it on every master if you run several. `localhost:9091` defaults to http://localhost:9091. Filers and volume servers read the setting from the master and must be restarted for it to take effect.

Flow: master / volume / filer, then Push Gateway, Prometheus server, Grafana. For pull, configure Prometheus to crawl the ports periodically.

Maintenance workers publish their own metrics when started with a metrics port (`weed worker -metricsPort=9328`), serving `/health`, `/ready` and `/metrics`. The page gives the port convention master 9324, volume 9325, filer 9326, s3 9327, and names a `SeaweedFS_worker_*` metric family (for example `SeaweedFS_worker_jobs_total`, `SeaweedFS_worker_objects_seen_total` and `_objects_skipped_total`). A shared Grafana dashboard JSON is in the repo under `other/metrics`.

Gotcha: all servers need different metrics ports.

## Checked

2026-11-08. Confirmed against the System Metrics wiki page. Removed the unsupported S3 gateway metric name and the curl verification; added restart, worker metrics and dashboard notes.

Method: documentation only; no commands were run.
