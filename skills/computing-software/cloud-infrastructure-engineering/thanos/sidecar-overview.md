---
id: computing-software.cloud-infrastructure-engineering.thanos.sidecar-overview
name: sidecar-overview
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-sidecar, prometheus-sidecar, storeapi, block-upload]
level: intro
status: docs-checked
description: "Run thanos sidecar beside Prometheus to expose its data over StoreAPI and optionally ship blocks to object storage."
sources: ["https://thanos.io/tip/components/sidecar.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sidecar overview

`thanos sidecar` is deployed with each Prometheus instance. It implements the Store API on top of Prometheus's remote-read API, so Queriers treat Prometheus as another source. Optionally it uploads TSDB blocks to object storage as Prometheus produces them (every 2 hours).

For sidecar upload, Prometheus must run with equal min and max block durations (local compaction disabled); `--web.enable-lifecycle` is needed for the sidecar reload features:

```
prometheus \
  --storage.tsdb.max-block-duration=2h \
  --storage.tsdb.min-block-duration=2h \
  --web.enable-lifecycle

thanos sidecar \
  --tsdb.path "/path/to/prometheus/data/dir" \
  --prometheus.url "http://localhost:9090" \
  --objstore.config-file "bucket.yml"
```

**Defaults.** `--prometheus.url=http://localhost:9090` (use a local network for performance), `--prometheus.ready_timeout=10m`, `--prometheus.get_config_interval=30s`, gRPC on `0.0.0.0:10901`, HTTP on `0.0.0.0:10902`, `--shipper.meta-file-name=thanos.shipper.json`.

Omit `--objstore.config*` to run query-only without uploads. `--min-time` and `--max-time` limit the range the sidecar serves.

## Checked

2026-11-03. Confirmed against the Thanos Sidecar page (components/sidecar.md) and the Thanos troubleshooting page: Store API over remote-read, 2h upload, block-duration requirement for upload, reloader flags, HTTP client config, upload-compacted, defaults. Fixed: the 2h fixed-block requirement applies to sidecar upload only. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
