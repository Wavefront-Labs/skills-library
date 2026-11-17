---
id: computing-software.it-support-helpdesk.desktop-support.smb-and-ntfs-permission-errors
name: smb-and-ntfs-permission-errors
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, smb-troubleshooting, icacls, smb-signing, ntfs-permissions, access-denied]
level: practitioner
status: docs-checked
description: "Fix file share access problems: how SMB signing is negotiated and when it blocks third-party devices, and backing up, granting and restoring NTFS ACLs with icacls."
sources:
  - "https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-signing-overview"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/icacls"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# smb-and-ntfs-permission-errors

## SMB signing as a cause of connection failures
- SMB signing is enabled in all versions of Windows; it adds a signature to each message to defeat tampering and relay.
- SMB 2.x/3.x signing is decided solely by whether it is required (`RequireSecuritySignature` = 1) on the client or
  server. Signing occurs if either side requires it and is not used only when both are 0. `EnableSecuritySignature`
  is ignored except for SMB1.
- Policy: Computer Configuration > Windows Settings > Security Settings > Local Policies > Security Options, "Microsoft
  network client/server: Digitally sign communications (always)".
- Domain controllers require signing by default (SYSVOL and NETLOGON). With a non-Microsoft file server the defaults
  can prevent a connection; Microsoft's "Control SMB signing behavior" page covers disabling the requirement.
- Prefer Kerberos: connecting by IP address or CNAME makes SMB use NTLM instead.
- Windows 11 24H2 can audit third-party servers or clients that do not support signing or encryption
  (`Set-SmbClientConfiguration -AuditServerDoesNotSupportSigning $true`; events in the SMBClient Audit log,
  IDs 31998 and 31999).

## icacls
```
icacls "<SHARE_ROOT>\Finance"                              & rem view the DACL
icacls "<SHARE_ROOT>\Finance" /save acl.txt /t             & rem back up ACLs first
icacls "<SHARE_ROOT>\Finance" /grant "CONTOSO\Finance-RW:(OI)(CI)M"
icacls "<SHARE_ROOT>\Finance\file.xlsx" /reset             & rem replace with default inherited ACL
icacls "<SHARE_ROOT>\Finance" /inheritancelevel:e          & rem enable inheritance
icacls "<SHARE_ROOT>" /restore acl.txt                     & rem restore (takes a directory)
```
- `/save` stores DACLs for later `/restore`; `/t` recurses; `/c` continues past file errors.
- `/grant` adds to existing explicit permissions; `/grant:r` replaces them.
- Basic rights: N none, F full, M modify, RX read and execute, R read-only, W write-only, D delete.
- `(OI)` object inherit and `(CI)` container inherit apply only to directories.
- `/setowner <user>` changes the owner. Use it only when admins are locked out, then restore correct permissions.
- `/inheritancelevel`: `e` enables inheritance, `d` disables and copies ACEs, `r` disables and removes inherited ACEs.
- SIDs may be names or numeric (prefix `*`). Canonical order: explicit denies, explicit grants, inherited denies, inherited grants.

## Verify
The user opens and saves a test file, and an ACL backup exists for any bulk change.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on the SMB signing overview and icacls pages. The cited SMBv1 troubleshooting page returned 404. Removed
as uncheckable: the error-message table (guest access, SMB1, error 53 and 1219), "Windows 11 24H2 requires signing
by default", share vs NTFS rules, Effective Access, and takeown. Corrected `/inheritance:e` to the documented
`/inheritancelevel:e`.
