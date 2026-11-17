---
id: computing-software.cloud-infrastructure-engineering.azure.azcopy-bench-and-sync-delete-destination-safety
name: azcopy-bench-and-sync-delete-destination-safety
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azcopy, azcopy-bench, delete-destination, azcopy-sync, throughput-testing]
level: practitioner
status: docs-checked
description: "Measure achievable throughput with azcopy bench, and run azcopy sync safely: comparison modes, delete-destination prompt/true, dry runs and soft delete as a net."
sources: ["https://learn.microsoft.com/azure/storage/common/storage-ref-azcopy-bench", "https://learn.microsoft.com/azure/storage/common/storage-ref-azcopy-sync", "https://learn.microsoft.com/azure/storage/common/storage-use-azcopy-optimize"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# azcopy bench and safe sync

**Goal:** know what bandwidth you'll get before a migration, and never wipe a destination with a reversed sync.

## Benchmark
```bash
azcopy bench "https://st.blob.core.windows.net/benchtest" --file-count 100 --size-per-file 1G     # upload, generated data
azcopy bench "https://st.blob.core.windows.net/benchtest" --mode download --file-count 50 --size-per-file 2G
```
- Uses generated data and deletes it afterwards (`--delete-test-data=true` default).
- The run reports performance statistics and a recommended concurrency value; tune
  `AZCOPY_CONCURRENCY_VALUE` (or set it to `AUTO`) and re-run.
- Run from the actual source machine/network path, at the same time of day as the real job.

## Sync semantics
```bash
azcopy sync "/data/site" "https://st.blob.core.windows.net/\$web" --recursive --delete-destination=prompt --dry-run
```
- Compares by **last-modified time** by default; `--compare-hash=MD5` relies on hashes instead (missing hashes at a remote source raise an error).
- `--mirror-mode` disables the last-modified comparison and overwrites conflicting files and blobs at the destination.
- `--delete-destination`: `false` (default) never deletes; `prompt` asks before scheduling deletions; `true` deletes extra files at the
  destination **without asking**.

## Safety checklist for delete-destination=true
1. Run with `--dry-run` and read the delete list.
2. Double-check argument order: `azcopy sync <source> <destination>`.
3. Enable blob soft delete/versioning on the destination before scheduled syncs.
4. In pipelines, pin source paths with variables validated non-empty (an empty source path can mean "sync nothing -> delete everything").

## Gotchas
- Sync identifies all files at the destination and compares names and last-modified times before it starts - slow for very large file counts. The AzCopy optimization page suggests `azcopy copy --overwrite=ifSourceNewer` instead (it never deletes at the destination), or `--include-after` for incremental jobs.

## Verify
- [ ] Bench numbers recorded in the migration plan; dry-run of the scheduled sync shows no unexpected deletes.

## Checked
2026-10-28. Confirmed on the azcopy bench, azcopy sync and Optimize AzCopy pages: `--mode`, `--file-count`, `--size-per-file`, `--delete-test-data` default true, `--compare-hash` (None, MD5), `--mirror-mode`, `--delete-destination` (true, false, prompt), `--dry-run`, concurrency recommendation, copy with `ifSourceNewer` as the no-scan alternative. Removed: the bottleneck-diagnosis claim, the stored-MD5 requirement, the unverified `--mirror-mode` version note, the file-share/blob sync-matrix remark and the clock-skew remark.
Method: documentation only; no commands were run.
