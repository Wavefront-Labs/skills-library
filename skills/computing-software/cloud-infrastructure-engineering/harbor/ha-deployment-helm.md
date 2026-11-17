---
id: computing-software.cloud-infrastructure-engineering.harbor.ha-deployment-helm
name: ha-deployment-helm
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [high-availability, helm, external-postgresql, external-redis, readwritemany]
level: advanced
status: docs-checked
description: "Deploy Harbor HA on Kubernetes with Helm: external PostgreSQL and Redis, shared storage, externalURL and the chart values to set."
sources:
  - https://goharbor.io/docs/main/install-config/harbor-ha-helm/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Most Harbor components are stateless, so HA means raising pod replicas and supplying HA data services yourself.

Prerequisites: Kubernetes 1.10+, Helm 2.8.0+, a highly available ingress controller, highly available PostgreSQL 9.6+, highly available Redis, and a PVC shareable across nodes or external object storage. Harbor does not deploy HA for the database or Redis, and does not support Redis Cluster or TLS connections to Redis.

Get the chart: `helm repo add harbor https://helm.goharbor.io` then `helm fetch harbor/harbor --untar`.

Set in `values.yaml` or with `--set`:
- `expose.ingress.hosts.core`: the ingress URL.
- `externalURL`: used for the docker and helm commands in the portal and the token service URL. Must be a domain root such as `harbor.example.com`; running on a path is not supported.
- External PostgreSQL: `database.type: external` and fill `database.external`. Create an empty database; the default name is `registry`, changeable with `coreDatabase`.
- External Redis: `redis.type: external` and fill `redis.external`. Sentinel mode is supported since 2.1.0 by setting `sentinelMasterSet` and `host` as comma-separated `<host>:<port>` pairs.
- Storage: use a StorageClass that supports `ReadWriteMany`, set at `persistence.persistentVolumeClaim.registry.storageClass` and `.jobservice.storageClass`, with `accessMode` `ReadWriteMany` on both. Alternatively use `existingClaim`.

## Checked

- 2026-11-03: concrete claims (parameter names, defaults, steps, limits, UI labels) read against the official Harbor docs: Deploying Harbor with High Availability via Helm.
Method: documentation only; no commands were run.
