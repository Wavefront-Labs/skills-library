---
id: computing-software.cloud-infrastructure-engineering.grafana-mimir.grafana-mimir-scaling-out-and-in
name: grafana-mimir-scaling-out-and-in
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-mimir
tags: [scaling, scale-down, ingesters, alertmanager, store-gateway]
level: advanced
status: docs-checked
description: "Explains how to scale Mimir components safely, especially scaling down ingesters in classic and ingest storage architectures and Alertmanagers."
sources: ["https://grafana.com/docs/mimir/latest/manage/run-production-environment/scaling-out/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Scaling Mimir

Every component scales horizontally. Scaling up is safe in monolithic and microservices mode. Stateless components can also be scaled down safely. Stateful ones (Alertmanagers, ingesters, store-gateways) need care, since scaling down can cause write or read failures or partial query results.

## Alertmanagers

Scale down at most two at once, and keep at least `-alertmanager.sharding-ring.replication-factor` instances (three by default). With zone awareness you can scale down any number inside one zone at a time.

## Ingesters, ingest storage

Scaling down reassigns ingestion partitions instead of transferring in-memory series. Data is durable in Kafka and object storage, so no draining is needed. The rollout-operator, deployed by the Helm chart, normally coordinates this by preparing ingesters for shutdown. Manually, use GET, POST or DELETE on `/ingester/prepare-partition-downscale`.

## Ingesters, classic

Ingesters hold recent samples in memory and by default do not upload them on shutdown, so data can be lost. Procedure on the page: POST `/ingester/prepare-instance-ring-downscale` on each ingester (read-only mode); wait until their uploaded blocks are queryable (the maximum of `-querier.query-store-after`, twice `-blocks-storage.bucket-store.sync-interval` and twice `-compactor.cleanup-interval`); then POST `/ingester/shutdown`, which flushes in-memory data to long-term storage and unregisters the ingester so it takes no reads or writes, and finally send `SIGINT` or `SIGTERM`. Uploaded blocks are not instantly queryable, so scaling down two or more ingesters in a short period can give partial query results.

## Checked

2026-11-04. Confirmed against the Mimir page "Scaling out Grafana Mimir" (Alertmanager, ingest storage and classic ingester sections). Removed the claim that the classic prepare endpoint returns 405 in ingest storage mode (not on the page). Store-gateway scale-down is not covered by this skill.
Method: documentation only; no commands were run.
