---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.upgrading-loki-2-to-3
name: upgrading-loki-2-to-3
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [loki-3-upgrade, loki-upgrade, schema-config, tsdb-shipper, structured-metadata]
level: advanced
status: gated
description: "Upgrade Loki 2.x to 3.x: move to TSDB index with schema v13, handle structured metadata defaults, removed config keys, Helm chart 6 changes and Promtail deprecation."
sources: ["https://grafana.com/docs/loki/latest/setup/upgrade/", "https://grafana.com/docs/loki/latest/operations/storage/schema/", "https://grafana.com/docs/loki/latest/setup/upgrade/upgrade-to-6x/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrading Loki 2.x to 3.x

## Schema first
Structured metadata (enabled by default in 3.x via `allow_structured_metadata: true`) requires the TSDB index and schema v13. Add a new period starting in the future (UTC, at least a day ahead):
```yaml
schema_config:
  configs:
    - {from: "2023-01-01", store: boltdb-shipper, object_store: s3, schema: v12, index: {prefix: index_, period: 24h}}
    - {from: "2026-11-01", store: tsdb, object_store: s3, schema: v13, index: {prefix: index_, period: 24h}}
```
Old periods stay readable. If you cannot add v13 yet, set `limits_config.allow_structured_metadata: false` to start 3.x.

## Config changes to review (upgrade guide)
- Removed keys: `shared_store` (tested: `field shared_store not found in type compactor.Config`; the index store now follows the period's `object_store`), legacy BoltDB settings deprecated (`boltdb-shipper` is being removed in Loki 4.0), defaults changed: `max_line_size` 256KB enforced, `max_label_names_per_series` 15 (was 30). Run the new binary with `-config.file=... -verify-config` (or `-print-config-stderr`) to see errors.
- Compactor retention needs `delete_request_store` set when retention is enabled.
- Service name discovery adds a `service_name` label automatically (`discover_service_name`); dashboards filtering exact label sets may change.

## Helm
The Loki upgrade page now says the chart moved to the grafana-community/helm-charts repository and chart numbering changed (6.x became 18.x); follow its "Upgrade to the Community Helm chart" guide. The chart-6.x values layout details (`deploymentMode`, `loki.schemaConfig`) were not checked (gated: unconfirmed, source is paywalled or blocked).

## Agents
Promtail reached end of life on 2 March 2026 (Loki docs); migrate to Alloy (`alloy convert --source-format=promtail`).

## Procedure
Staging first with production config; upgrade backend/compactor and ingesters (rolling), then read path (gated: unconfirmed, source is paywalled or blocked): the rollout order was not run here. Keep the 2.x image tag ready.

## Verify
- [ ] After the v13 `from` date, new index files appear under the TSDB prefix and queries spanning both periods work.

## Checked
Ran Loki 3.7.9 `-verify-config` on a TSDB v13 config with two periods (valid), with `compactor.shared_store` (unknown field), with retention enabled and no `delete_request_store` (error `delete-request-store should be configured when retention is enabled`), with schema v12 (error says set `allow_structured_metadata: false` or move to v13), and with an out-of-order `from` list (error `from time in schemas must be distinct and in increasing order`). Read the v3.7.9 docs source: setup/upgrade (3.0 breaking-changes list: structured metadata, `shared_store`, 256KB line size, 15 labels, `service_name`; Helm-chart move to the community repo), operations/storage/schema (new period needs a future `from`, boltdb-shipper deprecated), send-data/promtail (EOL 2 March 2026). `alloy convert --source-format=promtail` ran on Alloy v1.21.1. The rollout order and chart layout are gated as marked.
