---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-compression-dedup-storage-optimization
name: veeam-compression-dedup-storage-optimization
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam, veeam-storage-optimization, compression, inline-deduplication, block-size, dedupe-appliance]
level: advanced
status: docs-checked
description: "Choose Veeam job compression level, storage optimization block size and inline dedupe settings for disk, dedupe appliances and object storage, and predict the effect."
sources:
  - https://helpcenter.veeam.com/docs/vbr/userguide/compression_deduplication.html
  - https://helpcenter.veeam.com/docs/vbr/userguide/backup_job_advanced_storage_vm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compression, deduplication and storage optimization

Backup job wizard > Storage step > Advanced job settings > Storage tab.

## Storage optimization (block size)
| Setting | Recommended for |
|---|---|
| 4 MB (former Local target, large blocks) | Backup files larger than 16 TB; HPE StoreOnce and Dell Data Domain. Lowest dedupe ratio, largest incrementals |
| 1 MB (former Local target) | SAN, DAS or local storage. Fastest jobs, lower dedupe ratio |
| 512 KB (former LAN target) | NAS and on-site backup/replication. Better dedupe ratio, smaller files |
| 256 KB (former WAN target) | Off-site backup over WAN. Maximum dedupe ratio, smallest files (not always achieved) |

- More blocks means more processing time; a small block size on a large backup file creates a very large dedupe metadata table that can overgrow repository memory and CPU. Use large blocks for large files.
- For backup jobs, new block size applies only after an **active full** backup. For backup copy jobs: change it in the initial backup job, then run an active full on the initial job and on the copy job.

## Compression level
| Level | Algorithm | Notes |
|---|---|---|
| None | none | For storage with hardware compression and deduplication; can reduce performance by increasing transferred data |
| Dedupe-friendly | Rle | Some dedupe appliances and external WAN accelerators |
| Optimal | Lz4 | Recommended; best ratio vs performance, lowest proxy CPU, fastest restore |
| High | Zstd 3 | Up to 60% more reduction than Optimal, 2x CPU and 2x slower restore |
| Extreme | Zstd 9 | Up to 33% more than High, 5x CPU |

- Backup copy jobs: Auto reuses the compression of the copied files.
- Changing compression applies to newly created files without a new full; for one level throughout, run an active full.
- Data reduction is not guaranteed; it depends on source data and the target file system.
- With encryption on and the repository's "Decompress backup data blocks before storing" selected, Veeam does not compress VM data, so transferred data and backup size can be larger.

## Inline deduplication
On by default; dedupes within a single job. Clearing it makes incrementals faster (all CBT-marked blocks are saved without checking) but files can grow. The option is not shown for object storage repositories.

## Block exclusions
By default Veeam excludes swap file blocks (hiberfil.sys and pagefile.sys, via the NTFS MFT) and deleted file blocks (BitLooker). Both can be turned off in the same tab.

## Verify
Compare job statistics (dedupe and compression ratios and the bottleneck line) before and after a change.

## Checked
2026-11-09. Read in full: Veeam Help Center "Data Compression and Deduplication" and "Storage Settings" (build 13.1.2.57). Corrected: 4 MB block size is for files above 16 TB and Data Domain/StoreOnce (not object storage); High saves up to 60% more than Optimal (was about 10%). Removed as unstated: dedupe-appliance recipe (Align blocks, DD Boost, Catalyst), advice to disable inline dedupe on appliances, "revert if Proxy is the bottleneck" statistics wording, and the bp.veeam.com source.
Method: documentation only; no commands were run.
