---
id: computing-software.systems-network-administration.active-directory.trace-account-lockout-source
name: trace-account-lockout-source
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, password-policy, account-lockout, event-4740, event-4625, event-4771, lockout-source, caller-computer-name, badpwdcount, stale-credentials, unlock-adaccount]
level: practitioner
status: docs-checked
description: "Find what keeps locking an account: query 4740 on the PDC for the caller computer, then 4625/4771 on that host, and the usual culprits (mapped drives, phones, services)."
sources:
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4740
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Trace the source of account lockouts

## 1. Who and from where (PDC emulator)
The PDC emulator processes account lockouts; event **4740** names the
**Caller Computer Name**. It belongs to the *Audit User Account Management* subcategory.
```powershell
$pdc = (Get-ADDomain).PDCEmulator
Get-WinEvent -ComputerName $pdc -FilterHashtable @{LogName='Security'; Id=4740; StartTime=(Get-Date).AddDays(-1)} |
  ? { $_.Properties[0].Value -eq 'jsmith' } |
  Select TimeCreated, @{n='User';e={$_.Properties[0].Value}}, @{n='Caller';e={$_.Properties[1].Value}}
```
Also check bad password counts per DC:
```powershell
Get-ADDomainController -Filter * | % { Get-ADUser jsmith -Server $_.HostName -Properties badPwdCount,LastBadPasswordAttempt |
  Select @{n='DC';e={$_.HostName}},badPwdCount,LastBadPasswordAttempt }
```

## 2. What on the caller
- Caller is a **workstation/server**: look at its Security log for 4625 (logon failure,
  with process name and logon type) around the time. Logon type 3 = network, 4 = batch
  (scheduled task), 5 = service.
- Caller is an **Exchange/ADFS/RADIUS/VPN** server: the real source is a client behind it;
  check that service's own logs for the user and client address.
- Caller blank or not helpful: check 4771 (Kerberos pre-authentication failed, with the client address) and 4776
  (the DC attempted to validate credentials, NTLM) on DCs.

## 3. Usual culprits
- Saved credentials: Credential Manager (`cmdkey /list`), mapped drives with stored creds.
- Services/scheduled tasks running as the user with an old password.
- Mobile devices (mail, Wi-Fi), and disconnected RDP sessions on old servers
  (`quser /server:<host>`).
- Password guessing against an internet-facing sign-in: many users locked, not one.

## Unlock
```powershell
Unlock-ADAccount jsmith
Search-ADAccount -LockedOut | Select Name,LastBadPasswordAttempt
```

## Verify
- [ ] Source fixed (credential updated/removed) and no new 4740 for the user in 24 h.
- [ ] If many accounts are affected: the source address is blocked and the lockout policy is reviewed.

## Checked
2026-10-27, against the event 4740, 4771, 4776 and 4625 pages (Learn previous-versions, security auditing), the Appendix L events table, the understand-FSMO-roles article, and the cmdkey, quser, Get-ADDomain, Unlock-ADAccount and Search-ADAccount pages. Confirmed: 4740 fields (TargetUserName = locked-out account, TargetDomainName = Caller Computer Name) and its Audit User Account Management subcategory; PDC emulator processes lockouts; 4625 logon types 3 network, 4 batch, 5 service and its process, workstation and source address fields; 4771 and 4776 content; `cmdkey /list`; `quser /server:`; `Get-ADDomain` PDCEmulator; `Unlock-ADAccount`; `Search-ADAccount -LockedOut`. Removed as unconfirmed: the NTLM non-Windows remark, ActiveSync/ADFS/NPS specifics, 802.1X, spraying and smart/extranet lockout statements.

Method: documentation only; no commands were run.
