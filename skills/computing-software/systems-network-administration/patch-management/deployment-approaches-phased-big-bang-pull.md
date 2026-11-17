---
id: computing-software.systems-network-administration.patch-management.deployment-approaches-phased-big-bang-pull
name: deployment-approaches-phased-big-bang-pull
category: computing-software
field: systems-network-administration
product: patch-management
tags: [release-management, deployment-management, phased-deployment, big-bang-deployment, pull-deployment, continuous-deployment, itil-4, patch-management]
level: practitioner
status: draft
description: "Choose an ITIL 4 deployment approach for updates and releases (phased, big bang, pull, continuous), with selection criteria, gating between phases and how each maps to patching."
sources:
  - https://www.axelos.com/certifications/itil-service-management/itil-4-practice-manager
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deployment approaches: phased, big bang, pull, continuous

**Goal:** pick the deployment approach deliberately for each release or patch type, so
risk and speed are traded on purpose.

## The four approaches (ITIL 4 Deployment Management)
| Approach | What it is | Fits | Risk |
|---|---|---|---|
| **Phased** | Deploy to parts of the estate in sequence (rings, sites, user groups) | Monthly OS patching, app upgrades | Low; slower |
| **Big bang** | Deploy everywhere at once | Tightly coupled changes (schema + all clients), emergency fixes where exposure is worse than breakage | High: one failure hits all |
| **Pull** | Users/systems fetch when ready (self-service portal, store, auto-update on next check-in) | Optional apps, remote endpoints | Uneven coverage |
| **Continuous** | Small automated changes flow through pipelines constantly | Container images, cloud services | Low per change; needs automation and monitoring |

## Phased deployment for patching
1. Rings: IT/pilot (1-5%), early adopters (10-20%), broad, critical systems last (or
   first for internet-facing emergency cases).
2. **Gate** between phases with measurable criteria: install success rate ≥ 98%, no P1/P2
   incidents attributed, health checks green, soak time (e.g. 48 h).
3. Halt and roll back on gate failure; record the decision.

## Choosing
Ask: Can parts of the estate run different versions safely? How bad is a failure vs the
exposure? Can we detect failure quickly? Is rollback possible? If versions can't coexist,
big bang with strong rehearsal; if exposure is critical (KEV), compress phases rather than
skip them where possible (pilot hours, not days).

## Release records
For each release: approach chosen and why, phases with dates, gates and outcomes,
rollback plan, communications. This becomes the audit trail and the input to the PIR.

## Gotchas
- "Phased" without gates is just slow big bang.
- Pull approaches need a deadline and enforcement or coverage plateaus.

## Verify
Every release/patch cycle record names its approach and shows gate results per phase;
post-implementation reviews compare actual failure rates per ring.
