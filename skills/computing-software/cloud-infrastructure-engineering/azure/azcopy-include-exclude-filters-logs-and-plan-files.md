---
id: computing-software.cloud-infrastructure-engineering.azure.azcopy-include-exclude-filters-logs-and-plan-files
name: azcopy-include-exclude-filters-logs-and-plan-files
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azcopy, azcopy-filters, azcopy-logs, include-pattern, dry-run, plan-files]
level: practitioner
status: docs-checked
description: "Copy exactly the right files with AzCopy: include/exclude patterns, paths, regex and date filters, dry runs, and controlling log and job plan file locations."
sources: ["https://learn.microsoft.com/azure/storage/common/storage-ref-azcopy-copy", "https://learn.microsoft.com/azure/storage/common/storage-use-azcopy-configure", "https://learn.microsoft.com/azure/storage/common/storage-use-azcopy-blobs-upload"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AzCopy filters, logs and plan files

**Goal:** precise transfers you can preview, and logs that don't fill the system disk.

## Filters
```bash
azcopy copy "/data/exports" "https://st.blob.core.windows.net/exports" --recursive \
  --include-pattern "*.csv;*.json" --exclude-pattern "*tmp*"
azcopy copy "https://src.blob.core.windows.net/c" "https://dst.blob.core.windows.net/c" --recursive \
  --include-path "2026/09;2026/10" --exclude-path "2026/10/scratch"
azcopy copy "/data" "https://st.blob.core.windows.net/c" --recursive --include-after "2026-10-01T00:00:00Z"
azcopy copy "/data" "https://st.blob.core.windows.net/c" --recursive --include-regex "^logs/app[0-9]+/.*\.gz$"
```
- `--include-pattern` matches **file names** only (wildcards, `;`-separated); `--include-path` matches relative paths
  (no wildcards); `--include-regex` matches the relative path.
- `--include-after` / `--include-before` filter by last-modified time (ISO 8601, UTC).
- `--exclude-blob-type` (BlockBlob, PageBlob or AppendBlob; not applicable when copying from a non-Azure source) and `--exclude-container` (account-to-account transfers only).

## Preview first
```bash
azcopy copy "/data" "https://st.blob.core.windows.net/c" --recursive --include-pattern "*.csv" --dry-run
```
Prints what would transfer (or delete, for sync) without doing it.

## Logs and plan files
- Defaults: `~/.azcopy` (Linux/macOS) or `%USERPROFILE%\.azcopy` (Windows). Large jobs create big plan files.
```bash
export AZCOPY_LOG_LOCATION=/mnt/scratch/azcopy/logs
export AZCOPY_JOB_PLAN_LOCATION=/mnt/scratch/azcopy/plans
azcopy copy ... --log-level ERROR          # INFO default is verbose; WARNING/ERROR for big jobs
azcopy jobs show <jobId> --with-status=Failed
azcopy jobs clean                          # delete old plan/log files
```
- `--output-type json` gives machine-readable progress for pipelines.

## Gotchas
- `--with-status` values are case-sensitive (`Failed`, not `failed`).

## Verify
- [ ] Dry-run output matches expectations; job summary shows 0 failed; log directory on a disk with space.

## Checked
2026-10-28. Confirmed on the azcopy copy reference, Configure AzCopy and Upload-blobs pages: `--include-path` (no wildcards, relative path prefix), `--include-regex`, `--include-after`/`--include-before` (ISO 8601), `--exclude-blob-type`, `--exclude-container`, default log/plan location `.azcopy` under the user profile or home, `AZCOPY_LOG_LOCATION`, `AZCOPY_JOB_PLAN_LOCATION`, `azcopy jobs clean`, `azcopy jobs show --with-status=Failed` (case-sensitive value), `--output-type json`, `--log-level` default INFO. Removed: Linux case-sensitivity claim, the `/data/*` versus `--recursive` remark and the remove-filter remark.
Method: documentation only; no commands were run.
