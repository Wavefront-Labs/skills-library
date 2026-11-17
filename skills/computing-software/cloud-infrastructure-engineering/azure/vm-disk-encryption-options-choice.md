---
id: computing-software.cloud-infrastructure-engineering.azure.vm-disk-encryption-options-choice
name: vm-disk-encryption-options-choice
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, managed-disks, encryption-at-host, ade, disk-encryption-choice, disk-encryption-set, customer-managed-keys]
level: practitioner
status: docs-checked
description: "Choose between server-side encryption with platform or customer keys, encryption at host, Azure Disk Encryption and confidential disk encryption for Azure VMs."
sources: ["https://learn.microsoft.com/en-us/azure/virtual-machines/disk-encryption-overview", "https://learn.microsoft.com/en-us/azure/virtual-machines/disk-encryption", "https://learn.microsoft.com/en-us/azure/virtual-machines/linux/disks-enable-customer-managed-keys-cli", "https://learn.microsoft.com/en-us/azure/virtual-machines/linux/disks-enable-host-based-encryption-cli", "https://learn.microsoft.com/en-us/cli/azure/disk-encryption-set"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing a VM disk encryption option

**Goal:** the least complex option that meets the compliance requirement.

| Option | What it covers | Notes |
|---|---|---|
| SSE with platform-managed keys | OS and data disks, snapshots, images, encrypted at rest | On by default, managed by Microsoft; does not encrypt temp disks or disk caches |
| SSE with customer-managed keys (CMK) | Same, with your RSA keys in Key Vault or Managed HSM via a **Disk Encryption Set** | You can disable keys or revoke access at any time; disabled, deleted or expired keys shut down the VMs that use them |
| Double encryption at rest | An extra infrastructure-layer encryption using a different algorithm/mode and platform-managed keys | For customers worried about one algorithm, implementation or key being compromised; not supported on Ultra Disks or Premium SSD v2 |
| Encryption at host | Temp disks, OS/data disk caches, and data flowing to Storage | Needs the `EncryptionAtHost` feature registered on the subscription and a supported VM size |
| Azure Disk Encryption (ADE) | In-guest BitLocker (Windows) or DM-Crypt (Linux), keys in Key Vault | Uses the VM's CPU. Scheduled for retirement on September 15, 2028: use encryption at host for new VMs |
| Confidential disk encryption | Binds disk encryption keys to the VM's TPM (OS disk; temp disk is opt-in) | For confidential VMs |

## Typical decisions
- Default compliance: SSE with platform-managed keys. Need control of keys: SSE CMK.
- Need the temp disk and caches encrypted: add encryption at host.
- ADE and encryption at host cannot be combined: encryption at host can't be enabled on a VM or scale set that currently or ever had ADE enabled, and ADE can't be enabled on disks with encryption at host.
- CMK restrictions to know: key store and disks in the same region; only RSA keys of 2,048, 3,072 or 4,096 bits; HSM keys need Key Vault Premium; up to 5000 disk encryption sets per region per subscription.

## CMK setup (outline)
```bash
az disk-encryption-set create -g rg -n des1 --key-url <KEYVAULT_KEY_URL> --source-vault <KV_ID> --enable-auto-key-rotation true
az vm create ... --os-disk-encryption-set <DES_ID> --encryption-at-host
```
The Key Vault must have purge protection enabled (mandatory for managed-disk encryption). Grant the disk encryption set's identity the `get`, `wrapkey` and `unwrapkey` key permissions (for a Managed HSM, the "Managed HSM Crypto Service Encryption User" role). Identity creation can take a few minutes.

## Register encryption at host
`az feature register --namespace Microsoft.Compute --name EncryptionAtHost`, then check with `az feature show --namespace Microsoft.Compute --name EncryptionAtHost` until the state is Registered.

## Check
`az vm show -n vm -g rg --query [securityProfile.encryptionAtHost] -o tsv`, `az disk show -g rg -n disk --query [encryption.type] -o tsv`. Defender for Cloud has recommendations that detect encryption at host and ADE (see the overview page).

## Checked
Date: 2026-11-07
Read in full: Learn "Overview of managed disk encryption options" (comparison table, ADE retirement notice, Defender recommendations); "Server-side encryption of Azure Disk Storage" (platform vs customer keys, CMK restrictions, key disable behaviour, double encryption, encryption at host restrictions); "Use the Azure CLI to enable server-side encryption with customer-managed keys" and "...end-to-end encryption using encryption at host" (purge protection, set-policy permissions, Managed HSM role, feature register/show, `--encryption-at-host`, status queries); `az disk-encryption-set` reference (`--key-url`, `--source-vault`, `--enable-auto-key-rotation` found by search of the page, not read line by line).
Removed or fixed: "PMK plus CMK" for double encryption (page says platform-managed keys); "soft delete" requirement, "Key Vault Crypto Service Encryption User" role, `az provider register` step and the Azure Policy audit claim (none on the pages); `--encryption-at-host true` changed to the bare flag the page uses; ADE "can affect performance" replaced by the table's "uses the VM's CPU"; confidential disk wording changed from attestation to the TPM wording on the page.
Method: documentation only; no commands were run.
