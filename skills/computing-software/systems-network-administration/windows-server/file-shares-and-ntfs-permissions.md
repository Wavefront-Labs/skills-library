---
id: computing-software.systems-network-administration.windows-server.file-shares-and-ntfs-permissions
name: file-shares-and-ntfs-permissions
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, file-server, smb, smb3, file-share, ntfs, ntfs-permissions, share-permissions, acl, icacls, agdlp, effective-access, access-based-enumeration, abe, new-smbshare, get-smbshare, smb-signing, smb1, smb-encryption, dfs, dfs-namespaces, dfs-replication, inheritance, fsrm, samba, effective-permissions-troubleshooting]
level: practitioner
status: gated
description: "Build Windows file shares right: share vs NTFS permissions, AGDLP groups, icacls, effective access, access-based enumeration, SMB signing and SMB1 off."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/file-server/file-server-smb-overview
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/icacls
  - https://learn.microsoft.com/en-us/powershell/module/smbshare/new-smbshare
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# File shares and NTFS permissions — one place to grant access, groups not people

**Goal:** publish SMB shares where access is controlled by NTFS ACLs on groups, is easy
to audit, and the protocol itself is hardened.

## 1. Share vs NTFS
Both the share permission and the NTFS permission apply to network access; confirm how they combine in Microsoft's SMB
documentation before relying on either layer.

Standard practice: set the **share** permission wide and do all real control in **NTFS**.
- Share: `Authenticated Users` (or `Everyone`) = Full Control (or Change, if you want a
  belt-and-braces cap).
- NTFS: specific domain-local groups, as below.

Two layers of restriction double the troubleshooting; keep one.

## 2. Group design: AGDLP
**A**ccounts go in **G**lobal groups (by role: `GG-Finance-Staff`), global groups go in
**D**omain **L**ocal groups (by resource and right: `DL-FS01-Finance-RW`,
`DL-FS01-Finance-RO`), and **P**ermissions are granted only to the DL groups.
Never put individual users on an ACL. Access reviews then become "who is in this group".
Group membership changes reach users through new logon tokens; plan for a re-logon.

## 3. Create the folder, ACL and share
```powershell
New-Item -Path <DRIVE>:\Shares\Finance -ItemType Directory
# Break inheritance, keep a copy, then clean up
icacls <DRIVE>:\Shares\Finance /inheritance:d
icacls <DRIVE>:\Shares\Finance /remove:g "Users" "Authenticated Users"
icacls <DRIVE>:\Shares\Finance /grant "CONTOSO\DL-FS01-Finance-RW:(OI)(CI)M" "CONTOSO\DL-FS01-Finance-RO:(OI)(CI)RX"
icacls <DRIVE>:\Shares\Finance /grant "SYSTEM:(OI)(CI)F" "BUILTIN\Administrators:(OI)(CI)F"

New-SmbShare -Name 'Finance$' -Path <DRIVE>:\Shares\Finance `
  -FullAccess "CONTOSO\Domain Admins" -ChangeAccess "Authenticated Users" `
  -FolderEnumerationMode AccessBased -CachingMode None
```
(`CONTOSO` is a placeholder domain; `<DRIVE>` is your data volume, ideally not the OS volume.) Notes:
- `(OI)(CI)` = inherit to files and subfolders. `M` (Modify) is the right ceiling for
  users; never give users Full Control, it lets them change ACLs and take ownership.

- Back up ACLs before big changes: `icacls <DRIVE>:\Shares\Finance /save acl.txt /t /c`;
  restore with `icacls <DRIVE>:\Shares /restore acl.txt`.
- A trailing `$` hides the share from browse lists; it is not a security control.

## 4. Access-based enumeration (ABE)
`-FolderEnumerationMode AccessBased` hides folders the user cannot read. Learn: SMB does not display files and folders to a user who lacks rights to them. Toggle with
`Set-SmbShare -Name 'Finance$' -FolderEnumerationMode AccessBased`.

## 5. Check effective access
- GUI: folder › Properties › Security › Advanced › **Effective Access** › select user,
  include group membership. Note it does not fully model the share layer.
- `Get-SmbShareAccess -Name 'Finance$'` for share perms; `icacls <path>` for NTFS.
- Avoid deny ACEs; use group design instead.

## 6. Harden SMB
```powershell
Get-SmbServerConfiguration | Select EnableSMB1Protocol, RequireSecuritySignature, EncryptData
Set-SmbServerConfiguration -EnableSMB1Protocol $false -Force
Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol
Set-SmbServerConfiguration -RequireSecuritySignature $true -Force
Set-SmbShare -Name 'Finance$' -EncryptData $true      # per-share SMB3 encryption
```
Confirm SMB1 is disabled and that signing and encryption settings suit your clients; defaults differ by Windows build,
so check Microsoft's SMB security documentation for yours. Block TCP 445 at the perimeter.

## 7. Scale out with DFS
DFS Namespaces (`\\<DOMAIN>\files\Finance`) decouple the path users see from the
server, so you can migrate servers without remapping drives.

## Verify
- [ ] Share permission is broad; NTFS holds the real control, granted only to DL groups.
- [ ] No individual user accounts and no `Everyone: Full Control` appear in `icacls` output.
- [ ] A test user in the RO group can read but not write; one in no group cannot see the folder (ABE).
- [ ] `EnableSMB1Protocol` is `False` and signing is required.
- [ ] An ACL backup exists from before the change.

## Checked
2026-10-28. Confirmed on Learn (New-SmbShare/Set-SmbShare, icacls): -FolderEnumerationMode AccessBased hides items the user lacks rights
to, -CachingMode/-EncryptData/-FullAccess/-ChangeAccess parameters, icacls (OI)/(CI) inheritance flags and /save and
/restore. Removed as unconfirmed: the ticket-percentage claim, "most restrictive" rule wording, Kerberos refresh/klist
detail, CREATOR OWNER note, ABE CPU cost, deny-versus-inherited-allow rule, SMB1/2025 signing default statements, DFS-R
locking claim. Remaining items not checked on a fetched page: the exact icacls switch spellings (/inheritance:d, /remove:g),
the SMB server configuration cmdlets and Get-SmbShareAccess (gated: unconfirmed, source is paywalled or blocked).
Method: documentation only; no commands were run.
