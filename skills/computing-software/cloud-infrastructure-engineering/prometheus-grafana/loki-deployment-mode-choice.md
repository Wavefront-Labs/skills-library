---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.loki-deployment-mode-choice
name: loki-deployment-mode-choice
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [loki-deployment-modes, monolithic-loki, simple-scalable, microservices-mode, loki-helm-chart]
level: practitioner
status: docs-checked
description: "Choose Loki monolithic, simple scalable or microservices (distributed) mode by volume and ops capacity, and map each to Helm deploymentMode and targets."
sources: ["https://grafana.com/docs/loki/latest/get-started/deployment-modes/", "https://grafana.com/docs/loki/latest/setup/install/helm/", "https://grafana.com/docs/loki/latest/get-started/components/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loki deployment modes

All modes run the same binary with different `-target` values.

| Mode | Targets | Rough fit (docs guidance) | Notes |
|---|---|---|---|
| Monolithic | `-target=all` (single binary; HA with two instances, memberlist, shared object store, `replication_factor` 3) | small volume, up to approximately 20GB per day | simplest; the docs recommend microservices if you need to scale |
| Simple scalable (SSD) | `write`, `read`, `backend` | can scale close to a TB of logs per day | being deprecated and removed with Loki 4.0; plan to migrate to microservices or HA monolithic |
| Microservices (distributed) | `distributor`, `ingester`, `querier`, `query-frontend`, `query-scheduler`, `index-gateway`, `compactor`, `ruler`, plus experimental bloom planner/builder/gateway | very large clusters or precise scaling control | most complex to set up and maintain; designed for Kubernetes |

## Helm
```yaml
deploymentMode: Monolithic          # or SimpleScalable, Distributed (SingleBinary is the deprecated legacy name, renamed in community chart 12.0.0)
loki:
  commonConfig: {replication_factor: 3}
  storage: {type: s3, bucketNames: {chunks: loki-chunks, ruler: loki-ruler}}
  schemaConfig:
    configs:
      - {from: "<YYYY-MM-DD>", store: tsdb, object_store: s3, schema: v13, index: {prefix: index_, period: 24h}}
singleBinary: {replicas: 3}
```
Distributed: set `ingester.replicas`, `querier.replicas`, etc., and set `backend.replicas`, `read.replicas` and `write.replicas` to 0. With a single replica, set `commonConfig.replication_factor: 1`.

## Decision factors
- Query load spikes (big dashboards, Explore): separate read path (SSD/microservices) so queries do not starve ingestion.
- Team capacity: microservices means many components to monitor (use the Loki mixin).
- Scaling beyond one instance needs a shared object store.

## Migration
Loki decouples stored data from the software that ingests and queries it, so a cluster can be redeployed under a different mode with minimal or no configuration changes.

## Verify
- [ ] Ingest and query SLOs met at peak with headroom; components scale independently where needed.

## Checked
- 2026-10-28. Confirmed against the Loki deployment modes page (20GB per day for monolithic, HA with two instances, SSD close to a TB per day, SSD deprecation and Loki 4.0 removal, `write`/`read`/`backend` target contents, microservices component list, experimental bloom components) and the Helm monolithic and microservices install pages (`deploymentMode: Monolithic|Distributed`, SingleBinary renamed in community chart 12.0.0, `schema: v13`, `period: 24h`, `commonConfig.replication_factor`, `singleBinary.replicas`, zeroed `backend`/`read`/`write` replicas).
- Removed: the "few TB/day" SSD figure (the docs say close to a TB), a concrete schema date, and the migration side-by-side advice.
Method: documentation only; no commands were run.
