---
id: computing-software.cybersecurity-defensive.security-operations.domain-compromise-recovery
name: domain-compromise-recovery
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [incident-response, domain-compromise-recovery, active-directory, krbtgt, credential-reset, tier-0, eviction, persistence-removal]
level: sme
status: draft
description: "Recover from full Active Directory compromise: rebuild vs clean, coordinated eviction, krbtgt and privileged resets, persistence sweeps (ACLs, GPOs, AD CS) and validation."
sources: ["https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/planning-for-compromise", "https://www.cisa.gov/news-events/cybersecurity-advisories/aa21-008a", "https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/ad-forest-recovery-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Domain compromise recovery

When an attacker had Domain Admin (or equivalent: DCSync rights, AD CS abuse, backup operator on
DCs), assume every credential in the domain and every object ACL may be backdoored.

## Decide: clean in place or rebuild
- **Clean in place**: feasible when scope is well understood, dwell time short, and logging good.
- **Forest recovery / new forest**: when persistence cannot be ruled out (long dwell, poor logs,
  AD CS compromise, attacker had control of backups). Much more disruptive, more certain.

## Prepare in secret
Attacker likely reads mail and admin chats: use out-of-band comms. Stage tooling and clean admin
workstations (new PAWs) before acting.

## Coordinated eviction (single window)
1. Block attacker infrastructure and remote access paths (VPN, RMM tools).
2. Reset **krbtgt twice** with replication between resets (allow at least the max ticket lifetime
   (10h default) between resets if outage risk matters; in an active compromise reset quickly and
   accept some ticket failures). Use Microsoft's New-KrbtgtKeys script.
3. Reset all Tier 0 accounts (DA, EA, Schema/Account/Backup operators, built-in Administrator),
   service accounts with privileged rights, AD connector accounts (Entra Connect), and
   DSRM passwords on every DC.
4. Rotate trust passwords; reset computer account passwords of DCs if suspected.
5. Disable or delete attacker-created accounts.

## Persistence sweep
- Privileged group membership, including nested groups and `primaryGroupID` tricks.
- **AdminSDHolder** ACL and protected objects' ACLs (adminCount=1).
- DCSync rights (Replicating Directory Changes All) on the domain head.
- GPOs: new or modified, scheduled tasks/scripts deployed by GPO, GPO link permissions.
- SID history on accounts; `msDS-AllowedToActOnBehalfOfOtherIdentity` (RBCD); unconstrained delegation.
- AD CS: new templates, enrolment agent rights, issued certificates for privileged accounts
  (certificates survive password resets; revoke them).
- DC-level: skeleton key/DSRM logon behaviour, DLLs in LSA (`Security Packages`), DNS admin plugins.
Tools: PingCastle, Purple Knight, BloodHound for ACL paths; compare against pre-incident baselines.

## After
Tier 0 isolation (PAWs, no Tier 0 logons on lower tiers), Protected Users, LAPS, monitoring for
DCSync, golden ticket indicators (TGS without TGT, abnormal lifetimes), and new privileged logons.

## Gotchas
- Resetting passwords without removing ACL/certificate persistence lets the attacker reset them back.
- Entra ID: hybrid compromise can extend to the cloud (sync account, federation trust, seamless SSO
  AZUREADSSOACC key); rotate those too.
- Backups may hold attacker modifications; restore points must predate initial access.

## Verify
Repeat PingCastle/BloodHound and compare with a clean baseline; no unexplained privileged paths,
and monitoring shows no use of old credentials or certificates for 30+ days.
