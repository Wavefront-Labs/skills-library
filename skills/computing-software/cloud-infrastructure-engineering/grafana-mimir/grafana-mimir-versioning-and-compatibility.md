---
id: computing-software.cloud-infrastructure-engineering.grafana-mimir.grafana-mimir-versioning-and-compatibility
name: grafana-mimir-versioning-and-compatibility
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-mimir
tags: [versioning, compatibility, deprecation, experimental-features, api-compatibility]
level: intro
status: docs-checked
description: "Summarises Mimir versioning guarantees: deprecation window, reading old data, Prometheus API compatibility and the status of experimental features."
sources: ["https://grafana.com/docs/mimir/latest/configure/about-versioning/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Versioning and compatibility guarantees

## Upgrades

Upgrading from one minor version to the next should work. Mimir does not bump the major version for each removed parameter; deprecated features stay for two minor releases. The `deprecated_flags_inuse_total` metric can drive an alert for deprecated flags in use. These guarantees do not apply to experimental features.

## Reading old data

Maintainers commit that future versions can read data written within the last two years.

## API compatibility

Mimir aims for 100% compatibility with the Prometheus HTTP API, served under the `/prometheus/*` prefix. Deviations are treated as bugs, except: extra endpoints to create, remove or modify alerts and recording rules; extra push APIs (under `/prometheus/api/push`); management endpoints such as the ring, which carry no compatibility guarantee; and the Delete series API.

## Experimental features

Anything not considered production-ready is marked Experimental, with no backwards-compatibility guarantee. Examples the page lists as experimental include owned series tracking (`-ingester.track-ingester-owned-series`), out-of-order ingestion (`-ingester.out-of-order-time-window`) and the per-tenant `limited_queries` limit. Check the stability label before relying on a flag in production.

## Checked

Confirmed against the page: two-minor-release deprecation window, `deprecated_flags_inuse_total`, two-year read guarantee, Prometheus API compatibility and its exceptions, experimental status. Removed the claim that TSDB block upload is experimental (not listed on the page).

Method: docs-checked 2026-11-09 against the raw markdown of the Mimir about-versioning page (grafana/mimir main), read in full.
