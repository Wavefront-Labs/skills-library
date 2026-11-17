---
id: computing-software.cloud-infrastructure-engineering.victoriametrics.victoriametrics-single-node-storage-and-retention
name: victoriametrics-single-node-storage-and-retention
category: computing-software
field: cloud-infrastructure-engineering
product: victoriametrics
tags: [single-node, retention-period, storage-data-path, snapshots, force-merge, deduplication, delete-series]
level: practitioner
status: docs-checked
description: "Configure single-node VictoriaMetrics storage path, retention, deduplication, snapshots, export, deletion and forced merges."
sources: ["https://docs.victoriametrics.com/victoriametrics/single-server-victoriametrics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Victoriametrics single node storage and retention

Single-node VictoriaMetrics listens on port 8428 by default.

- `-storageDataPath`: where all data lives (default `victoria-metrics-data` in the working directory).
- `-retentionPeriod`: old data is deleted automatically. Default is 1 month (31 days); minimum 24h. Enterprise adds `-retentionFilter` for per-series retention such as `'{team="juniors"}:3d'` and `-downsampling.period=offset:interval`.
- `-dedup.minScrapeInterval`: keeps one sample per interval when set to a positive duration; disabled by default. Needed when several vmagent or Prometheus replicas push identical data.
- Snapshots: `/snapshot/create`, `/snapshot/list`, `/snapshot/delete?snapshot=<name>`, `/snapshot/delete_all`, stored under `<-storageDataPath>/snapshots`; `-snapshotsMaxAge` deletes old ones. Archive them with vmbackup.
- Export: `/api/v1/export` (JSON line), `/api/v1/export/csv`, `/api/v1/export/native`, limited by `-search.maxExportDuration` and `-search.maxExportSeries`.
- Delete: `POST /api/v1/admin/tsdb/delete_series`, protected by `-deleteAuthKey` and capped by `-search.maxDeleteSeries`.
- Forced merge: `/internal/force_merge?partition_prefix=YYYY_MM` (auth `-forceMergeAuthKey`); forced flush: `/internal/force_flush` (`-forceFlushAuthKey`).
- Scraping: `-promscrape.config` points to a Prometheus-style file; `-promscrape.config.strictParse=false` ignores unsupported options.
- Flags from environment: `-envflag.enable`, optional `-envflag.prefix`; `%{ENV_VAR}` placeholders expand in flags and config files.

Ingestion protocols include Prometheus remote write, DataDog, InfluxDB line protocol, Graphite plaintext, OpenTelemetry HTTP, OpenTSDB, JSON-line and CSV import, and Prometheus exposition format.

## Checked

2026-11-03. Flags, endpoints, HTTP paths, defaults, limits and version gates were checked against the official VictoriaMetrics documentation pages cited in `sources` (docs.victoriametrics.com, fetched this batch) with a phrase-by-phrase comparison. No wrong claims were found; no claims were removed.

Method: documentation only; no commands were run.
