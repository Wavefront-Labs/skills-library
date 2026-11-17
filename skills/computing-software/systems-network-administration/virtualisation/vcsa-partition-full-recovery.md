---
id: computing-software.systems-network-administration.virtualisation.vcsa-partition-full-recovery
name: vcsa-partition-full-recovery
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vcsa-disk-full, vsphere-troubleshooting, vcsa, storage-log, storage-seat, vpostgres, vmware, vsphere]
level: advanced
status: draft
description: "Recover a vCenter Server Appliance whose /storage/log, /storage/seat, /storage/archive or root partition filled: find the culprit, free space safely, and grow the VMDK."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VCSA partition full

Symptoms: vSphere Client "no healthy upstream", vpxd won't start, VAMI health shows
Storage red, logins fail.

## Find what's full
```sh
df -h | egrep "Use%|/storage|/$"
du -xsh /storage/log/* 2>/dev/null | sort -h | tail
du -xsh /var/log/* | sort -h | tail
```
Each partition is its own VMDK (8.0: disk 1 root, 5 log, 6 db, 7 dblog, 8 seat, ...;
`lsblk` maps them).

## By partition
| Partition | Usual cause | Safe action |
|---|---|---|
| `/storage/log` | debug logging, runaway service log, old support bundles | delete old `vc-support*.tgz`, rotated `*.gz` older than needed; reset log level |
| `/storage/seat` | events/tasks/stats (SEAT) retention too long, alarm storms | lower retention (vCenter → Configure → General → Database retention), then truncate via SR-guided procedure |
| `/storage/archive` | Postgres WAL archive kept for backups | normal to be high; fix if file-based backup schedule broken |
| `/storage/updatemgr` | old ISOs/bundles | delete unused images and baselines in vLCM |
| `/` root | core files, `/var/core`, audit logs, stale `/tmp` | remove core dumps after collecting |

Never delete active `*.log` files of running services (space not freed until restart;
use `> file.log` to truncate instead) and never delete Postgres data files.

## Grow the disk (permanent fix)
1. Snapshot VCSA (or confirm a fresh file-based backup).
2. Increase the matching VMDK in the VCSA VM settings.
3. On VCSA:
   ```sh
   /usr/lib/applmgmt/support/scripts/autogrow.sh
   ```
   (or VAMI API `POST /api/appliance/system/storage?action=resize`). 
4. `df -h` confirms; restart services: `service-control --start --all`.

## Gotchas
- Shrinking is impossible; grow in sensible increments.
- SEAT growth often signals an event storm (e.g. a host flapping); fix the source.
- Alarms "Log disk exhaustion" exist from 7.0; make sure they notify someone.

## Verify
All partitions < 80 %; `service-control --status --all` shows required services running;
VAMI Health Storage green.
