---
id: computing-software.systems-network-administration.active-directory.domain-join-failure-troubleshooting
name: domain-join-failure-troubleshooting
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, domain-join, netsetup-log, domain-join-errors, nltest]
level: practitioner
status: docs-checked
description: "Diagnose failed domain joins from netsetup.log: DNS lookup of the DC, error 1355, 2224 account exists, 8557 quota and secure channel issues."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/active-directory-domain-join-troubleshooting-guidance
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/failure-when-you-use-an-existing-computer-account-to-join-a-domain
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/status-code-0x216d-not-joined-domain
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/domain-join-log-analysis
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/access-denied-when-joining-computers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting domain join failures

The join wizard's error is vague; `%windir%\debug\netsetup.log` on the joining machine says exactly which step failed.

## Read the log
Find the final `NetpDoDomainJoin: status: 0x...` line, then read upward for the first non-zero status. The log is enabled by default.

## Common codes
| Code | Meaning | Fix |
|---|---|---|
| 0x54B / 1355 | specified domain cannot be contacted (DC location problem) | check DNS server addresses and suffix search order; test `nltest /dsgetdc:<domain>` |
| 0x8B0 / 2224 | account already exists (NERR_UserExists); with 0xAAC, reuse blocked by policy | see the hardening section below; delete a stale object |
| 0x216D / 8557 | user exceeded the limit of 10 computers, or a GPO restricts joining (*Add workstations to domain*) | use a delegated join account or pre-stage the object; check the user right |
| 0x5 / 5 | access denied | the joiner needs Create computer objects on the OU and, for an existing object, Reset Password on it; Account Operators need Read on the built-in OU |
| 0x40 / 64 | network name no longer available; trouble getting Kerberos tickets for the SMB session | see the 0x40 article; check SMB and Kerberos to the DC |
| 0x569 / 1385 | logon type not granted | the join account lacks *Access this computer from the network* on the DC that serves the join |
| 0x6BF / 1727 | RPC failed | a router, firewall or VPN device rejects packets between client and DC |
| 0x6D9 | no more endpoints from the endpoint mapper | connectivity blocked between client and DC |

## Basic tests from the joining machine
```powershell
Resolve-DnsName -Type SRV _ldap._tcp.dc._msdcs.corp.example.com
nltest /dsgetdc:corp.example.com
Test-NetConnection <DC> -Port 389; Test-NetConnection <DC> -Port 445; Test-NetConnection <DC> -Port 88
```
Ports needed from the client to the DC: DNS 53 (TCP and UDP), 389 (UDP and TCP), Kerberos 88 (TCP), RPC 135 and the
TCP dynamic range up to 65535, SMB 445. Kerberos needs time accurate to within 5 minutes.

## Hardening-related failures (2022+ updates)
Windows updates from October 11, 2022 onward (KB5020276, CVE-2022-38042) block reusing an existing computer account
(`0xaac` / 2732, NERR_AccountReuseBlockedByPolicy) unless the joiner created it, it was created by a member of an
administrator group, or its owner is in the *Domain controller: Allow computer account reuse during domain join*
Group Policy setting (needs the March 14, 2023 updates on members and DCs). Fixes: join with the creating account,
delete a stale account, rename the computer, or use that policy.

## Verify
- [ ] netsetup.log ends with `NetpDoDomainJoin: status: 0x0`.
- [ ] After reboot `Test-ComputerSecureChannel` returns True.

## Checked
2026-10-27, against the Learn article "Active Directory domain join troubleshooting guidance", the 0xaac/0x8b0, 0x216d, 0x54b, 0x569 and "Access is denied when joining computers" articles, and "Domain join log analysis" (SupportArticles-docs, current). Confirmed: netsetup.log location, default-on and the NetpDoDomainJoin status line; the port table; each code's cause (0x54B, 0x8B0, 0xAAC, 0x216D, 0x569, 0x6BF, 0x6D9, 0x40, Reset Password requirement); the October 11, 2022 hardening conditions and the March 14, 2023 GPO; Kerberos 5-minute time requirement. Removed as unconfirmed: 0x35, w32tm /stripchart, and the earlier descriptions of 0x40 and 0x6BF as SMB/135 problems.

Method: documentation only; no commands were run.
