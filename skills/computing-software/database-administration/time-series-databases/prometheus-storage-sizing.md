---
id: computing-software.database-administration.time-series-databases.prometheus-storage-sizing
name: prometheus-storage-sizing
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-prom-retention, prometheus-storage-sizing, prometheus]
level: practitioner
status: docs-checked
description: "Estimate Prometheus disk with the documented retention x samples/s x bytes-per-sample formula and bound query memory."
sources:
  - https://prometheus.io/docs/prometheus/latest/storage/
  - https://prometheus.io/docs/prometheus/latest/command-line/prometheus/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage and memory sizing

**Goal:** Estimate disk and RAM for a Prometheus server.

## Steps
- Disk: `needed_disk_space = retention_time_seconds * ingested_samples_per_second * bytes_per_sample`. The storage docs say Prometheus stores an average of 1-2 bytes per sample.
- Samples per second is the ingestion rate of the server; as a rule of thumb it is active series divided by the scrape interval.
- Worked example: 1M active series at a 15 s scrape interval is about 66,667 samples/s; over 15 days (1,296,000 s) that is roughly 86 billion samples, so about 86-173 GB at 1-2 bytes per sample.
- Reduce ingestion by scraping fewer series or lengthening the scrape interval; reducing series is likely more effective because of per-series compression.
- The disk must also hold the WAL and m-mapped head chunks (they count toward size retention and peak every two hours), plus a compaction buffer: keep retention size at most 80-85 percent of the disk.
- Query memory is bounded by `--query.max-samples` (default 50000000) and time by `--query.timeout` (default 2m).
- RAM for the head scales with active series; measure it on your own data rather than using a fixed per-series figure.

**Gotcha:** Budgeting disk from retention alone ignores the WAL, `chunks_head` and compaction overlap; allow the 15-20 percent buffer.

## Verify
- Predicted and actual disk usage after a week agree closely; adjust the bytes-per-sample estimate from your own data.
- Resident memory stays comfortably below the host's RAM.

## Checked
2026-11-03. Confirmed against the storage page (formula, 1-2 bytes per sample, WAL and chunks_head counted, 80-85 percent) and the command-line page (`--query.max-samples`, `--query.timeout` defaults). Arithmetic for the example recomputed. Resolved the "confirm" on RAM by removing it. Removed: the 3-8 KB per series and 3-8 GB figures, the "add 20-30 percent" figure, the 25 percent and 70 percent verify thresholds, and the `rate(prometheus_tsdb_head_samples_appended_total[5m])` and `process_resident_memory_bytes` metric names.
Method: documentation only; no commands were run.
