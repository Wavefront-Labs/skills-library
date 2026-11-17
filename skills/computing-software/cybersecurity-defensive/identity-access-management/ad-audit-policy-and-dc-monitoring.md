---
id: computing-software.cybersecurity-defensive.identity-access-management.ad-audit-policy-and-dc-monitoring
name: ad-audit-policy-and-dc-monitoring
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [active-directory-security, ad-audit-policy, domain-controller-monitoring, advanced-audit-policy, directory-service-changes, defender-for-identity, dcsync-detection, privileged-group-changes]
level: advanced
status: gated
description: "Configure domain controller audit policy and monitor what matters: privileged group changes, DCSync, Kerberos anomalies, GPO edits and log clearing."
sources: ["https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/audit-policy-recommendations", "https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4662", "https://attack.mitre.org/techniques/T1558/003/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AD audit policy and domain controller monitoring

**Goal:** every change to identity infrastructure and every classic AD attack technique leaves
an event that someone sees.

## DC audit policy (Advanced Audit Policy via the Default Domain Controllers Policy GPO) (gated: unconfirmed, source is paywalled or blocked)
| Subcategory | Setting |
|---|---|
| Account Logon: Credential Validation, Kerberos Authentication Service, Kerberos Service Ticket Operations | Success, Failure |
| Account Management: User, Computer, Security Group Account Management | Success, Failure |
| DS Access: Directory Service Changes | Success (needs SACLs on objects) |
| DS Access: Directory Service Access | Success, Failure (for DCSync detection, SACL on domain root) |
| Logon/Logoff: Logon, Special Logon | Success, Failure |
| Policy Change: Audit Policy Change, Authentication Policy Change | Success |
| Privilege Use: Sensitive Privilege Use | Success, Failure |
| System: Security System Extension, Security State Change | Success |
Set "Force audit policy subcategory settings" so legacy categories do not override. Raise
Security log size and forward to the SIEM.

## Detections that matter
| Technique | Signal |
|---|---|
| Privileged group change | Group membership change events on Domain Admins, Enterprise Admins, Administrators, Schema Admins, DnsAdmins, Backup Operators |
| DCSync | 4662 for directory replication rights by a non-DC account |
| Kerberoasting | 4769 with RC4 encryption (0x17) for many SPNs from one account |
| Password spraying | 4771/4625 failures spread across many accounts from one source |
| AdminSDHolder / ACL change | 5136 on AdminSDHolder or domain root |
| GPO change | 5136 (and object-creation events) on groupPolicyContainer objects |
| Log cleared | 1102 |
| New DC / replication from unknown host (DCShadow) | Computer account changes adding replication SPNs; unexpected DC objects |

**Microsoft Defender for Identity** (sensor on DCs, AD FS, AD CS) detects many of these with
behavioural baselines; still forward raw events for investigation.

## Gotchas
- Directory Service Changes events need SACLs; without them 5136 does not fire.
- 4662 is high volume; filter at the forwarder to the replication GUIDs and sensitive objects.
- Every DC must be covered; one forgotten DC is where an attacker authenticates.

## Verify
- [ ] Test changes (add a test account to a monitored group, test GPO edit) produce alerts.
- [ ] All DCs forward Security logs; gap alert if a DC goes silent.

## Checked

2026-10-28. Confirmed against the event pages for 4662, 4771, 4769, 1102 and 5136 and the audit policy recommendations page (Sensitive Privilege Use subcategory): those events exist as described; MITRE T1558.003 confirms 4769 with RC4 etype 0x17. Gated: the subcategory settings table. Removed: log size figure, replication GUIDs, group-change event ids, DCShadow event ids.

Method: documentation only; no commands were run.
