---
id: computing-software.systems-network-administration.patch-management.asset-criticality-patch-tiers
name: asset-criticality-patch-tiers
category: computing-software
field: systems-network-administration
product: patch-management
tags: [asset-criticality-tier, patch-tiers, asset-groups, maintenance-groups, remediation-sla, patch-management]
level: practitioner
status: draft
description: "Tier assets by criticality and exposure for patching, map tiers to SLAs, rings and windows, and implement tiers as groups in WSUS, ConfigMgr, Intune and Ansible."
sources:
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
  - https://www.cisa.gov/known-exploited-vulnerabilities-catalog
  - https://learn.microsoft.com/en-us/security/privileged-access-workstations/privileged-access-access-model
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tiering assets by criticality for patching

**Goal:** patch the most dangerous systems fastest, and avoid a one-size schedule that patches everything late.

## Define tiers (example)
| Tier | Members | Target SLA (critical/KEV) |
|---|---|---|
| T0 | Identity and control planes: domain controllers, PKI, hypervisor management, backup servers, privileged access | 48-72 h |
| T1 | Internet-facing: VPN, firewalls, web front ends, email gateways | 72 h |
| T2 | Business-critical internal apps and databases | 7-14 days |
| T3 | General servers and user endpoints | 14-30 days |
Combine **impact** (business criticality, data sensitivity) with **exposure** (internet, untrusted networks). An internet-facing low-value host still sits high.

## Map tiers to execution
- Rings within each tier: pilot (a few representative hosts) then broad.
- Maintenance windows per tier; T0 often patched member-by-member for redundancy (one DC at a time).
- Change type: T0/T1 emergency patches via emergency change; routine via standard change.

## Implement as groups
- WSUS: computer groups via GPO client-side targeting (`TargetGroup`).
- ConfigMgr: collections by tier attribute; deployments with different deadlines.
- Intune: Entra groups mapped to update rings.
- Ansible: inventory groups `tier0`, `tier1` with group_vars for windows and serial.
- Cloud: tags (`PatchTier=T1`) used by Azure Update Manager or SSM patch groups.

## Gotchas
- Tier assignment must live in the CMDB (or tags) and be audited; ad-hoc lists drift.
- "Too critical to patch" is not a tier; it is a risk exception with compensating controls and an expiry.

## Verify
Every in-scope asset has exactly one tier, and SLA reporting is produced per tier.
