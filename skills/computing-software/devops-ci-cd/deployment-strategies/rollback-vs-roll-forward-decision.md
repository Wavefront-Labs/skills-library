---
id: computing-software.devops-ci-cd.deployment-strategies.rollback-vs-roll-forward-decision
name: rollback-vs-roll-forward-decision
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, rollback-decision, rollback, roll-forward]
level: practitioner
status: docs-checked
description: "Decide quickly whether to roll back or roll forward during a bad release: decision criteria, data and schema constraints, time-to-fix estimates and who decides."
sources: ["https://sre.google/sre-book/emergency-response/", "https://dora.dev/capabilities/continuous-delivery/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rollback vs roll-forward decision

Default: **roll back first, debug later**, unless rolling back is unsafe or slower than the fix.

## Decision checklist (answer in minutes)
1. Is customer impact ongoing? If yes, restore service first.
2. Can the previous version run against the current data/schema? (Expand/contract followed? Any
   irreversible migration, new message formats, data written in new shape?)
3. Is rollback fast and rehearsed (one command / one revert PR / flag off)?
4. Is the fix known, small, and can it go through the normal pipeline faster than rollback?
5. Did the release include changes others depend on already (API consumers, mobile clients)?

| Situation | Choose |
|---|---|
| Impact, rollback safe | roll back |
| Flagged feature misbehaving | flag off (fastest rollback) |
| Irreversible migration, old code incompatible | roll forward with fix |
| Security fix in the release | roll forward (rolling back reopens the hole) |
| Unknown cause, fix not obvious | roll back |

## Rules
- Roll-forward still goes through the pipeline (tests, review), possibly with an expedited path;
  "hotfix in production by hand" creates drift.
- Name an incident commander who makes the call; time-box debugging before deciding.
- Record the decision and timings in the incident timeline; measure time to restore.

## Verify
- [ ] Runbook contains the checklist and the exact rollback command per service.

## Checked

2026-10-28. Nothing in this skill is checkable against vendor documentation; it is process advice. Removed: the 15-minute time-box figure and the DORA attribution.

Method: documentation only; no commands were run.
