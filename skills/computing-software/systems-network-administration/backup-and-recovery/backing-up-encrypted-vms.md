---
id: computing-software.systems-network-administration.backup-and-recovery.backing-up-encrypted-vms
name: backing-up-encrypted-vms
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [encrypted-vm-backup, vm-image-backup, vm-encryption, vtpm, key-provider, shielded-vm-backup]
level: advanced
status: draft
description: "Back up and restore encrypted VMs: vSphere VM Encryption and vTPM with VADP, key provider availability, Hyper-V shielded VMs, and in-guest BitLocker or LUKS volumes."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-security-8-0/virtual-machine-encryption.html
  - https://learn.microsoft.com/en-us/windows-server/security/guarded-fabric-shielded-vm/guarded-fabric-and-shielded-vms
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backing up encrypted VMs

**Goal:** encrypted VMs are backed up and, more importantly, can be restored where and when needed, with keys available.

## vSphere VM Encryption / vTPM
- Backup via VADP reads **decrypted** data from the host (the host has the key). The backup itself is plaintext unless the backup tool encrypts it, so turn on backup encryption.
- Transport modes: NBD/NBDSSL work. HotAdd requires the backup proxy VM to be encrypted too, and the backup service account needs the Cryptographic Operations privileges listed in the backup vendor's permissions guide (for restore of encrypted VMs as well as backup).
- **Restore**: restoring as an encrypted VM needs the key provider (standard KMS or vSphere Native Key Provider) available in the target vCenter. For DR, the DR vCenter must have the same key provider (same KMS cluster or an imported NKP backup).
- **Back up the Native Key Provider** (`.p12` export) and KMS keys; without them encrypted VMs and vTPM-protected guests (BitLocker keys sealed to vTPM) do not boot.

## Hyper-V shielded VMs
- Host-level backup captures the VM files; the guest disks are BitLocker-encrypted with keys released by HGS.
- Restore only runs on a guarded host trusted by the same HGS. Back up HGS (configuration, keys, certificates) separately; it is a tier-0 dependency.

## In-guest encryption (BitLocker, LUKS)
- Image backups contain encrypted volumes; dedup and compression are poor.
- File-level restore and application item restore need the volume unlocked (BitLocker recovery key, LUKS passphrase) on the mount host; many tools cannot do it at all.
- Escrow recovery keys (AD/Entra for BitLocker, a vault for LUKS) and back up the escrow.

## Gotchas
- Restoring an encrypted VM as unencrypted (allowed with privileges) bypasses policy; control who can do that.
- Key rotation without a fresh backup: old backups need old keys, so keep key history for the retention period.

## Verify
Annual test: restore an encrypted VM into the DR site with only the documented key material, boot it, and unlock a vTPM-protected guest.
