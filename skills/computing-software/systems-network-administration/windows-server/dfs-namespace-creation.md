---
id: computing-software.systems-network-administration.windows-server.dfs-namespace-creation
name: dfs-namespace-creation
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, dfs-namespaces, new-dfsnroot, new-dfsnfolder, dfs-folder-targets, domain-based-namespace, windows-server-2008-mode, abe, dfsn-module, namespace-servers]
level: practitioner
status: docs-checked
description: "Build a domain-based DFS namespace in 2008 mode: namespace servers, root and folder targets with New-DfsnRoot/New-DfsnFolder, ABE, and migrating servers behind it."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/dfs-namespaces/dfs-overview
  - https://learn.microsoft.com/en-us/windows-server/storage/dfs-namespaces/create-a-dfs-namespace
  - https://learn.microsoft.com/en-us/windows-server/storage/dfs-namespaces/choose-a-namespace-type
  - https://learn.microsoft.com/en-us/windows-server/storage/dfs-namespaces/change-the-amount-of-time-that-clients-cache-referrals
  - https://learn.microsoft.com/en-us/windows-server/storage/dfs-namespaces/enable-access-based-enumeration-on-a-namespace
  - https://learn.microsoft.com/en-us/powershell/module/dfsn/new-dfsnroot
  - https://learn.microsoft.com/en-us/powershell/module/dfsn/new-dfsnfoldertarget
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create a DFS namespace

**Goal:** users map `\\ad.example.com\files\Finance`; the real server behind it can change
without touching clients.

## Build
```powershell
Install-WindowsFeature FS-DFS-Namespace -IncludeManagementTools    # on each namespace server
# root share on each namespace server
New-Item <DATA_DRIVE>:\DFSRoots\files -ItemType Directory
New-SmbShare -Name files -Path <DATA_DRIVE>:\DFSRoots\files -ReadAccess '<DOMAIN_FQDN>\<GROUP_NAME>'
New-DfsnRoot -Path '\\ad.example.com\files' -TargetPath '\\ns01\files' -Type DomainV2 -EnableAccessBasedEnumeration $true
New-DfsnRootTarget -Path '\\ad.example.com\files' -TargetPath '\\ns02\files'
# folders pointing at real shares
New-DfsnFolder -Path '\\ad.example.com\files\Finance' -TargetPath '\\fs01\Finance$'
New-DfsnFolderTarget -Path '\\ad.example.com\files\Finance' -TargetPath '\\fs02\Finance$' -State Offline   # standby target
```
- **DomainV2** (Windows Server 2008 mode): supports access-based enumeration and larger namespaces; it needs forest functional level Windows Server 2003 or higher and domain functional level Windows Server 2008 or higher, with Windows Server 2008 or newer namespace servers. Prefer it when the environment supports it.
- Add a second namespace server for availability.
- Permissions on the namespace root folder are independent of the permissions on the target folders; set both. ABE hides folders from users without access but does not stop a referral to a target whose path is already known; control visibility of individual DFS folders with `Grant-DfsnAccess` or the folder's view permissions.

## Migrate a file server behind the namespace
1. Copy data to the new server, share it.
2. Add the new share as a folder target (Offline), final sync, then set new target Online
   and old Offline (`Set-DfsnFolderTarget -State`).
3. Clients follow at referral cache expiry (default 1800 seconds for folder referrals, 300 for root referrals); then remove the old target.

## Verify
- [ ] `Get-DfsnRootTarget '\\ad.example.com\files'` shows both namespace servers Online.
- [ ] A client's `dfsutil cache` output (see `dfsutil cache /?`) or the folder's Properties > DFS tab shows the active target.

## Checked

Checked 2026-10-25 against the MicrosoftDocs/windowsserverdocs and windows-powershell-docs (Windows Server 2025 DFSN/DFSR modules) repositories, latest commit 2026-10-23. Confirmed: `New-DfsnRoot` `-Type` values Standalone, DomainV1, DomainV2 and `-EnableAccessBasedEnumeration`; DomainV2 functional-level and server requirements; root share creation with `New-SmbShare -ReadAccess`; root and folder permissions are independent; ABE does not block referrals; referral cache defaults of 300 seconds (root) and 1800 seconds (folders); `dfsutil` has `cache` and `diag` command groups. Removed the reparse-point remark, the claim about DCs hosting namespaces and the `dfsutil cache referral` subcommand, which the checked pages do not state.

Method: documentation only; no commands were run.
