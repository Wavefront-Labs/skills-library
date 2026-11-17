---
id: computing-software.cloud-infrastructure-engineering.azure.azcopy-storage-explorer-and-data-box
name: azcopy-storage-explorer-and-data-box
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azcopy, storage-explorer, data-transfer, data-box, data-box-disk, bulk-copy, azcopy-sync, azcopy-copy, azcopy-jobs, resume, concurrency, server-to-server-copy, s3-to-azure, gcs-to-azure, blob-copy, put-blob-from-url, object-replication, storage-mover, migration, throughput-tuning]
level: practitioner
status: docs-checked
description: "Move data into or between Azure Storage: AzCopy copy/sync with identity auth, resume and tuning, S3/GCS/blob copies, Storage Explorer, Storage Mover, Data Box offline."
sources: ["https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-optimize", "https://learn.microsoft.com/en-us/azure/storage/common/storage-ref-azcopy-copy", "https://learn.microsoft.com/en-us/azure/storage/common/storage-ref-azcopy-sync", "https://learn.microsoft.com/en-us/azure/storage/common/storage-ref-azcopy-login", "https://learn.microsoft.com/en-us/azure/databox/data-box-overview", "https://learn.microsoft.com/en-us/azure/databox/data-box-disk-overview", "https://learn.microsoft.com/en-us/azure/databox/data-box-limits", "https://learn.microsoft.com/en-us/azure/storage-mover/service-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data transfer — AzCopy for anything online, Data Box when the pipe is the bottleneck

**Goal:** a transfer that finishes, can be resumed, leaves a log you can audit, and
chose the tool by data size ÷ bandwidth rather than habit.

## 1. Pick the tool
| Volume / situation | Tool |
|---|---|
| Scripts, CI, anything repeatable | **AzCopy v10** |
| One-off browsing, ACL edits, small uploads | **Storage Explorer** |
| NAS/SMB/NFS shares to Files/Blob at scale | **Azure Storage Mover** |
| Between storage accounts, continuous | **Object replication** (blob, async, policy-based) or a server-to-server `azcopy copy` |
| Tens of TB or more with limited or no connectivity | **Data Box** (check the overview page for current SKUs and usable capacity: 80 TB, or next-gen 120 TB and 525 TB; Data Box Heavy is retired), **Data Box Disk** (8 TB disks, about 7 TB usable) |
Rule: Microsoft calls Data Box ideal above about 40 TB with little or no connectivity; work out data size ÷ real sustained bandwidth and order a device when the transfer would take weeks.

## 2. AzCopy essentials
```bash
azcopy login --tenant-id <t>              # Entra auth (needs Storage Blob Data Contributor); or
export AZCOPY_AUTO_LOGIN_TYPE=MSI          # managed identity on a VM; AZCOPY_SPA_CLIENT_SECRET for SP
azcopy copy "/data/exports" "https://st.blob.core.windows.net/raw/exports" --recursive \
  --block-size-mb 32 --put-md5 --log-level WARNING --overwrite ifSourceNewer
azcopy sync "/data/site" "https://st.blob.core.windows.net/web" --delete-destination true --recursive
azcopy jobs list; azcopy jobs resume <job-id>      # resumes from the plan file (~/.azcopy)
azcopy copy "https://src.blob.core.windows.net/c?<sas>" "https://dst.blob.core.windows.net/c" --recursive  # server-to-server, no egress through you
azcopy copy "https://s3.eu-west-1.amazonaws.com/bucket/prefix" "https://st.blob.core.windows.net/c" --recursive  # AWS_ACCESS_KEY_ID/SECRET env; GCS via GOOGLE_APPLICATION_CREDENTIALS
```
- Blob-to-blob copies are **server-to-server**: data flows between storage servers, not through the AzCopy host. S3 and GCS sources need `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY` or `GOOGLE_APPLICATION_CREDENTIALS` set.
- Preserve ACLs on ADLS Gen2 and Azure Files SMB with `--preserve-permissions`; `--preserve-info` replaces the older `--preserve-smb-info`.
- `--include-pattern "*.parquet"`, `--exclude-path`, `--include-after 2026-01-01T00:00:00Z`
  for incremental; `--dry-run` first.
- Tiers at upload: `--block-blob-tier Cool`; `--cache-control`, `--content-type` for web assets.

## 3. Throughput tuning
- `AZCOPY_CONCURRENCY_VALUE` (default 32 below five CPUs, otherwise 16 × CPUs, default capped at 300; the docs suggest a value above 1000 for blob-to-blob copies, `AUTO` to self-tune; run a benchmark first), `AZCOPY_BUFFER_GB` to cap buffer memory, `--cap-mbps` to cap the rate (uploads and downloads only, not account-to-account).
- Keep each job under 10 million files (over 50 million performs poorly); `--log-level ERROR` and `--check-length=false` cut overhead on many small files; run one AzCopy instance per client.
- Benchmark the path first: `azcopy bench "https://st.blob.core.windows.net/bench" --file-count 100 --size-per-file 100M`.
- Many small files: throughput is bound by request rate (default 20,000 requests per second per general-purpose v2 account) — split jobs, or parallelise across accounts.
- A VM in-region only helps if the data is already in Azure; from on-prem the uplink is the limit, so consider Data Box.

## 4. Storage Explorer and Mover
- Storage Explorer: sign in with Entra; prefer it over SAS or keys.
- Storage Mover: migrates SMB and NFS sources to Azure Blob containers and Azure file shares; see the service overview page for the supported source/target matrix (for example SMB 1.x sources and NFS Azure file shares are not supported for SMB mounts).

## 5. Data Box workflow
Order in portal (region, target storage accounts) → device ships (AES 256-bit encryption, tamper-evident stickers) → connect via the device's 1-GbE/10-GbE interfaces, copy with SMB/NFS or the Data Box *data copy service* to its share names (`<account>_BlockBlob`, `<account>_PageBlob`, `<account>_AzFile`) → prepare to ship → Microsoft uploads → check the copy log in the portal → disks wiped to NIST 800-88r1. Files in the `_BlockBlob`/`_PageBlob` shares upload as block/page blobs; folders directly under `_AzFile` become file shares. Export (cloud → you) is also available. Keep source data until the portal confirms the copy.

## Gotchas
- `azcopy sync` deletes at destination only with `--delete-destination true`; it compares last-modified time, not content — use `--compare-hash MD5` when clocks are untrustworthy.
- A block blob maxes out at 50,000 blocks × 4,000 MiB (about 190.7 TiB); adjust `--block-size-mb` for very large files.
- Data Box has naming limits (blob names 1 to 1,024 characters, at most 254 path segments); read the copy error log before shipping (see the Data Box limits page).

## Verify
- [ ] `azcopy jobs show <id>` reports the job completed with no failed transfers; the log in `~/.azcopy` is archived.
- [ ] Spot-check MD5 (`--put-md5` then `az storage blob show --query properties.contentSettings.contentMd5`) against source for a sample.
- [ ] Blob count and total bytes at destination equal source (`azcopy list --machine-readable --running-tally`).
- [ ] Data Box: portal copy log shows 0 errors before the source is decommissioned.

## Checked
2026-10-28. Confirmed against Learn and the AzCopy wiki: AzCopy concurrency default (32 below five CPUs, else 16 x CPUs, max default 300), AZCOPY_BUFFER_GB, `--cap-mbps` scope, job-size guidance, `--delete-destination`, `--compare-hash MD5`, `--preserve-permissions`/`--preserve-info`, `--include-after`, `--block-blob-tier`, `AZCOPY_AUTO_LOGIN_TYPE`, `azcopy login --tenant-id`, `azcopy list --machine-readable --running-tally`, S3/GCS credential variables, 20,000 requests per second account target, 190.7 TiB block blob maximum, Data Box 80 TB / 120 TB / 525 TB usable, Data Box Heavy retired, Data Box Disk 8 TB, AES 256-bit, NIST 800-88r1, share names, 1,024-character blob names. Removed or corrected: old 100 TB / 1 PB capacities, 1 Gbps = 10 TB/day rule, 7-day uncommitted block claim, `Put Block From URL` name, `--preserve-smb-permissions`, Storage Mover agent/VM and Storage Explorer setting details, turnaround time.
Method: documentation only; no commands were run.
