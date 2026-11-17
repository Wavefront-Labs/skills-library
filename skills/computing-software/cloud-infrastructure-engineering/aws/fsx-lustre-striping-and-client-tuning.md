---
id: computing-software.cloud-infrastructure-engineering.aws.fsx-lustre-striping-and-client-tuning
name: fsx-lustre-striping-and-client-tuning
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, fsx, lustre-striping, fsx-lustre, hpc-storage, lfs]
level: advanced
status: gated
description: "Tune FSx for Lustre for throughput: file striping with lfs setstripe and progressive layouts, OST balance, client mount options and lctl parameters."
sources: ["https://docs.aws.amazon.com/fsx/latest/LustreGuide/performance.html#striping-data", "https://docs.aws.amazon.com/fsx/latest/LustreGuide/performance-tips.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lustre striping and client tuning

## 1. Striping
A file lives on one or more OSTs (storage targets). Large files read by many clients should be striped.
```bash
lfs getstripe /fsx/datasets/big.tar
lfs setstripe --stripe-count 8 /fsx/datasets/          # new files in the dir: 8 OSTs
lfs migrate --stripe-count 8 /fsx/datasets/old-big.bin  # restripe an existing file
```
- Progressive File Layouts (PFL) grow the stripe count as a file grows; file systems created after December 18, 2020 default to a PFL
  (files under 1 GiB in one stripe, larger files get more stripes). Override per directory for known large-file workloads.
- Small files: keep stripe count 1; striping adds overhead.

## 2. Balance
```bash
lfs df -h /fsx        # per-OST usage (gated: unconfirmed, source is paywalled or blocked)
```
Imbalance comes from huge unstriped files; restripe them.

## 3. Client side
- Mount options: `-o relatime,flock` (only use `flock` if apps need locks). (gated: unconfirmed, source is paywalled or blocked)
- Large instances: follow the client parallelism tuning in the FSx performance tips for the instance type in use.
- Keep the Lustre client version matching the kernel and supported by the FSx file system version.

## 4. Metadata
Millions of files in one directory and `ls -l` loops hammer the MDS; spread files across directories,
use `lfs find` instead of `find` (gated: unconfirmed, source is paywalled or blocked), and add metadata IOPS where the deployment type supports it.

## Verify
- [ ] `lfs getstripe` shows the intended layout; parallel read throughput approaches the file system's provisioned throughput.

## Checked

2026-10-28

Confirmed: lfs setstripe with --stripe-count, lfs migrate for existing files, progressive file layout default for file systems created after 2020-12-18 (files under 1 GiB in one stripe), provisioned Metadata IOPS on Persistent 2 file systems (FSx for Lustre User Guide).

Removed: 4 MiB stripe size, the -1 all-OSTs example, lctl parallelism values, EFA/GPUDirect sentence, the full-OST write-failure claim.

Gated: mount options relatime,flock and the lfs find advice: not found on the fetched performance pages.

Method: documentation only; no commands were run.
