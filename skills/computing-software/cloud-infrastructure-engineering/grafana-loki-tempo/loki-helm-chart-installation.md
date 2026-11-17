---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.loki-helm-chart-installation
name: loki-helm-chart-installation
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [loki-helm-chart, loki, helm, simple-scalable, singlebinary, distributed-mode, grafana-helm-repo]
level: practitioner
status: docs-checked
description: "Install Loki with the community Helm chart in monolithic or distributed mode, with the repo move and deprecations."
sources: ["https://grafana.com/docs/loki/latest/setup/install/helm/", "https://grafana.com/docs/loki/latest/setup/install/helm/install-monolithic/", "https://grafana.com/docs/loki/latest/setup/install/helm/install-microservices/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: a working Loki on Kubernetes with a supported chart and object storage.

Since March 2026 the Loki chart is maintained by the Grafana community in the grafana-community/helm-charts repo, and the install pages use that repo:
```
helm repo add grafana-community https://grafana-community.github.io/helm-charts
helm repo update
helm install loki grafana-community/loki -f values.yaml -n loki --create-namespace
helm upgrade --values values.yaml loki grafana-community/loki -n loki
```
Prerequisites on the install page: Helm 3 or above, Kubernetes 1.25 or later.

Modes
- Monolithic (small or meta-monitoring stacks): set `deploymentMode: Monolithic`. As of community chart 12.0.0 `SingleBinary` was renamed `Monolithic`; the old value still works but is deprecated. Keys such as `singleBinary.replicas` remain in the page's examples. With one replica you must set `loki.commonConfig.replication_factor: 1`, or requests fail. The docs recommend at least three replicas for high availability.
- Microservices (HA and scale): `deploymentMode: Distributed`, with the other modes' replica counts zeroed as in the page's examples.
- Simple Scalable mode is being deprecated; the docs recommend microservices for production.

A schema block from the monolithic example:
```yaml
loki:
  commonConfig:
    replication_factor: 1
  schemaConfig:
    configs:
      - from: "2024-04-01"
        store: tsdb
        object_store: s3
        schema: v13
        index:
          prefix: loki_index_
          period: 24h
```
Copy the rest of the values from the page for your mode; the chart deploys the gateway (NGINX), Loki Canary, and chunks and results caches.

Gotchas
- The built-in MinIO subchart is deprecated and scheduled for removal on 2026-10-31; with chart v17+ rendering fails unless `ignoreMinioDeprecation: true` is set. Use external object storage (S3, GCS or Azure Blob) for production, and do not run microservices mode on filesystem storage.
- Chart values change between major versions (a major version signals breaking changes); read the chart README and values reference before upgrading.

## Verify
```
kubectl get pods -n loki
```
All Loki pods reach Running; `GET /ready` returns HTTP 200 once Loki accepts traffic.

## Checked
2026-11-03. Confirmed against the Loki Helm install overview, monolithic and microservices install pages (repo name, commands, Monolithic rename, replication factor note, MinIO deprecation). Corrected: old repo `grafana/loki` and `SingleBinary`/filesystem example replaced with the community repo and `Monolithic`. Removed: `loki.storage.type: s3`, `lokiCanary` and `test` toggles, `helm show values`, the 50Gi PVC and WAL claims (not on the pages read).
Method: documentation only; no commands were run.
