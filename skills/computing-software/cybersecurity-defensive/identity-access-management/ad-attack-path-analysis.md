---
id: computing-software.cybersecurity-defensive.identity-access-management.ad-attack-path-analysis
name: ad-attack-path-analysis
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [active-directory-security, ad-attack-paths, bloodhound, sharphound, pingcastle, purple-knight, tier-0, attack-path-management, acl-abuse]
level: advanced
status: draft
description: "Use BloodHound, PingCastle and similar tools defensively to find and remove Active Directory attack paths to Tier 0 before attackers use them."
sources: ["BloodHound Community Edition documentation (SpecterOps)", "PingCastle documentation", "Microsoft Learn - Securing privileged access (enterprise access model)", "ANSSI Active Directory security checkpoints"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AD attack path analysis for defenders

**Goal:** know every path by which a normal user or computer could become Domain Admin, and
cut the paths, prioritising those that affect the most principals.

## Collect and assess (authorised, coordinated with the AD team)
- **PingCastle** health check: `PingCastle.exe --healthcheck --server corp.example.com` gives a
  risk score and prioritised findings (stale objects, privileged accounts, trusts, anomalies).
- **Purple Knight** (Semperis) or Microsoft Defender for Identity posture assessments as alternatives.
- **BloodHound CE**: collect with SharpHound (`SharpHound.exe -c All,GPOLocalGroup`) or
  the Azure collector AzureHound; import into BloodHound and query.

## Typical paths to fix
| Edge / finding | Fix |
|---|---|
| Users with GenericAll/WriteDacl/WriteOwner on privileged groups or DCs | Remove ACEs; delegate via dedicated groups |
| Tier 0 admins logging on to workstations (HasSession) | Enforce tiering, logon restrictions, PAWs |
| Local admin reuse across machines (AdminTo) | Windows LAPS |
| Kerberoastable accounts with admin rights | gMSA or long random passwords, remove privileges, AES-only |
| Unconstrained delegation on non-DC computers | Remove or switch to constrained/resource-based delegation |
| AD CS template misconfigurations (ESC1-ESC8) | See AD CS hardening |
| GPO edit rights for non-admins on GPOs linked to Tier 0 | Restrict GPO permissions |
| DCSync rights (Replicating Directory Changes All) outside DCs and tools | Remove |

## Prioritise
BloodHound attack path management: fix "choke points" (edges many paths pass through) first;
measure the % of users with a path to Tier 0 and drive it down.

## Gotchas
- SharpHound collection looks like attacker recon; tell the SOC and run from an approved host.
- Collection data is a map of how to compromise you: store it like a secret, delete when done.
- Fixes to ACLs on AdminSDHolder-protected objects get overwritten by SDProp unless fixed on AdminSDHolder.

## Verify
- [ ] Re-collect after remediation: number of principals with a path to Domain Admins reduced and tracked.
- [ ] PingCastle score trend improving quarter on quarter.
