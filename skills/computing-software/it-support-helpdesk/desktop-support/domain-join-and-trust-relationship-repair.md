---
id: computing-software.it-support-helpdesk.desktop-support.domain-join-and-trust-relationship-repair
name: domain-join-and-trust-relationship-repair
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, windows-networking, domain-join, domain-trust-relationship, secure-channel, test-computersecurechannel, nltest, add-computer, machine-account-password, active-directory]
level: practitioner
status: draft
description: "Join PCs to Active Directory correctly and fix 'The trust relationship between this workstation and the primary domain failed' without an unjoin/rejoin when possible."
sources:
  - "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/test-computersecurechannel"
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/troubleshoot-domain-join-error-messages"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/nltest"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# domain-join-and-trust-relationship-repair

Goal: put a machine in the domain in the right OU first time, and repair a
broken secure channel in a minute instead of a 30-minute rejoin.

## Joining
```powershell
Add-Computer -DomainName corp.example.com -OUPath "OU=Laptops,OU=Workstations,DC=corp,DC=example,DC=com" `
  -NewName LT-012345 -Credential CORP\svc-join -Restart
```
- Use a delegated join account (rights only on the workstation OUs), not a
  domain admin.
- Pre-stage the computer object if the default Computers container has no
  GPOs linked — machines landing there get no policy.
- DNS must point at domain controllers. "An Active Directory Domain
  Controller for the domain could not be contacted" is a DNS problem in 9 of
  10 cases: `nslookup -type=srv _ldap._tcp.dc._msdcs.corp.example.com`.
- Error `0x0000052E` = bad credentials; `0x00000A8B`/"account already exists"
  = object exists and your account can't reuse it — delete or reset it.

## The trust relationship failed
Cause: the computer's machine account password (rotated every 30 days) no
longer matches AD — restored from snapshot/System Restore, reimaged with the
same name, or offline > tombstone period.
Fix without rejoin — sign in with a **cached local admin** or cached domain
credentials with the network cable unplugged, then reconnect:
```powershell
Test-ComputerSecureChannel -Verbose            # False = broken
Test-ComputerSecureChannel -Repair -Credential CORP\svc-join
# or
Reset-ComputerMachinePassword -Server DC01 -Credential CORP\svc-join
nltest /sc_verify:corp.example.com
```
Reboot not required, but run `gpupdate /force` afterwards.

Last resort: unjoin to workgroup, delete or reset the AD object, rejoin with
the same name (group memberships of the computer object are lost if
deleted — note them first).

## Gotchas
- Windows LAPS or a local admin is needed to get in; if neither, use WinRE
  or a cached domain account with network disconnected.
- Hybrid-joined devices: after repair, run `dsregcmd /status` to confirm the
  Entra hybrid join is still healthy.
- Duplicate names across two machines will keep breaking each other; check
  the asset register before reusing a name.

## Verify
`Test-ComputerSecureChannel` returns True, `nltest /sc_query:<domain>` shows
`NERR_Success`, a domain user without cached creds can sign in.
