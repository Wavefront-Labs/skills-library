---
id: computing-software.digital-privacy-hygiene.device-hardening.nas-backups-with-snapshots
name: nas-backups-with-snapshots
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, nas-snapshots, nas, ransomware, backups]
level: practitioner
status: draft
description: "Protect a home NAS and its data with Btrfs/ZFS snapshots, immutable snapshots, off-site replication, and access settings that keep ransomware out."
sources:
  - "https://kb.synology.com/"
  - "https://www.truenas.com/docs/"
  - "https://www.qnap.com/en/how-to/faq"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# NAS backups with snapshots

**Goal:** a NAS that can roll back from ransomware or mistakes, and that isn't your only copy.

## Snapshots
- **Synology (Btrfs):** Snapshot Replication > Snapshots > set a schedule (hourly, keep e.g. 24 hourly, 14 daily,
  8 weekly). DSM 7.2+ supports **immutable snapshots** that can't be deleted, even by an admin, for a set number of days.
- **TrueNAS (ZFS):** Data Protection > Periodic Snapshot Tasks per dataset with retention.
- **QNAP:** Storage & Snapshots > snapshot schedule on thick/thin volumes.
Enable snapshot visibility (`#snapshot` / `.zfs/snapshot`) so users can self-restore.

## Off-site copy
A snapshot lives on the same disks: a fire, theft or failed array takes it too. Replicate with Hyper Backup /
Cloud Sync, ZFS replication or restic to a cloud bucket (Backblaze B2, Synology C2) or a second NAS elsewhere.

## Keep ransomware out
- Don't map NAS shares on PCs with admin credentials; give each user its own account with access only to its shares.
- Disable the default `admin` account, enable 2FA for DSM/TrueNAS logins.
- Never expose the NAS web UI or SMB to the internet (QNAP Deadbolt and similar campaigns hit exposed units). Turn
  off UPnP port mapping and remote cloud relay unless needed; use a VPN.
- Auto-install security updates.

## Verify
Restore a file from a snapshot and from the off-site backup each quarter.
