---
id: computing-software.cloud-infrastructure-engineering.aws.ebs-attach-detach-and-nvme-device-naming
name: ebs-attach-detach-and-nvme-device-naming
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ebs, nvme-device-naming, attach-volume, detach-volume, fstab]
level: practitioner
status: docs-checked
description: "Attach and detach EBS volumes safely, map NVMe device names on Nitro instances back to volume IDs, and write fstab entries that survive reordering."
sources: ["https://docs.aws.amazon.com/ebs/latest/userguide/ebs-attaching-volume.html", "https://docs.aws.amazon.com/ebs/latest/userguide/identify-nvme-ebs-device.html", "https://docs.aws.amazon.com/ebs/latest/userguide/ebs-using-volumes.html", "https://docs.aws.amazon.com/ebs/latest/userguide/ebs-detaching-volume.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Attaching volumes and NVMe device naming

## 1. Attach
```bash
aws ec2 attach-volume --volume-id vol-0abc --instance-id i-0abc --device /dev/sdf
aws ec2 wait volume-in-use --volume-ids vol-0abc
```
Same AZ only. On Nitro instances the volume appears as `/dev/nvme1n1` (or another number), not `/dev/sdf`.

## 2. Map NVMe devices to volumes
```bash
lsblk -o NAME,SIZE,SERIAL,MOUNTPOINT          # SERIAL = vol0abc... (volume ID without the hyphen)
sudo nvme id-ctrl -V /dev/nvme1n1        # other distributions; sn = volume ID, vendor data = device name
sudo ebsnvme-id /dev/nvme1n1             # Amazon Linux or FreeBSD AMIs
```
NVMe names follow the order in which devices respond at boot, not the block device mapping, so they can change between boots. The volume ID (the NVMe serial number) and the mount point are stable. Volumes attached after launch show a `/dev/` prefix in the vendor data; volumes attached at launch do not.

## 3. Format and mount by UUID
```bash
sudo mkfs -t xfs /dev/nvme1n1
UUID=$(sudo blkid -s UUID -o value /dev/nvme1n1)
echo "UUID=$UUID /data xfs defaults,nofail 0 2" | sudo tee -a /etc/fstab
sudo mount -a
```
`nofail` lets the instance boot even if there are errors mounting the volume (for example after the volume is moved to another instance).

## 4. Detach
```bash
sudo umount /data
aws ec2 detach-volume --volume-id vol-0abc
```
Snapshot the volume before unmounting if the data matters. A forced detach (`--force`) is a last resort for a volume stuck in `detaching`: it can damage the file system or data.

## 5. Windows
Disks show in Disk Management. On Windows, `ebsnvme-id.exe` (included in the AWS Windows Server AMIs and installed by the AWS NVMe driver package 1.5.0 or later) lists each disk number with its volume ID and device name.

## Verify
- [ ] After reboot the volume mounts at `/data` regardless of NVMe number.

## Checked

Checked 2026-10-27 against the Amazon EBS User Guide (docs.aws.amazon.com/ebs/latest/userguide) and the botocore EC2 model and waiters.
- Same-AZ attach rule, `nofail` fstab behaviour and the forced-detach warning confirmed on the attach, using-volumes and detach pages.
- NVMe naming, `lsblk -o +SERIAL`, `nvme id-ctrl -V` and `ebsnvme-id` usage confirmed on the "Map volumes to device names" page (identify-nvme-ebs-device).
- `attach-volume` (--device required), `detach-volume --force` and the `volume-in-use` waiter confirmed in the service model.
- Removed the by-id symlink listing and the Windows `Get-Disk` serial claim, which no documentation page confirmed.

Method: documentation only; no commands were run.
