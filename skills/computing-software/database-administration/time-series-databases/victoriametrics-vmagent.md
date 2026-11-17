---
id: computing-software.database-administration.time-series-databases.victoriametrics-vmagent
name: victoriametrics-vmagent
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-prom-victoriametrics, victoriametrics-vmagent, prometheus, victoriametrics]
level: practitioner
status: draft
description: "Use vmagent as a lightweight scraper and remote-write forwarder with buffering."
sources:
  - https://docs.victoriametrics.com/
  - https://prometheus.io/docs/prometheus/latest/storage/
  - https://prometheus.io/docs/introduction/overview/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# vmagent and relabeling

**Goal:** Use vmagent as a lightweight scraper and remote-write forwarder with buffering.

## Steps
- `vmagent -promscrape.config=prometheus.yml -remoteWrite.url=http://vm:8428/api/v1/write`.
- It buffers to disk during outages (`-remoteWrite.tmpDataPath`, `-remoteWrite.maxDiskUsagePerURL`).
- Multiple destinations: repeat `-remoteWrite.url` and use `-remoteWrite.urlRelabelConfig` per URL.
- Reduce cardinality via `-remoteWrite.streamAggr.config` stream aggregation, `-remoteWrite.relabelConfig`.
- Accepts many ingestion protocols (Prometheus, InfluxDB, OpenTSDB, Graphite), useful as a gateway.
- Check targets at the vmagent UI (`/targets`) and config reload with `kill -HUP` or `/-/reload`; per-target relabel debugging is at `/target-relabel-debug`.
- Sharding scrape across vmagents with `-promscrape.cluster.membersCount` and `-promscrape.cluster.memberNum`.

**Gotcha:** Disk buffer limits drop the oldest data when exceeded; size it to your longest tolerated outage.

## Verify
- `vmagent_remotewrite_pending_data_bytes` returns to near zero after an outage.
- Series show in VM with correct labels.
