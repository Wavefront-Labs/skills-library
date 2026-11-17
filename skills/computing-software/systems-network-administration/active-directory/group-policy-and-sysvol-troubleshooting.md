---
id: computing-software.systems-network-administration.active-directory.group-policy-and-sysvol-troubleshooting
name: group-policy-and-sysvol-troubleshooting
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, group-policy, gpo, sysvol, netlogon, dfsr, frs, dfsr-migration, dfsrmig, gpt-ini, gpc, gpt, version-mismatch, gpresult, rsop, gpsvc-debug, gpsvc-log, event-1058, event-1030, event-1129, event-4012, event-2213, authoritative-restore, msdfsr-options, slow-link, policy-not-applying, wmi-filter, security-filtering, authenticated-users, ms16-072, dcdiag]
level: advanced
status: docs-checked
description: "Fix GPOs that don't apply and broken SYSVOL: MS16-072 filtering, gpsvc logs, key events, DFSR health, dirty shutdown and authoritative SYSVOL restore."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/group-policy/applying-group-policy-troubleshooting-guidance
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/group-policy/force-authoritative-non-authoritative-synchronization
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/group-policy/cannot-apply-user-gpo-when-computer-objects-dont-have-read-permissions
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/ntfrs-deprecation-blocks-replic-dc-installation
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/dfsrmig
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Group Policy and SYSVOL troubleshooting — find which half of the GPO is broken

**Goal:** when "the GPO isn't applying", decide in minutes whether it's scope,
processing, or SYSVOL replication, and repair SYSVOL without making it worse.

## 1. Know the two halves
A GPO is the **GPC** (the Group Policy Container in AD, replicated by AD replication) and
the **GPT** (the Group Policy template files in `\\<DC>\SYSVOL\<DOMAIN>\Policies\<GUID>`,
including `gpt.ini`, replicated by **DFSR**). If the GPT is missing or stale on the DC a
client talks to, the GPO is skipped or half-applied.

## 2. Is the client even in scope?
```cmd
gpresult /h gp.html
gpresult /r
```
The report shows the GPOs that did not apply and why. The GroupPolicy Operational log also lists
applied and denied GPOs with the reasons for denial.
- **MS16-072 gotcha:** since the June 2016 update, user policy is retrieved in the *computer's* security
  context. If you removed *Authenticated Users* from security filtering to target a user
  group, the computer account still needs **Read** on the GPO: grant **Read** to Authenticated Users
  (this does not restore Apply), to **Domain Computers**, or to specific computers or a group of them.
  Make sure none of them is explicitly denied. Domain controllers are usually unaffected because
  *Enterprise Domain Controllers* has Read by default.
- `Get-GPPermission -Name <GPO> -All` lists the permissions on a GPO.

## 3. Processing errors on the client
Event Viewer → *Applications and Services Logs → Microsoft → Windows → GroupPolicy →
Operational* shows the processing steps.
- **1058** "could not read a file from a DC": name resolution or network connectivity to the DC,
  replication latency (the file has not replicated to that DC), or the DFS client disabled.
  Test by reading `\\<DC>\SYSVOL\<DOMAIN>\Policies\<GUID>\gpt.ini` as the failing user or computer.
- **1030/1006**: failed to retrieve policy settings; check name resolution and that LDAP
  (port 389) is reachable on the DC, and the `Get-GPPermission` output for the GPC.
- **1129**: no network connectivity to a DC (for example LDAP port 389 blocked, or the NIC
  not ready at startup).
Deep dive: enable gpsvc debug logging
(`HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Diagnostics`, DWORD
`GPSvcDebugLevel = 0x30002`; create `%windir%\debug\usermode` or no log is written), reproduce, read
`gpsvc.log`. Set the value back to 0 afterwards.

## 4. SYSVOL health (DFSR)
```powershell
dfsrmig /getglobalstate           # run on the PDC emulator; must be 'Eliminated' (FRS removed)
Get-SmbShare SYSVOL, NETLOGON     # on every DC
dcdiag /test:sysvolcheck /test:advertising /e
Get-WinEvent -LogName 'DFS Replication' -MaxEvents 50
```
- **4012** — DC was offline beyond `MaxOfflineTimeInDays` (60 default); DFSR stopped
  replicating SYSVOL on it. Do a non-authoritative sync (below), don't raise the limit.
- **2213** — dirty shutdown, replication paused. The event text gives a
  `ResumeReplication` WMI command; run it only after confirming the DB isn't the only
  good copy.
- Backlog between DCs: `Get-DfsrBacklog -GroupName "Domain System Volume" -FolderName
  "SYSVOL Share" -SourceComputerName <DC1> -DestinationComputerName <DC2>`.
- Still on FRS? Migrate with `dfsrmig /setglobalstate 1`, `2`, `3` waiting for
  `/getmigrationstate` to converge between steps (the Eliminated state is irreversible).
  Windows Server 2016 is the first release that ends FRS support, and promotion of newer
  replica DCs is blocked while SYSVOL still uses FRS.

## 5. Authoritative vs non-authoritative SYSVOL sync
- **Non-authoritative** (one bad DC): set `msDFSR-Enabled=FALSE` on that DC's
  `CN=SYSVOL Subscription` object, replicate AD, run `dfsrdiag pollad`, wait for event **4114**, set it back to
  TRUE, replicate, run `dfsrdiag pollad`, wait for **4614** then **4604**.
- **Authoritative** (all DCs broken; you pick the good copy, preferably the PDC emulator): stop DFSR on all DCs, set
  `msDFSR-Enabled=FALSE` everywhere and `msDFSR-options=1` on the chosen DC's
  subscription, then follow Microsoft's sequence exactly. Every other DC must then be synced
  non-authoritatively or you get conflicts — **back up SYSVOL from the good DC first**.

## 6. Repairing missing GPO content
If the GPT folder is missing on all DCs, restore the GPO from a `Backup-GPO` backup with `Restore-GPO`
(see `computing-software.systems-network-administration.windows-server.group-policy-management`).

## Verify
- [ ] The GPT folder for the GPO exists on every DC and replicates (no backlog).
- [ ] `gpresult` lists the GPO under Applied, not Denied, for the target.
- [ ] No 1058/1030 events on clients after `gpupdate /force`.
- [ ] `dfsrmig /getglobalstate` = Eliminated; SYSVOL and NETLOGON shared on every DC.
- [ ] No outstanding DFSR 4012/2213 events; backlog is zero.

## Checked
2026-10-27, against Microsoft Learn (SupportArticles-docs group-policy pages: "Applying Group Policy troubleshooting guidance", MS16-072 read-permission article, force authoritative/non-authoritative DFSR sync, NTFRS deprecation; dfsrmig and cmdlet pages). Confirmed: events 1058, 1030, 1006 and 1129 and their causes; gpsvc debug value 0x30002, key path, usermode folder and gpsvc.log; MS16-072 Read requirement and the three ways to grant it; dfsrmig states and irreversibility of Eliminated; DFSR events 4012, 2213, 4114, 4614, 4604; non-authoritative and authoritative sequences; Get-GPPermission, Get-DfsrBacklog, Backup-GPO and Restore-GPO. Removed as unconfirmed: GPC/GPT version-number checks and the GPMC Status tab claim, the GPC DN path, the gpresult denial-reason list, the "Always wait for the network" remark, the repair-by-edit step. Corrected: FRS support ended with Windows Server 2016 (not 2019).

Method: documentation only; no commands were run.
