---
id: computing-software.systems-network-administration.backup-and-recovery.restore-throughput-benchmarking
name: restore-throughput-benchmarking
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [restore-throughput, restore-testing, rto, backup-performance, bottleneck-analysis, recovery-testing]
level: advanced
status: docs-checked
description: "Benchmark restore throughput to prove RTO: time restores end to end, find the bottleneck, use restic restore options, and extrapolate honestly."
sources:
  - https://restic.readthedocs.io/en/stable/050_restore.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Restore throughput benchmarking

**Goal:** a measured restore rate per system type so RTOs are evidence, not hope.

## Measure
- Time the full restore end to end: start of request to service usable. Record data size, wall time, MB/s, and how many restores ran at once.
- Test from each storage tier you actually use (local disk repository, appliance, object storage, tape, archive tier).
- Compare the same data restored whole and restored partially, because the restore scope changes the time.

## Find the bottleneck
Check each stage in turn: repository read, network between repository or proxy and target, the CPU of whatever decompresses or decrypts, and write speed on the target. Use your backup product's job statistics where it reports a bottleneck.

## restic restore options that affect time
Taken from the restic restore page:
- `restic restore <snapshot-id> --target <dir>` restores a snapshot; `latest` selects the latest one, and `--host` and `--path` only select which snapshot, they do not restrict what is restored.
- `--include` or `--exclude` (mutually exclusive) restrict the restore to a subset of files; the `<snapshot>:<subfolder>` syntax restores one subfolder.
- Existing files in the target are checked by default (`--overwrite always` verifies content and restores only mismatching parts); `--overwrite if-changed` speeds the check by trusting matching size and mtime; `if-newer` and `never` are the other values.
- `--dry-run` with `--verbose=2` lists what would be restored without the full operation. A dry run also verifies existing content per the overwrite setting; specify `--overwrite never` or a non-existing `--target` to skip those checks.
- For many files or a whole snapshot, the restic page says `restic restore` is often significantly faster than `restic mount`.
- `--sparse` creates holes for long runs of zero bytes; the exact hole locations can differ from the original.

## Extrapolate honestly
Full-site RTO is the sum, over the restore sequence, of data divided by the aggregate rate, plus boot and validation time and time spent waiting on dependencies. One small test at one rate does not predict a much larger restore: test at realistic concurrency or measure each tier's ceiling.

## Verify
A throughput table per tier and system class, refreshed after infrastructure changes and compared against the BIA RTOs with gaps flagged.

## Checked

2026-11-09. Confirmed against the restic "Restoring from backup" page: `restore`, `latest`, `--host`/`--path`, `--include`/`--exclude`, subfolder syntax, `--overwrite` values, `--dry-run`, `--sparse`, and restore versus mount speed. Removed (not on the cited page): LTO-9 native speed, iperf3 and MTU advice, Veeam bottleneck percentages, Instant Recovery, SQL Server tuning options, restic pack-size advice, and the specific 200 GB and 50 TB figures. The measurement method is procedure advice.

Method: documentation only; no commands were run.
