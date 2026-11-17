---
id: computing-software.digital-forensics-incident-response.evidence-handling.snapshotting-azure-managed-disks-for-forensics
name: snapshotting-azure-managed-disks-for-forensics
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [azure-disk-snapshot, cloud-snapshot, cloud-evidence, azure-incident-response, dfir]
level: advanced
status: docs-checked
description: "Preserve Azure VM disks: managed disk snapshots, SAS read access, and Microsoft's chain-of-custody reference design (SOC subscription, immutable blobs, hashes in Key Vault)."
sources: ["https://learn.microsoft.com/en-us/azure/virtual-machines/snapshot-copy-managed-disk", "https://learn.microsoft.com/en-us/azure/architecture/example-scenario/forensics/", "https://learn.microsoft.com/en-us/cli/azure/snapshot"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snapshotting Azure managed disks for forensics

**Goal:** snapshot the OS and data disks of a suspect Azure VM, move the copy to a separate SOC subscription, and keep a hash chain, following Microsoft's reference architecture "Computer forensics chain of custody in Azure". That article is based on its authors' knowledge; validate it with your legal department before legal use.

## Snapshot
A managed disk snapshot is a full, read-only, point-in-time copy of an OS or data disk that exists independently of the source disk.
```bash
az vm show -g RG -n VM --query "storageProfile.osDisk.managedDisk.id" -o tsv
az snapshot create -g RG --source "<osDiskId>" --name VM-os-snap-CASE014 --tags case=CASE014
az snapshot list -g RG -o table
```
- Snapshots are billed on used size, separately from the source disk. The default is locally redundant standard storage, and Microsoft recommends standard over premium storage (premium costs more). For zone-redundant storage use a region with availability zones and `--sku Standard_ZRS`.
- `az snapshot create` also takes `--incremental {false, true}`: incremental snapshots on the same disk occupy less space and can be diffed.
- Snapshot every attached disk (OS and data). Ephemeral OS disks do not support snapshots, so the reference design requires persistent managed OS disks on VMs where evidence collection is needed.

## Move to the SOC subscription
- Cross-resource-group copy: pass the full resource ID as `--source` (the CLI reference shows this form for another resource group).
- Export: `az snapshot grant-access --duration-in-seconds 3600 --name SNAP --resource-group RG` grants read access via a SAS that expires after the given seconds (`--access-level` takes Read or Write; `--file-format VHDX` is also shown). Copy it into the evidence storage account, then revoke with `az snapshot revoke-access`.
- Reference design: the SOC subscription, accessible only to the SOC team, holds a storage account whose container has a legal hold policy (immutable blob storage, write once read many) and a dedicated Key Vault holding the snapshot hash values. The Copy-VmDigitalEvidence runbook, run from an Automation hybrid runbook worker using a system-assigned managed identity, snapshots the OS and data disks, copies them to the immutable container and a temporary file share, hashes the file-share copy, stores the hash in Key Vault and deletes all copies except the immutable one. Supported hash algorithms: MD5, SHA256, SKEIN, KECCAK (SHA3).
- The identity needs Storage Account Contributor on the SOC storage account, Key Vault Secrets Officer on the SOC key vault, and Contributor on the target VM's resource group (which gives snapshot rights).
- Enable secure transfer and the firewalls on the storage account and key vault, allowing only the SOC virtual network. Keep the hybrid worker's network unconnected to the hub.
- Only two SOC custodians should be able to change RBAC. Give investigators a read-only SAS URI that expires (the article's example is eight hours) and add their IPs to the storage firewall allow list.
- Azure audit logs record who took a snapshot and when. Legal-hold snapshots cannot be deleted, so storage cost accumulates.

## Analyse
Investigators can attach disk copies to a computer dedicated to forensic analysis without powering on or accessing the original VM. To recover from a snapshot, create a managed disk from it, then attach it as a data disk (or use it as an OS disk for a new VM).

## Verify
Snapshot IDs, hashes and audit log entries are recorded in the evidence register.

## Checked
Confirmed against the Azure managed disk snapshot page (snapshot definition, billing, default storage, CLI commands), the chain of custody architecture article (workflow, roles, immutability, hashes, SAS handling, ephemeral OS disk limit) and the az snapshot CLI reference (create, list, grant-access, revoke-access, `--incremental`). Removed claims the pages do not give: crash-consistent behaviour, Azure Disk Encryption Key Vault secret handling, the CanNotDelete resource lock, dc3dd imaging and the `azcopy` command.

Method: docs-only read of cited pages, 2026-11-08
