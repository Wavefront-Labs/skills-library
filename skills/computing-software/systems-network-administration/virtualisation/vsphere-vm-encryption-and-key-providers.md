---
id: computing-software.systems-network-administration.virtualisation.vsphere-vm-encryption-and-key-providers
name: vsphere-vm-encryption-and-key-providers
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vm-encryption, native-key-provider, kms, standard-key-provider, kmip, trust-authority, encryption-policy, vsphere-security, vmware, vsphere]
level: advanced
status: draft
description: "Encrypt VMs in vSphere: Native Key Provider vs external KMIP KMS, VM Encryption storage policy, backing up NKP keys, encrypted VM behaviour, and recovery when keys are missing."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vSphere VM encryption and key providers

**Goal:** VM disks and files encrypted at rest at the hypervisor layer, with keys you can
recover after a vCenter or site loss.

## Key providers
| Provider | Notes |
|---|---|
| **Native Key Provider (NKP)** (7.0U2+) | Built into vCenter, no external KMS; enables vTPM and VM encryption. **Back up the NKP** (password-protected `.p12`) or keys are lost with vCenter. Hosts need TPM 2.0 if "require TPM" set |
| Standard key provider | External KMIP KMS cluster (Thales, Entrust, HyTrust, Fortanix…); vCenter holds trust certs, hosts get keys via vCenter |
| Trusted key provider (vSphere Trust Authority) | Attestation-based, hosts get keys only if attested |

## Encrypt a VM
1. Configure a key provider and set it as default (Configure → Security → Key Providers).
2. Apply the **VM Encryption Policy** (storage policy) to VM home and disks (VM powered off
   for existing VMs in most versions). New disks inherit.
3. Users need the cryptographic privileges; the "No cryptography administrator" role lets
   admins manage VMs without decrypting/exporting them.

## Behaviour
- Encrypted VMs always use encrypted vMotion; core dumps on hosts become encrypted.
- Backups via VADP read decrypted data (backup proxy must have crypto privileges);
  backups are then encrypted by the backup software, not by VM encryption.
- Cannot encrypt VMs with snapshots in some cases; consolidate first.
- Performance overhead is small on AES-NI CPUs but storage dedupe on the array drops to
  nothing for encrypted data.

## Recovery scenarios
- **Restored/rebuilt vCenter:** restore the NKP from its backup with the same name, or
  re-add the same KMS cluster with the **same key provider name**; VMs show "locked" until
  keys are available, then **Unlock VM**.
- Host reboots while KMS unreachable: encrypted VMs cannot power on (hosts cache keys
  only while running for standard providers). Keep KMS highly available and outside the
  cluster it serves.

## Verify
NKP backup exists in the vault and was test-restored in a lab; `Get-VM | Where
{$_.ExtensionData.Config.KeyId}` lists the intended encrypted VMs; a test VM powers on
after a host reboot.
