---
id: computing-software.software-engineering.code-review.review-metrics-and-slas
name: review-metrics-and-slas
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, review-process, review-metrics, review-sla, dora-metrics, cycle-time, pr-analytics]
level: practitioner
status: draft
description: "Measure code review health without gaming: time to first review, review cycle time, PR size, rework, healthy SLAs, and using the metrics to fix bottlenecks rather than rank people."
sources:
  - https://google.github.io/eng-practices/review/reviewer/speed.html
  - https://dora.dev/guides/dora-metrics-four-keys/
  - https://www.microsoft.com/en-us/research/publication/expectations-outcomes-and-challenges-of-modern-code-review/
  - https://linearb.io/blog/cycle-time
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Review metrics and healthy SLAs

## Why measure
Review wait time is often the largest part of lead time for changes (a DORA key metric). Slow reviews push authors to batch changes into larger PRs, which are reviewed worse and slower - a vicious cycle.

## Metrics that matter
| Metric | Definition | Healthy range (typical) |
|---|---|---|
| Time to first review | PR ready-for-review -> first reviewer comment/approval | < 4 working hours; Google guidance: respond within one business day at most |
| Review cycle time | ready-for-review -> approved | < 1 working day for normal PRs |
| PR size | lines changed (excluding generated/lock files) | median < 200-400 lines |
| Review rounds / rework | number of review iterations before approval | 1-2 |
| Pickup distribution | share of reviews per person | no one person doing most reviews |
| Merge-to-deploy | approval -> production | minutes to hours with CD |
| Post-merge defects | bugs/incidents traced to merged PRs | trend down |

## Getting the data
- GitHub: GraphQL API (`pullRequest { createdAt reviews { submittedAt } timelineItems(itemTypes: READY_FOR_REVIEW_EVENT) mergedAt additions deletions }`), GitHub Insights, or tools like LinearB, Swarmia, Sleuth, Faros, DX, Apache DevLake (open source).
- GitLab Value Stream Analytics; Gerrit has review age dashboards.
- Count from "ready for review", not PR creation (drafts are not waiting on reviewers). Exclude bots and reverts.
- Report medians and p90, not averages (a few stale PRs distort means).

## SLAs and norms
- Team agreement: first response within N working hours (for example 4); reviewers do reviews at natural breaks (after a task, before lunch) rather than interrupting deep work.
- Small PRs get priority; very large PRs can be sent back with a request to split.
- Rotation or a "review buddy" for unclear ownership; CODEOWNERS for routing.
- Stale PR nudges (Slack reminders via GitHub scheduled reminders, Pull Panda style bots) after the SLA.

## Avoid gaming and harm (Goodhart's law)
- Never use review counts or comment counts for individual performance ranking; it produces rubber-stamp approvals and nit storms.
- Pair speed metrics with quality signals (escaped defects, revert rate).
- Use metrics in retrospectives to find system bottlenecks: one overloaded reviewer, time zones, oversized PRs, slow CI.

## Verify
- [ ] Dashboard shows median and p90 time-to-first-review and PR size per team, updated weekly.
- [ ] Team SLA written in the contributing guide and reviewed in retros quarterly.
