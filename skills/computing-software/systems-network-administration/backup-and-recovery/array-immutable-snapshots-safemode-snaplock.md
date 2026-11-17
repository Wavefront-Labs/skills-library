---
id: computing-software.systems-network-administration.backup-and-recovery.array-immutable-snapshots-safemode-snaplock
name: array-immutable-snapshots-safemode-snaplock
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [safemode, snaplock, immutable-snapshots, storage-array, ransomware-protection, tamperproof-snapshots]
level: advanced
status: draft
description: "Use storage array immutable snapshots for ransomware resilience: Pure SafeMode, NetApp SnapLock and tamperproof snapshots, PowerStore secure snapshots, and their limits."
sources:
  - https://support.purestorage.com/Solutions/SafeMode
  - https://docs.netapp.com/us-en/ontap/snaplock/index.html
  - https://docs.netapp.com/us-en/ontap/snaplock/snapshot-lock-concept.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Array immutable snapshots (SafeMode, SnapLock)

Array snapshots restore terabytes in minutes. Made immutable, they survive an attacker who has admin credentials to the array or backup software.

## Pure Storage SafeMode
- Snapshots and protection-group snapshots cannot be eradicated (deleted permanently) before retention, even by array admins.
- Enabled and changed only via Pure Support with designated contacts and a PIN; this is the point: a compromised admin cannot turn it off.
- Configure "auto-on" SafeMode for all new protection groups; retention typically 7-14 days of eradication delay plus snapshot schedule.

## NetApp ONTAP
- **SnapLock** volumes (Compliance or Enterprise mode): WORM files with retention; Compliance mode cannot be deleted even by admins until expiry (and not the aggregate either).
- **Tamperproof snapshot locking** (ONTAP 9.12.1+): lock regular snapshots with a retention period on SnapLock-licensed systems; `volume snapshot policy` with retention, and Multi-Admin Verification (MAV) for destructive commands.
- **SnapVault to a SnapLock destination** for immutable backups on a secondary system.

## Others
Dell PowerStore/PowerMax secure snapshots, HPE Alletra immutable snapshots, Infinidat InfiniSafe; check vendor names and licensing.

## Design
- Snapshots are on the same array: protect against logical attack, not array loss. Keep an off-array copy.
- Size capacity for retention × change rate; a ransomware event's churn consumes space fast and cannot be freed early.
- Protect array management: separate admin accounts, MFA, MAV or multi-party approval, management network isolation.

## Verify
Attempt to delete a locked snapshot with an admin account in a test: the array refuses. Restore a volume clone from a locked snapshot and mount it.
