---
id: computing-software.systems-network-administration.active-directory.ntdsutil-set-dsrm-password
name: ntdsutil-set-dsrm-password
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-recovery, dsrm, ntdsutil-set-dsrm-password, directory-services-restore-mode]
level: practitioner
status: gated
description: "Reset a DC's Directory Services Restore Mode password with ntdsutil and synchronize it from a domain account so every DC has a known DSRM password."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/reset-directory-services-restore-mode-admin-pwd
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-R2-and-2008/cc754363(v=ws.10)
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Reset and synchronize the DSRM password

The DSRM password is the local administrator password of a DC, set when it was promoted, used to start the DC in
Directory Services Restore Mode for restores. Nobody remembers it from promotion day. Fix that before you need it.

## Reset on a running DC
```cmd
ntdsutil
set dsrm password
reset password on server null      REM null = this DC; or the DNS name of another DC
REM type the new password when prompted
q
q
```
You cannot use this on a server that is already running in DSRM. A Domain Admins member can reset it for the local DC
or for another DC in the domain.

## Sync from a domain account
`sync from domain account` performs a **one-time** synchronization of the DSRM administrator password from the named
domain user. Create a dedicated domain user (for example `dsrm-sync`) with a strong password, then on each DC:
```cmd
ntdsutil "set dsrm password" "sync from domain account dsrm-sync" q q
```
Run it across DCs:
```powershell
Invoke-Command -ComputerName (Get-ADDomainController -Filter *).HostName {
  ntdsutil "set dsrm password" "sync from domain account dsrm-sync" q q }
```
The DSRM password becomes that account's current password at the time of the sync, so re-run it after you change the
account's password. The reference notes the option needs Windows Server 2008 R2, or 2008 with SP3 or hotfix 961320;
all supported DC versions are newer.

## Modern alternative
Windows LAPS can manage and back up each DC's DSRM password (see the windows-laps-dsrm-password-backup skill).

## Use it
- Boot to DSRM: `bcdedit /set safeboot dsrepair` then reboot; log on as `.\Administrator` with the DSRM password
  (gated: unconfirmed, source is paywalled or blocked). The current bcdedit reference does not list the `dsrepair` value,
  so confirm it on a test server.
- Remove it afterwards: `bcdedit /deletevalue safeboot`. (gated: unconfirmed, source is paywalled or blocked)

## Verify
- [ ] Every DC's DSRM password is synced or LAPS-managed and stored in the vault; tested on one DC by booting to DSRM.

## Checked

Date: 2026-10-27. Documentation: Microsoft Support "How to reset the DSRM administrator account password" (2026-02),
ntdsutil `set DSRM password` reference (Windows Server 2008 / 2008 R2 archive page; no current-release page was
readable).
Confirmed: `set dsrm password`, `reset password on server null` or a DNS name, no reset while the target is in DSRM,
`sync from domain account` as a one-time sync and its minimum version.
Gated: the `bcdedit` safeboot values for entering and leaving DSRM.
Removed unconfirmed claims: the `DsrmAdminLogonBehavior` registry value, the "disabled user" and monthly scheduled-task
advice, and the "do not use both" statement for LAPS.

Method: documentation only; no commands were run.
