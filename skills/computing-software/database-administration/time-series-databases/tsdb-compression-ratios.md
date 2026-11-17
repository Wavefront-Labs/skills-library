---
id: computing-software.database-administration.time-series-databases.tsdb-compression-ratios
name: tsdb-compression-ratios
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-gen-sizing, tsdb-compression-ratios]
level: practitioner
status: draft
description: "Know realistic compression for each engine so storage estimates are credible."
sources:
  - https://prometheus.io/docs/prometheus/latest/storage/
  - https://docs.timescale.com/
  - https://docs.influxdata.com/influxdb/v2/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Compression ratios

**Goal:** Know realistic compression for each engine so storage estimates are credible.

## Steps
- Gorilla-style delta-of-delta timestamps and XOR floats give 1 to 2 bytes per sample in Prometheus and VictoriaMetrics (often under 1 byte on regular data).
- TimescaleDB native compression: commonly 90 percent size reduction (10x) on metrics, workload dependent; segmentby choice dominates.
- InfluxDB 2 TSM: roughly 2 to 4 bytes per point; InfluxDB 3 Parquet with zstd varies widely.
- ClickHouse: codecs `DoubleDelta`, `Gorilla`, `T64` with `ZSTD` give 5 to 20x on numeric series.
- Random floats and high-entropy values compress poorly; regular intervals compress well.
- Measure: load a sample day, compare uncompressed (`pg_total_relation_size`, `du`) to compressed.

**Gotcha:** Vendor ratios use clean, regular data; irregular timestamps and noisy sensors often compress at half the advertised ratio.

## Verify
- A one-day sample reports your own bytes per sample.
- Capacity plan uses the measured number, not the vendor claim.
