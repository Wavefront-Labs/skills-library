---
id: computing-software.systems-network-administration.active-directory.domain-kerberos-policy
name: domain-kerberos-policy
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, password-policy, kerberos-policy, kerberos, ticket-lifetime]
level: advanced
status: docs-checked
description: "Review and tune the Default Domain Policy Kerberos settings: TGT and service ticket lifetimes, renewal, clock skew and user logon restriction enforcement."
sources:
  - https://learn.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/kerberos-policy
  - https://learn.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/maximum-lifetime-for-user-ticket
  - https://learn.microsoft.com/en-us/windows-server/security/credentials-protection-and-management/protected-users-security-group
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Domain Kerberos policy

Kerberos policy lives in the **Default Domain Policy** (Computer Configuration > Windows Settings > Security Settings > Account Policies > Kerberos Policy). Microsoft notes that in most environments these settings should not need to be changed.

## Settings and defaults
| Setting | Default | Notes |
|---|---|---|
| Enforce user logon restrictions | Enabled | KDC validates every service ticket request against the user's logon rights; Microsoft recommends Enabled |
| Maximum lifetime for service ticket | 600 min | 10 minutes or more; 0 means tickets never expire |
| Maximum lifetime for user ticket (TGT) | 10 h | 0 means TGTs never expire |
| Maximum lifetime for user ticket renewal | 7 days | |
| Maximum tolerance for computer clock synchronization | 5 min | Microsoft advises 5 minutes |

## Security trade-offs
- Users whose accounts were disabled might keep accessing services with service tickets issued before the account was disabled; shorter lifetimes shrink that window but increase authorization overhead.
- Authentication policies can set a shorter, non-renewable TGT lifetime (in seconds) for specific accounts instead of changing the domain policy.
- Protected Users members have TGT lifetime and renewal limited to 240 minutes.

## Inspect
```powershell
Get-GPOReport -Name 'Default Domain Policy' -ReportType Html -Path <REPORT_PATH>
```
On a client, `klist` shows the Start, End and Renew times of cached tickets.

## Verify
- [ ] Values documented; changes made only in the Default Domain Policy.
- [ ] `klist tgt` on a client shows the expected End and Renew Until times.

## Checked
Checked 2026-10-27 against Microsoft Learn (Kerberos Policy and its five setting pages; Protected Users group; authentication policies overview; Get-GPOReport reference, Windows Server 2025).
- Confirmed: all five defaults (enforce restrictions Enabled, service ticket 600 minutes, user ticket 10 hours, renewal 7 days, clock tolerance 5 minutes); policy location; 0 means no expiry for ticket lifetimes; Protected Users 240-minute limits; authentication policy TGT lifetime is in seconds and non-renewable; Get-GPOReport -ReportType accepts Xml and Html.
- Removed: the GPO precedence and OU-level claims and the XML key names, which no source confirmed.

Method: documentation only; no commands were run.
