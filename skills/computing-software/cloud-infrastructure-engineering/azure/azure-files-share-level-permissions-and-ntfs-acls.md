---
id: computing-software.cloud-infrastructure-engineering.azure.azure-files-share-level-permissions-and-ntfs-acls
name: azure-files-share-level-permissions-and-ntfs-acls
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-files, share-level-permissions, ntfs-acls, icacls, default-share-permission, smb]
level: practitioner
status: docs-checked
description: "Authorise Azure Files SMB access in two layers: share-level RBAC or default share permission, then directory/file NTFS ACLs with icacls - without mounting by key day to day."
sources: ["https://learn.microsoft.com/azure/storage/files/storage-files-identity-assign-share-level-permissions", "https://learn.microsoft.com/azure/storage/files/storage-files-identity-configure-file-level-permissions", "https://learn.microsoft.com/windows-server/administration/windows-commands/icacls"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Files share-level permissions and NTFS ACLs

**Goal:** file-server-like permissions on Azure Files with identity-based auth (AD DS, Entra Kerberos or Entra DS).

## Layer 1: share level (Azure RBAC)
| Role | Access |
|---|---|
| Storage File Data SMB Share Reader | Read |
| Storage File Data SMB Share Contributor | Read, write, delete |
| Storage File Data SMB Share Elevated Contributor | Read, write, delete, and modify ACLs |
| Storage File Data Privileged Contributor | Read, write, delete, and modify ACLs, overriding existing ACLs |
```bash
az role assignment create --assignee <group-objectId> --role "Storage File Data SMB Share Contributor" \
  --scope "/subscriptions/<sub>/resourceGroups/rg/providers/Microsoft.Storage/storageAccounts/stfiles/fileServices/default/fileshares/finance"
# or one default for every authenticated identity (common when NTFS does the real work)
az storage account update -g rg -n stfiles --default-share-permission StorageFileDataSmbShareContributor
```

## Layer 2: NTFS ACLs
Mount as an admin with the privileged role, then:
```powershell
icacls Z:\ /grant "CONTOSO\FileAdmins:(OI)(CI)F"
icacls <DRIVE>:\Finance /grant "CONTOSO\Finance-RW:(OI)(CI)M" "CONTOSO\Finance-RO:(OI)(CI)RX"
icacls <DRIVE>:\Finance /remove "Authenticated Users"
icacls <DRIVE>:\Finance
```
Or Windows Explorer > Security tab (when mounted from a domain-joined machine).
Effective access = most restrictive of share-level and NTFS.

## Gotchas

## Verify
- [ ] Test user in Finance-RO can read but not write `\\stfiles.file.core.windows.net\finance\Finance`; `icacls` output matches the design.

## Checked
2026-10-28. Confirmed on the assign-share-level-permissions and configure-file-level-permissions pages: the SMB share role names and what they grant (Contributor, Elevated Contributor, Privileged Contributor), `az role assignment create` and `az storage account update --default-share-permission`, share-level plus NTFS being evaluated together, `icacls` `/grant` and `/remove` syntax and `(OI)(CI)` flags.
Removed (not confirmed): the cloud-only group claim, the `/inheritance:r` step, the root-of-share default permission claim, account-key bypass note, `klist purge` advice and the robocopy `/COPY` flags.

Method: documentation only; no commands were run.
