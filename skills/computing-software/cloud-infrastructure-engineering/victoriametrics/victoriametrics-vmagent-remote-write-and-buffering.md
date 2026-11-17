---
id: computing-software.cloud-infrastructure-engineering.victoriametrics.victoriametrics-vmagent-remote-write-and-buffering
name: victoriametrics-vmagent-remote-write-and-buffering
category: computing-software
field: cloud-infrastructure-engineering
product: victoriametrics
tags: [vmagent, remote-write, disk-buffer, relabel-config, cardinality-limits, multi-tenancy]
level: practitioner
status: docs-checked
description: "Configure vmagent remote write destinations, on-disk buffering, relabeling order, label limits and tenant routing."
sources: ["https://docs.victoriametrics.com/victoriametrics/vmagent/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Victoriametrics vmagent remote write and buffering

vmagent collects metrics (scraping or push on port 8429, for example `/api/v1/write` and `/opentelemetry/v1/metrics`) and forwards them to remote storage.

- `-remoteWrite.url`: destination; repeat it to replicate to several. Cluster form: `<schema>://<vminsert-host>:8480/insert/<accountID>/prometheus/api/v1/write`.
- `-remoteWrite.forceVMProto` / `-remoteWrite.forcePromProto` choose the protocol per URL; `-remoteWrite.vmProtoCompressLevel` (default 0, range -22 to 22).
- `-remoteWrite.label` adds labels to everything sent; `-remoteWrite.tlsServerName` sets SNI for `dns+` URLs.
- Disk buffering: if remote storage is down, data is buffered at `-remoteWrite.tmpDataPath`; cap it with `-remoteWrite.maxDiskUsagePerURL`; `-remoteWrite.disableOnDiskQueue` turns the queue off (on by default).
- Limits: `-remoteWrite.maxHourlySeries`, `-remoteWrite.maxDailySeries`, `-maxIngestionRate`, `-maxLabelsPerTimeseries`, `-maxLabelNameLen`, `-maxLabelValueLen`.
- Relabeling: `-remoteWrite.relabelConfig` is global and applies before sharding and replication; `-remoteWrite.urlRelabelConfig` is per URL and flag order matters (first config goes to first URL).
- Multi-tenancy: `-enableMultitenantHandlers`, point `-remoteWrite.url` at `/insert/multitenant/...`, and use labels `vm_account_id` and `vm_project_id`; unspecified tenant is `0:0`.
- Kubernetes: headless Services work with `dns+` URLs for client-side load balancing.

Self-monitoring metrics include `up`, `scrape_duration_seconds`, `scrape_samples_scraped`, `scrape_series_added` and `scrape_series_limit_samples_dropped`.

## Checked

2026-11-03. Flags, endpoints, HTTP paths, defaults, limits and version gates were checked against the official VictoriaMetrics documentation pages cited in `sources` (docs.victoriametrics.com, fetched this batch) with a phrase-by-phrase comparison. No wrong claims were found; no claims were removed.

Method: documentation only; no commands were run.
