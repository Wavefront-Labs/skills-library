---
id: computing-software.it-support-helpdesk.desktop-support.mapped-drives-and-file-share-access
name: mapped-drives-and-file-share-access
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, windows-networking, mapped-drives, smb, unc-path, net-use, group-policy-preferences, drive-maps, access-denied, ntfs-permissions, share-permissions, enablelinkedconnections]
level: practitioner
status: draft
description: "Map network drives that survive reboots, VPN and elevation, and diagnose 'access denied', red X drives and 'network path not found' on SMB shares."
sources:
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/net-use"
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-client/networking/mapped-drives-not-available-from-elevated-command"
  - "https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/dn581922(v=ws.11)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# mapped-drives-and-file-share-access

Goal: the user's S: drive is there every morning and opens; when it doesn't,
find out whether it's name resolution, transport, authentication or
permissions.

## Mapping methods
- Fleet: **Group Policy Preferences → Drive Maps** with action **Update**
  and item-level targeting by group; or Intune (PowerShell script / ADMX
  ingestion) for cloud-only devices. Users shouldn't map by hand.
- Ad hoc: `net use S: \\fs01\shared /persistent:yes`
  or `New-PSDrive -Name S -PSProvider FileSystem -Root \\fs01\shared -Persist`.

## Triage ladder
1. `Test-NetConnection fs01 -Port 445` — False = network/firewall/VPN (many
   ISPs and guest Wi-Fi block 445; only works over VPN).
2. `Resolve-DnsName fs01` — wrong/no answer = DNS suffix or VPN DNS.
3. `net use` — status "Unavailable"/"Disconnected" vs OK.
4. `dir \\fs01\shared` — "Access is denied" = permissions or wrong
   credentials cached; "network name cannot be found" = share name wrong.
5. `cmdkey /list` — stale stored credential for fs01 overriding the user's
   Kerberos ticket; delete with `cmdkey /delete:fs01`.
6. `klist` — Kerberos ticket for `cifs/fs01`; using an IP or an alias without
   SPN falls back to NTLM, which may be blocked.

## Permissions
Effective access = the more restrictive of **share** permissions and **NTFS**
permissions. Check NTFS: folder → Properties → Security → Advanced →
Effective Access → pick the user. Group membership changes need a new logon
token (sign out/in, or `klist purge` for Kerberos) before they apply.

## Common symptoms
- Red X at logon, opens on click: drive maps before the network is up
  (Wi-Fi/VPN) — enable "Always wait for the network at computer startup and
  logon" or ignore; it's cosmetic.
- Drives missing in elevated apps (installers, admin cmd): UAC split token;
  set `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System`
  `EnableLinkedConnections=1` (DWORD) and reboot.
- Drive shows old server after migration: GPP action "Create" doesn't
  overwrite — switch to "Replace" or "Update".

## Gotchas
- SMB1 is disabled on modern Windows; old NAS boxes needing it should be
  upgraded, not have SMB1 re-enabled.
- Offline Files (CSC) can show stale content; check Sync Center.

## Verify
`net use` shows OK, the user can create and delete a test file in the
share, drive persists after sign-out/in and over VPN.
