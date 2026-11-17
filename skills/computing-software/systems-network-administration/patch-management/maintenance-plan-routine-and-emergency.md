---
id: computing-software.systems-network-administration.patch-management.maintenance-plan-routine-and-emergency
name: maintenance-plan-routine-and-emergency
category: computing-software
field: systems-network-administration
product: patch-management
tags: [maintenance-plan, maintenance-groups, asset-groups, routine-maintenance, emergency-maintenance, nist-sp-800-40, patch-management]
level: practitioner
status: draft
description: "Write NIST SP 800-40r4 style maintenance plans: asset and maintenance groups, routine vs emergency plans per group, timelines, owners, and what triggers each plan."
sources:
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Routine and emergency maintenance plans

**Goal:** for every group of assets, a written answer to "how and when do we patch this,
normally and in an emergency", agreed before the emergency happens.

## Groups (NIST SP 800-40r4)
- **Asset groups:** assets sharing characteristics that affect patching (platform,
  environment, criticality, who manages them, connectivity). Examples: domain
  controllers, internet-facing web, internal app servers, end-user laptops, OT/medical
  devices, network devices.
- **Maintenance groups:** the subsets that are actually patched together (a ring, a
  cluster half, a site).

## Plan contents (per asset group)
| Section | Content |
|---|---|
| Scope | Assets, owners, software types covered (OS, apps, firmware) |
| Routine plan | Cadence (e.g. monthly after Patch Tuesday), rings and timing (pilot +2 days, broad +7, critical servers +14), maintenance windows, approvals (standard change) |
| Emergency plan | Triggers (CISA KEV entry, vendor emergency release, active exploitation in sector), target time (e.g. 48-72 h for internet-facing), who can declare, approval path (emergency change), reduced testing |
| Testing | What is tested and by whom before each ring |
| Rollback | Method per platform and the decision owner |
| Risk responses | When mitigation, isolation or acceptance is used instead of patching |
| Exceptions | How assets that cannot be patched are handled |
| Metrics | Time to patch, coverage, failures |

## Writing tips
- Express timelines from the vendor release date, so they are measurable.
- Name roles, not people, and include out-of-hours contacts.
- Keep emergency plans short (a page): they are read under pressure.
- Assets with no plan are themselves a finding; default them into the strictest group.

## Review
Revisit plans after every emergency, after major platform changes, and at least yearly.

## Verify
Every asset in the inventory maps to exactly one asset group with a current plan; last
emergency's actual timeline is compared to the plan target in the post-incident review.
