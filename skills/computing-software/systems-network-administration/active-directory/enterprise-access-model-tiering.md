---
id: computing-software.systems-network-administration.active-directory.enterprise-access-model-tiering
name: enterprise-access-model-tiering
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, privileged-access, enterprise-access-model, tiering, control-plane, management-plane]
level: advanced
status: docs-checked
description: "Apply Microsoft's enterprise access model to AD: control, management and data/workload planes, mapping Tier 0 assets, and rules that stop credential exposure."
sources:
  - https://learn.microsoft.com/en-us/security/privileged-access-workstations/privileged-access-access-model
  - https://learn.microsoft.com/en-us/security/privileged-access-workstations/privileged-access-strategy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enterprise access model (tiering for AD)

The enterprise access model replaced the old Tier 0/1/2 model but keeps its core rule: a credential must never be
exposed on a system less trusted than what it controls.

## Planes
- **Control plane** (Tier 0 expanded): access control for the whole estate, centred on the enterprise identity
  systems (AD DS and Entra ID), including network access control where it is the only option.
- **Management plane**: enterprise-wide IT management functions (the old Tier 1, split).
- **Data/workload plane**: per-workload management, sometimes by business units (the old Tier 1, split).
- **User access** (B2B, B2C, public) and **app access** (API pathways): the old Tier 2, split.
- Privileged access pathways connect IT staff and developers to these planes and need the strongest protection.

## Map Tier 0 honestly
List every system and account that can take over a DC: anything with code execution on a DC (agents,
hypervisor admins, backup operators), GPO editors linked to the DC OU, owners and editors of AdminSDHolder, and
accounts with directory replication rights. If it can control Tier 0, it is Tier 0.

## Rules to implement
- Separate admin accounts per plane; control plane admins log on only to control plane systems from PAWs.
- Block downward logons: the *Deny log on* user rights (locally, through RDS, as batch, as service) and *Deny access to
  this computer from the network* for Tier 0 groups on lower-tier systems (by GPO), and authentication policy silos for
  Tier 0 accounts.
- No Tier 0 agent on lower tiers; no lower-tier agent on Tier 0.
- Just-in-time elevation (for example time-bound group membership) instead of standing membership.

## Verify
- [ ] Tier 0 asset list exists and is reviewed against your assessment tooling.
- [ ] Logon events (4624, the successful-logon event) show no Tier 0 account on a non-Tier 0 host.

## Checked
2026-10-27, against the Learn page "Enterprise access model" (updated 2026-05-07), "Privileged access strategy" pages and windowsserverdocs Appendix L and least-privilege pages. Confirmed: plane definitions and how Tier 0, Tier 1 and Tier 2 were expanded or split; enforce hierarchy and least privilege principles; the deny user rights; 4624 event name. Removed as unconfirmed: the named products listed per plane, PIM, DCSync and attack-path tool references.

Method: documentation only; no commands were run.
