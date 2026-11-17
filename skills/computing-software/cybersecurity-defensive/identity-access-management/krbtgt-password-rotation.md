---
id: computing-software.cybersecurity-defensive.identity-access-management.krbtgt-password-rotation
name: krbtgt-password-rotation
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [active-directory-security, krbtgt-rotation, krbtgt, golden-ticket, kerberos, ad-recovery, new-krbtgtkeys]
level: advanced
status: gated
description: "Rotate the krbtgt account password safely (twice, with replication checks) for routine hygiene and after domain compromise to invalidate golden tickets."
sources: ["https://attack.mitre.org/techniques/T1558/", "https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/security-policy-settings/maximum-lifetime-for-user-ticket", "https://github.com/microsoftarchive/New-KrbtgtKeys.ps1"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# krbtgt password rotation

**Goal:** invalidate forged Kerberos tickets (golden tickets) and limit the lifetime of a stolen
krbtgt hash, without breaking authentication across the domain.

## Why twice
The krbtgt account keeps the current and the previous password; tickets signed with either are
accepted (gated: unconfirmed, source is paywalled or blocked). One reset leaves the stolen (now previous) key valid. A second reset removes it.

## Procedure
1. Check AD replication health first and
   resolve any failures. Resetting with broken replication causes Kerberos failures.
2. Use Microsoft's **New-KrbtgtKeys.ps1** script (gated: unconfirmed, source is paywalled or blocked): run its informational and simulation modes first, then
   the real reset, which forces replication to all writable DCs.
   For RODCs, each has its own krbtgt account; reset those separately.
3. Wait at least the maximum ticket lifetime (default 10 hours for TGTs, plus clock skew) and
   confirm replication has completed before the second reset.
4. Second reset (mode 4 again).
5. Monitor for Kerberos errors (for example failed 4769 events) and application issues.

## When
- **After domain compromise**: as part of eradication, after attacker access is removed (otherwise they take the new hash too). In a confirmed DA compromise, the two resets may be done closer together accepting disruption; follow your IR lead.
- **Routine**: every 180 days is a common practice; also when admins with DC access leave.

## Gotchas
- A plain password reset works but loses the safety checks the script performs.
- Long-running services with old tickets may need restart after the second reset.
- Golden tickets are also invalidated only if the attacker cannot get the new hash: DCSync rights and DC access must be cleaned first.
- Trusts use separate inter-realm keys; rotate trust passwords if trusts were in scope.

## Verify
- [ ] `Get-ADUser krbtgt -Properties PasswordLastSet` shows both resets with the planned interval.
- [ ] No spike in Kerberos failures after each reset.

## Checked

2026-10-28. Confirmed against the MITRE ATT&CK T1558 page: reset the KRBTGT password twice to invalidate golden tickets, consider rotating every 180 days; and the Maximum lifetime for user ticket page: 10 hours default in the Default Domain Policy. Gated: the New-KrbtgtKeys.ps1 script name and modes (the GitHub archive README did not name them) and the explanation of current and previous password. Removed: repadmin commands, krbtgt_<number> RODC account name, KDC event 14 and 0x1F error codes, 24-hour routine wait, Set-ADAccountPassword.

Method: documentation only; no commands were run.
