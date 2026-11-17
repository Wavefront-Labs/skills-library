---
id: computing-software.devops-ci-cd.deployment-strategies.rollback-drills
name: rollback-drills
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, rollback-drill, rollback, game-day]
level: practitioner
status: docs-checked
description: "Rehearse rollbacks regularly: scheduled drills in staging and production, measuring time-to-rollback, data compatibility checks and fixing the runbook gaps found."
sources: ["https://sre.google/workbook/managing-incidents/", "https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_testing_resiliency_game_days_resiliency.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rollback drills

A rollback that has never been executed will fail when needed: missing permissions, expired
artifacts, incompatible schema, unknown commands.

## Drill design
1. Pick a service and a recent release.
2. Announce (or not, for a mature team) and start a timer.
3. Execute the documented rollback exactly as written (tool rollback command, revert PR, flag off, alias shift).
4. Verify the previous version serves traffic and data written by the newer version is handled.
5. Roll forward again.
6. Record: time to decision, time to rollback complete, problems found.

## What drills typically uncover
- Previous artifact deleted by retention (registry cleanup, artifact expiry): keep last N releases.
- GitOps reverting a manual rollback within seconds.
- Migrations without compatible old code path.
- On-call engineer lacks permission or VPN access.
- Rollback command depends on a CI system that is down; have a break-glass path.

## Cadence
Staging monthly per critical service; production quarterly for top services, during business hours
with low-risk releases. Track time-to-rollback as an SLO.

## Verify
- [ ] Drill log with timings exists for each tier-1 service this quarter; issues found have tickets.

## Checked

2026-10-28. Nothing in this skill is checkable against vendor documentation; it is process advice. Removed: the tool command list and the 10-minute SLO example.

Method: documentation only; no commands were run.
