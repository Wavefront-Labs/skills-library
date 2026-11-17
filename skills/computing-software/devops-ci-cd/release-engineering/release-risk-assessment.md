---
id: computing-software.devops-ci-cd.release-engineering.release-risk-assessment
name: release-risk-assessment
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, release-risk-assessment, release-readiness, change-management]
level: practitioner
status: draft
description: "Assess release risk with a lightweight scoring model (blast radius, reversibility, change size, novelty) that sets rollout strategy and approvals instead of blanket CAB review."
sources: ["https://sre.google/workbook/canarying-releases/", "https://dora.dev/capabilities/streamlining-change-approval/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Release risk assessment

Risk should decide **how** a change ships (rollout speed, monitoring, approvals), not just whether.

## Scoring dimensions (score 1-3 each)
| Dimension | Low (1) | High (3) |
|---|---|---|
| Blast radius | one internal service | all customers, payments, auth |
| Reversibility | flag off / instant rollback | irreversible migration, external side effects |
| Change size | < 200 lines, one component | many services, infra + app together |
| Novelty | routine change type | new technology, first-of-kind |
| Test confidence | covered by automated tests | manual-only verification |
| Timing | normal hours | near peak events, during freezes |

## Mapping score to process
| Total | Process |
|---|---|
| 6-9 | standard pipeline, automatic canary, peer review only |
| 10-13 | slower canary/ring rollout, explicit owner on watch, rollback rehearsed |
| 14-18 | release plan, go/no-go with service owners, staged by region, comms prepared |

## Automate the inputs
- Size and touched components from the diff; migration files present; infra paths changed.
- Labels from PR templates ("irreversible", "customer-facing").
- Post a risk summary on the PR or deployment and require the extra approval only for high scores.

## Learn
Compare scores with outcomes (failed changes) quarterly and adjust weights.

## Verify
- [ ] Every production change carries a risk score; high-risk changes show the required plan and approver.
