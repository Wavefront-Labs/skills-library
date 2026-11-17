---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-tsdb-disk-sizing
name: prometheus-tsdb-disk-sizing
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [tsdb-disk-sizing, bytes-per-sample, tsdb, storage-retention, capacity-planning, prometheus]
level: practitioner
status: docs-checked
description: "Size Prometheus disk from ingested samples/s, retention and bytes per sample, plus WAL and compaction headroom, and set retention.size as a safety net."
sources: ["https://prometheus.io/docs/prometheus/latest/storage/#operational-aspects", "https://prometheus.io/docs/prometheus/latest/command-line/prometheus/", "https://prometheus.io/docs/prometheus/latest/storage/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TSDB disk sizing

The Prometheus storage docs give a rough capacity formula and state that Prometheus stores an average of only 1-2 bytes per sample:

`needed_disk_space = retention_time_seconds * ingested_samples_per_second * bytes_per_sample`

Take ingested samples per second and bytes per sample from your own server, rather than assuming the 1-2 byte average.

## Worked example (illustrative numbers)
200k samples/s x 30d (2,592,000 s) x 1.5 bytes = about 778 GB of blocks.
Add headroom for:
- WAL: raw, not yet compacted data, so significantly larger than regular block files. WAL files are 128MB segments; at least three are kept, and high-traffic servers may keep more to hold at least two hours of raw data. `--storage.tsdb.wal-compression` is enabled by default since 2.20.0 and can roughly halve WAL size.
- Compaction: the source blocks and the new compacted block coexist on disk, so on-disk size can briefly exceed the retention size. Compacted blocks span up to 10% of the retention time or 31 days, whichever is smaller.
- Retention size buffer: the docs recommend setting retention size to at most 80-85% of the allocated disk, leaving 15-20% for in-progress compactions.
Result for the example: provision about 1.2 TB and set `--storage.tsdb.retention.size=1TB` (about 83%, inside the 80-85% guidance).

## Retention flags
- `--storage.tsdb.retention.time` (default 15d if neither it nor the size flag is set; units y, w, d, h, m, s, ms) and `--storage.tsdb.retention.size` (default 0, disabled; units B, KB, MB, GB, TB, PB, EB, powers of 2). If both are set, whichever triggers first is used.
- The command-line reference marks both flags as deprecated in favour of the `storage.tsdb.retention.time` and `storage.tsdb.retention.size` fields in the configuration file.
- Only persistent blocks are deleted to honour size retention, but the WAL and m-mapped chunks are counted in the total size. The minimum disk requirement is therefore the peak space of the `wal` (WAL and checkpoint) and `chunks_head` directories combined, which peaks every 2 hours.
- Expired block cleanup runs in the background and may take up to two hours; a block must be fully expired before removal.

## Gotchas
- To lower the ingested sample rate, scraping fewer series is likely more effective than increasing the scrape interval, because samples within a series compress well.
- Non-POSIX filesystems are not supported for local storage (unrecoverable corruption may happen); NFS, including AWS EFS, is not supported. Use a local filesystem.
- Local storage is not clustered or replicated; snapshots are recommended for backups.

## Checked
Date: 2026-11-07.
Read in full: the Storage page (on-disk layout, compaction, Operational aspects, Right-Sizing Retention Size, filesystem caution) and the Prometheus command-line page (retention and WAL flags, deprecation notes).
Confirmed: the capacity formula, 1-2 bytes per sample, 128MB WAL segments with at least three kept, WAL compression since 2.20.0 enabled by default, compaction up to 10% of retention or 31 days, retention flag defaults and units, the 80-85% advice, the WAL and m-mapped chunks counting towards size retention, and the NFS/EFS caution. The worked-example arithmetic was recomputed (200,000 x 2,592,000 x 1.5 = about 778 GB).
Removed because no cited page confirms them: all four PromQL metric names (`prometheus_tsdb_*`), the WAL "5-15% extra" and "2-3 h" figures, the "10-20% free" and 6-12 month growth rules, the churn and native histogram gotchas, the claim that a full disk corrupts the WAL, the `node_filesystem_avail_bytes` alert, and the invented Verify checklist.
Method: documentation only; no commands were run.
