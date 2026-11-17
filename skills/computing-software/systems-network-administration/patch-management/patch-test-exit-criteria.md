---
id: computing-software.systems-network-administration.patch-management.patch-test-exit-criteria
name: patch-test-exit-criteria
category: computing-software
field: systems-network-administration
product: patch-management
tags: [test-exit-criteria, patch-testing, sign-off, go-no-go, patch-management]
level: practitioner
status: draft
description: "Define measurable patch test exit criteria and run the go/no-go: install success, health checks, app sign-offs, open defects, waivers and who can sign."
sources:
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Patch test exit criteria and sign-off

Without written exit criteria, testing ends when someone gets bored. Write them once in the patch policy; reuse every cycle.

## Example criteria for promoting from test to pilot / pilot to broad
| Criterion | Threshold |
|---|---|
| Install success on test ring | >= 98% of targeted devices, all failures explained |
| Post-reboot health | 100% of tier-1 servers pass automated checks (services, ports, synthetic transactions) |
| App owner sign-off | All tier-1 apps pass; tier-2 no open sev-1/2 |
| Open defects | No sev-1; sev-2 only with approved workaround |
| Telemetry | Crash/BSOD rate not above baseline + 10% over 48 h |
| Vendor known issues | Reviewed; none affecting our configs, or mitigated |
| Rollback | Tested on at least one system per OS family |
| Soak time | Minimum 72 h in ring (shortened for emergency track) |

## Go/no-go meeting (15 minutes)
1. Patch manager presents the scorecard against each criterion.
2. Each failing item: waive (with approver and reason), fix, or block.
3. Decision recorded in the change record with timestamp and approvers.

## Who signs
- Patch manager: technical criteria.
- App owners: their apps.
- Change authority: overall go for production rings.
- Security: can override soak time for exploited CVEs (documented).

## Gotchas
- Criteria that are never measurable ("users happy") get ignored; tie each to a report or query.
- Do not lower thresholds silently mid-cycle; waivers must be visible.
- Emergency track needs its own lighter criteria written in advance.

## Verify
Every promotion in the last quarter has a scorecard and sign-off attached; waivers are counted in the monthly report.
