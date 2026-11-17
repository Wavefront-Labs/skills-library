---
id: computing-software.cloud-infrastructure-engineering.azure.blob-storage-sftp-local-users-and-nfs-3
name: blob-storage-sftp-local-users-and-nfs-3
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, blob-storage, blob-sftp, sftp-local-users, nfs-3-blob, adls-gen2, protocol-support]
level: practitioner
status: docs-checked
description: "Expose Blob Storage over SFTP with local users and over NFS 3.0: prerequisites, permissions, network rules, mount options, costs and limitations."
sources: ["https://learn.microsoft.com/azure/storage/blobs/secure-file-transfer-protocol-support", "https://learn.microsoft.com/azure/storage/blobs/secure-file-transfer-protocol-support-authorize-access", "https://learn.microsoft.com/azure/storage/blobs/secure-file-transfer-protocol-support-entra-id-based-access", "https://learn.microsoft.com/azure/storage/blobs/network-file-system-protocol-support-how-to", "https://learn.microsoft.com/azure/storage/blobs/network-file-system-protocol-known-issues"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blob Storage over SFTP and NFS 3.0

**Goal:** give partners SFTP drop zones and Linux workloads NFS mounts directly on Blob Storage - no file server VMs.

## Prerequisite
Both need **hierarchical namespace** (ADLS Gen2) enabled. NFS 3.0 cannot be enabled on an existing account: choose it at account creation (standard general-purpose v2 or premium block blob accounts).

## SFTP
```bash
az storage account update -g rg -n stpartners --enable-sftp true
az storage account local-user create -g rg --account-name stpartners -n acme \
  --home-directory inbound \
  --permission-scope permissions=rw service=blob resource-name=inbound \
  --has-ssh-key true --ssh-authorized-key key="ssh-ed25519 AAAA... acme" --has-ssh-password false
```
- Connect: `sftp stpartners.acme@stpartners.blob.core.windows.net` (username = `<account>.<localuser>`).
- Permissions per container: Read, Write, List, Delete, Create, Modify Ownership and Modify Permissions; they apply to all directories and subdirectories in the container. Up to 50,000 local users per account.
- Microsoft Entra ID based access is also supported for SFTP (no local users needed); local users authenticate with an SSH key or password. Prefer SSH keys; rotate per partner.
- **Cost**: enabling SFTP has an hourly cost - disable it on idle accounts.
- Network: SFTP uses port 22.

## NFS 3.0
```bash
az storage account create -g rg -n stnfsdata -l westeurope --sku Premium_LRS --kind BlockBlobStorage \
  --enable-hierarchical-namespace true --enable-nfs-v3 true --default-action Deny
az storage account network-rule add -g rg --account-name stnfsdata --vnet-name vnet-app --subnet snet-app
sudo mount -t aznfs -o sec=sys,vers=3,nolock,proto=tcp stnfsdata.blob.core.windows.net:/stnfsdata/data /nfsdata
```
- Network security (virtual network, firewall rules, private endpoint) is the only way to secure NFS 3.0 access; account keys, Microsoft Entra and ACLs cannot authorise NFS requests (a named-user ACL entry makes the file inaccessible to non-root clients).
- NFS 3.0 uses ports 111 and 2048; the AZNFS Mount Helper package is the documented way to mount (`-t aznfs`).
- Not suited to workloads needing granular locking or sub-millisecond latency; file locking via Network Lock Manager is unsupported, so mounts must use `nolock`, and only NFS over TCP is supported.

## Gotchas
- Some Blob Storage features are unsupported or preview-only with NFS 3.0 or SFTP; check the Blob Storage feature support table before enabling.

## Verify
- [ ] Partner can upload only to their home directory; NFS mount works from the allowed subnet and fails from elsewhere.

## Checked

2026-10-24, against MicrosoftDocs/azure-docs (storage/blobs SFTP support, authorize-access, entra-id-based-access, NFS support-how-to and known-issues): HNS requirement, NFS only on new accounts, supported account kinds, SFTP hourly cost, port 22, username format, 50,000 local-user limit, Entra ID based SFTP access, permission list, `--enable-sftp`, local-user create parameters, NFS network-only security, ports 111 and 2048, `nolock`, TCP-only, `aznfs` mount type. Removed the wrong claim that SFTP has no Entra authentication, the POSIX ACL access-control claim, the unconfirmed requirement to turn off secure transfer, and the atomic-rename remark.

Method: documentation only; no commands were run.
