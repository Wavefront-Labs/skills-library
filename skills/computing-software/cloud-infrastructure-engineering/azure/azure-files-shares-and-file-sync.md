---
id: computing-software.cloud-infrastructure-engineering.azure.azure-files-shares-and-file-sync
name: azure-files-shares-and-file-sync
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-files, file-shares, smb, nfs-shares, nfs-4-1, azure-file-sync, cloud-tiering, sync-group, server-endpoint, identity-based-authentication, entra-kerberos, ad-ds-authentication, premium-file-shares, provisioned-v2, share-snapshots, soft-delete, smb-multichannel, smb-over-quic, port-445, azure-files-backup, large-file-shares]
level: practitioner
status: draft
description: "Run Azure Files: SMB vs NFS, standard vs premium, identity-based auth (AD DS or Entra Kerberos) with share and NTFS ACLs, port-445 workarounds, snapshots, File Sync with cloud tiering."
sources: ["Microsoft Learn - Planning for an Azure Files deployment", "Microsoft Learn - Overview of Azure Files identity-based authentication for SMB access", "Microsoft Learn - Enable Microsoft Entra Kerberos authentication for hybrid identities on Azure Files", "Microsoft Learn - Planning for an Azure File Sync deployment and cloud tiering", "Microsoft Learn - NFS Azure file shares"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Azure Files — shares that replace the file server, with the ACLs users expect

**Goal:** SMB/NFS shares with identity-based permissions, right-sized performance, and
on-prem servers turned into caches via File Sync rather than copies.

## 1. Choose protocol and tier
- **SMB 3.x** (Windows, Linux cifs, macOS): identity auth, snapshots, Backup, File Sync.
- **NFS 4.1**: premium (FileStorage) accounts only, Linux, no identity auth (network-only
  security — private endpoint/service endpoint mandatory, `--default-action Deny`), no File Sync/Backup (use snapshots).
- **Standard** (GPv2, HDD, pay-per-GiB + transactions; large file shares up to 100 TiB) vs
  **Premium** (SSD, provisioned, ms latency, 100 TiB, IOPS scale with size — size up for IOPS
  even when capacity isn't needed). The **provisioned v2** billing model (2025) lets you set
  IOPS/throughput independently on both tiers in supported regions — prefer it for new shares.
```bash
az storage share-rm create --storage-account stfiles -n hr --quota 1024 --enabled-protocols SMB --access-tier TransactionOptimized
```

## 2. Identity-based auth for SMB
Options: **on-prem AD DS** (classic: `Join-AzStorageAccount` from the AzFilesHybrid module
creates a computer/service account in AD; Kerberos tickets from domain-joined clients;
needs line-of-sight to a DC), **Entra Kerberos for hybrid identities** (no DC
line-of-sight — good for AVD/roaming: `az storage account update --enable-files-aadkerb true
--domain-name corp.example.com --domain-guid <guid>`; clients must be Entra joined/hybrid
joined; still needs AD-synced users and an admin consent on the auto-created app), or
**Entra Domain Services**.
Then two permission layers:
1. **Share-level** RBAC: *Storage File Data SMB Share Reader / Contributor / Elevated
   Contributor* assigned to groups (or set a default share-level permission for all authenticated).
2. **NTFS ACLs** on directories/files, set once via `icacls` from a mount using the
   storage key (`net use Z: \\stfiles.file.core.windows.net\hr /user:Azure\stfiles <key>`),
   then users mount with their own identity.
RBAC to **Storage File Data Privileged Contributor** bypasses NTFS for migrations.

## 3. Mounting and port 445
- Windows: `net use Z: \\stfiles.file.core.windows.net\hr` (Kerberos) — the portal's
  *Connect* script handles persistence and credential store.
- Linux: `mount -t cifs //stfiles.file.core.windows.net/hr /mnt/hr -o vers=3.1.1,credentials=/etc/smbcred,dir_mode=0777,file_mode=0777,serverino,nosharesock,actimeo=30`
  (key-based; identity auth on Linux needs Kerberos + `sec=krb5`).
- ISPs and many corporate firewalls block outbound **TCP 445**: use VPN/ExpressRoute +
  private endpoint, or **SMB over QUIC** (443, Windows Server 2022 Azure Edition / Windows 11 clients via File Sync server or Azure Edition VM).
- Performance: SMB Multichannel on premium (`az storage account file-service-properties update --enable-smb-multichannel true`), `nconnect` on NFS, and premium share sizing for IOPS.

## 4. Protection
- **Share snapshots**: `az storage share snapshot` (200 per share, incremental); users
  restore via Previous Versions in Explorer. Azure Backup for Files schedules snapshots and
  keeps them in a vault policy (daily/weekly/monthly, up to 10 years); soft delete on
  shares (`--enable-delete-retention-policy`) protects against share deletion.
- Standard shares are LRS/ZRS/GRS; premium LRS/ZRS only. NFS: snapshots only, plan your own copy.

## 5. Azure File Sync
Storage Sync Service → **sync group** (one cloud endpoint = one share) → **server
endpoints** (a folder on each registered Windows Server, 2016+). Agent from the portal,
`Register-AzStorageSyncServer`. **Cloud tiering**: `-CloudTiering -VolumeFreeSpacePercent 20
-TierFilesOlderThanDays 30` keeps hot files local, tiers the rest to the share (reparse
points; backup software must respect them — use Azure Backup on the share, not on
tiered servers). Initial sync: pre-seed with the server as the source; don't also bulk-copy
to the share (conflict renames). Max 100 server endpoints/sync group; each server volume
needs NTFS, not ReFS/dedup-on-tiered.
Branch office pattern: one share, File Sync on each site's server as a cache, Backup on the cloud side.

## Gotchas
- Entra Kerberos and AD DS auth are mutually exclusive per account; AVD FSLogix with Entra-only clients needs Entra Kerberos.
- `TransactionOptimized` vs `Hot` vs `Cool` on standard shares changes transaction vs storage price dramatically for file-server-style chatter (metadata ops are transactions).
- NFS 4.1 shares historically need *Secure transfer required* **off** on the account (NFS has no TLS); encryption in transit for NFS is a newer, region-gated feature — unconfirmed for your region, check before relying on it.
- Deleting a share with File Sync attached orphans server endpoints — remove the cloud endpoint first.
- Large file shares (>5 TiB) require `--enable-large-file-share` on standard accounts; it's irreversible but harmless.

## Verify
- [ ] Domain user on a hybrid-joined client maps the share without a credential prompt; `klist` shows a `cifs/stfiles.file.core.windows.net` ticket.
- [ ] Denied NTFS folder returns access denied for a user who has share-level Contributor.
- [ ] `az storage share-rm show --query "{tier:accessTier,quota:shareQuota,prov:provisionedIops}"` matches sizing.
- [ ] File Sync health: server endpoint *Healthy*, tiering frees space to the configured threshold, recalled file opens within seconds.
