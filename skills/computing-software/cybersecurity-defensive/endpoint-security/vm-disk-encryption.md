---
id: computing-software.cybersecurity-defensive.endpoint-security.vm-disk-encryption
name: vm-disk-encryption
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [vm-disk-encryption, server-disk-encryption, azure-disk-encryption, encryption-at-host, ebs-encryption, bitlocker-server, disk-encryption]
level: practitioner
status: draft
description: "Encrypt server and VM disks: cloud platform options (EBS default encryption, Azure encryption at host, CMEK), BitLocker/LUKS on VMs with network unlock or Clevis/Tang."
sources: ["https://docs.aws.amazon.com/ebs/latest/userguide/encryption-by-default.html", "https://learn.microsoft.com/en-us/azure/virtual-machines/disk-encryption-overview", "https://github.com/latchset/clevis", "https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/network-unlock"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Server and VM disk encryption

## Cloud VMs
| Cloud | Option | Notes |
|---|---|---|
| AWS | EBS encryption by default per region (`aws ec2 enable-ebs-encryption-by-default`), CMK in KMS | Snapshots and AMIs inherit; unencrypted shares impossible with CMK not shared |
| Azure | Server-side encryption (always on, platform keys) + **encryption at host** (temp disk and cache encrypted) + customer-managed keys via Disk Encryption Set | Azure Disk Encryption (BitLocker/dm-crypt in guest) is scheduled for retirement (Sept 2028); prefer encryption at host |
| GCP | Default encryption, CMEK or CSEK for persistent disks | CMEK key disable = disks unusable (intentional kill switch) |
Enforce with policy (AWS Config `ec2-ebs-encryption-by-default`, Azure Policy for encryption at host/CMK, GCP org policy `constraints/gcp.restrictNonCmekServices`).

## On-prem / guest encryption
- **Windows Server BitLocker:** TPM protector; **Network Unlock** for unattended reboots on trusted networks (WDS + certificate), or TPM-only for servers in secure data centres; recovery keys to AD.
- **Linux LUKS:** unattended unlock with **Clevis + Tang** (network-bound: unlocks only when Tang server reachable) or TPM2 pin:
  `clevis luks bind -d /dev/sda3 tang '{"url":"http://tang.internal"}'` then `dracut -f` to include in initramfs.
- Hypervisor-level: vSphere VM Encryption with a key provider (native KMS or external KMIP) and vTPM.

## Threat model
Platform encryption protects against physical media theft and some provider-side exposure; it does not
protect against someone with access to the running VM or the cloud console. Pair with key access control.

## Gotchas
- Tang servers become boot dependencies; run at least two, `sss` policy for threshold.
- Key deletion/disable in KMS bricks all dependent disks and backups - protect key lifecycles.

## Verify
- [ ] Inventory query: zero unencrypted volumes (AWS Config, Azure Resource Graph, GCP asset inventory).
- [ ] Reboot test of an unattended-unlock server succeeds; detached disk elsewhere cannot unlock.
