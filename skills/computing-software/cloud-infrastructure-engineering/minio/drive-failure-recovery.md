---
id: computing-software.cloud-infrastructure-engineering.minio.drive-failure-recovery
name: drive-failure-recovery
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, drive-failure-recovery, hot-swap, drive-replacement, mkfs-xfs, fstab, label-mounting, mc-admin-heal]
level: practitioner
status: docs-checked
description: "Replace a failed MinIO drive by hot-swap: unmount, install an empty XFS drive with the same label, fix fstab, remount and watch healing, with capacity-ceiling and nofail caveats."
sources: ["https://github.com/minio/docs/blob/main/source/operations/data-recovery/recover-after-drive-failure.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO drive failure recovery

MinIO supports hot-swapping failed drives. It detects and heals the new drive with no node or deployment restart, and healing touches only the replaced drive and usually has minimal performance impact. All access to the drives must go through MinIO. The steps assume each node mounts drives from `/etc/fstab` using per-drive labels.

1. **Unmount** the failed drive, e.g. `umount /dev/sdb`.
2. **Replace** it with a drive that is XFS formatted and empty, the same type (HDD, SSD, NVMe), and of equal or greater performance and capacity. A larger drive adds nothing: MinIO uses the **smallest** drive's capacity as the ceiling for all drives in the server pool. Format and label to match the failed one: `mkfs.xfs /dev/sdb -L DRIVE1`. Label-based mounting is strongly recommended so drive order survives restarts.
3. **Review fstab.** With labels (`LABEL=DRIVE1 /mnt/drive1 xfs defaults,noatime 0 2`) no change is needed when the new drive reuses the label. With UUID mounts update each UUID (see `lsblk`).
4. **Remount** with `mount -a`.
5. **Monitor**: `mc admin logs` or `journalctl -u minio` should name each formatted, empty drive. Track overall healing with `mc admin heal`; MinIO heals replaced drives aggressively for rapid recovery.
6. **Afterwards** watch for further failures, since drive batches can fail close together. Schedule dedicated maintenance to replace a known bad batch.

## nofail caution
Cloud instances with external mounts may fail to boot if a mount errors. `nofail` silences that, but the docs say not to use it on locally attached disks, as it stops MinIO and the OS responding normally to drive errors.

Concepts: `computing-software.cloud-infrastructure-engineering.minio.healing`, `computing-software.cloud-infrastructure-engineering.minio.hardware-checklist`.

## Checked
2026-11-03. Confirmed against the MinIO docs source: Drive Failure Recovery page (recover-after-drive-failure.rst). Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
