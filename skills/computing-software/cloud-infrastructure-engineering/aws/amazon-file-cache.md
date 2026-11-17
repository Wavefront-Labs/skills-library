---
id: computing-software.cloud-infrastructure-engineering.aws.amazon-file-cache
name: amazon-file-cache
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, file-cache, amazon-file-cache, lustre, data-repository-association, hybrid-storage]
level: advanced
status: docs-checked
description: "Put Amazon File Cache, a Lustre-based high-speed cache, in front of on-prem NFS or S3 data: create the cache, link data repositories, lazy load and write back."
sources: ["https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/what-is.html", "https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/create-linked-data-repo.html", "https://docs.aws.amazon.com/cli/latest/reference/fsx/create-file-cache.html", "https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/preload-file-contents-hsm.html", "https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/exporting-files-hsm.html", "https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/cache-eviction.html", "https://docs.aws.amazon.com/fsx/latest/FileCacheGuide/mounting-ec2-instance.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Amazon File Cache

**Use:** burst compute in AWS (rendering, genomics, EDA) needs fast access to data that lives on
on-prem NFS or in S3, without copying it all first. Check current service availability for new
customers before designing around it; FSx for Lustre with S3 data repositories is the usual alternative.

## 1. Create
```bash
aws fsx create-file-cache --file-cache-type LUSTRE --file-cache-type-version 2.12 \
  --storage-capacity 1200 --subnet-ids subnet-a --security-group-ids sg-cache \
  --lustre-configuration 'DeploymentType=CACHE_1,PerUnitStorageThroughput=1000,MetadataConfiguration={StorageCapacity=2400}' \
  --data-repository-associations '[
    {"FileCachePath":"/onprem","DataRepositoryPath":"nfs://nfs.example.com/export/assets/","NFS":{"Version":"NFS3"}}]'
```
- Up to 8 data repository associations, each with a unique cache directory; all must be the same type, all NFS or all S3 (an S3 association uses an `s3://bucket/prefix` path and no `NFS` block).
- The NFS data repository must support NFSv3 and can be on premises or in the cloud; see the on-premises prerequisites page for network needs.

## 2. Use
Clients mount with the Lustre client (`mount -t lustre <dns>@tcp:/<mountname> /cache`).
- First read of a file lazy-loads it from the repository; later reads are served from cache.
- Preload hot sets: `sudo lfs hsm_restore <file>` (check with `lfs hsm_action`).
- Write back: `sudo lfs hsm_archive <file>` exports changes to the data repository.
- Automatic eviction releases less recently used files when the cache fills; only exported (archived) files can be released, manually with `lfs hsm_release`.

## Verify
- [ ] Second read of a large file is many times faster than the first.
- [ ] Exported outputs appear on the on-prem NFS share.

## Checked

Checked 2026-10-28 against the Amazon File Cache User Guide (what is, linking data repositories, preload, export, eviction, mounting) and the `aws fsx create-file-cache` CLI reference.
- Confirmed: Lustre 2.12, `CACHE_1`, `PerUnitStorageThroughput` 1000, metadata `StorageCapacity` 2400, storage 1200 GiB, up to 8 DRAs, NFSv3 only, lazy load, HSM commands, automatic eviction, Lustre client mount.
- Corrected: S3 and NFS associations cannot be mixed on one cache; the example now uses NFS only.
- Removed: data repository task export claim and the NFS export/IP and DX/VPN specifics, replaced by a pointer to the prerequisites page.

Method: documentation only; no commands were run.
