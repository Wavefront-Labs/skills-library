---
id: computing-software.cloud-infrastructure-engineering.grafana-mimir.grafana-mimir-owned-series-tracking
name: grafana-mimir-owned-series-tracking
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-mimir
tags: [owned-series, ingester, series-limits, autoscaling, experimental]
level: sme
status: docs-checked
description: "Explains Mimir experimental owned series tracking, which counts only series an ingester owns so limits stay correct when scaling ingesters or shard sizes."
sources: ["https://grafana.com/docs/mimir/latest/configure/configure-owned-series/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Owned series tracking

Experimental (Mimir 2.12 and later). Problem: each ingester enforces a fraction of a tenant's in-memory series limit. If a tenant limit is 150k across 3 ingesters (50k each) and the tenant has about 30k per ingester, then moving to 6 ingesters or a larger shuffle shard drops the local limit to 25k, and the original ingesters immediately start discarding samples because stale series remain in memory.

## How it works

A series is owned by an ingester if the hash of its labels and tenant ID falls in a token range the ingester owns (in ingest storage, tokens belong to partitions). Each ingester counts per-tenant owned series. Every `ingester.owned-series-update-interval` the service checks if recomputation is needed after shard size changes, local limit changes, token range changes or compaction. A recomputation triggered by a limit decrease finishes before the lower limit takes effect; increases apply immediately. The count also gives autoscalers feedback quickly after ring changes.

## Classic architecture prerequisites

Enable zone-aware replication and set the replication factor equal to the number of zones. These are not needed with ingest storage.

## Enable

```text
-ingester.track-ingester-owned-series=true
```

then configure the interval and the limit settings described on the Mimir page. Because the feature is experimental, expect changes without backwards-compatibility guarantees.

## Checked

Confirmed against the page: experimental since 2.12, the 150k/3 to 6 ingesters example, ownership by token range, update interval and recomputation triggers, limit decrease versus increase behaviour, classic-only prerequisites, the enable flag. Nothing removed.

Method: docs-checked 2026-11-09 against the raw markdown of the Mimir configure-owned-series page (grafana/mimir main), read in full.
