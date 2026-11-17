---
id: computing-software.it-support-helpdesk.user-support-communication.ticket-quality-audits
name: ticket-quality-audits
category: computing-software
field: it-support-helpdesk
product: user-support-communication
tags: [it-support-helpdesk, user-support-communication, ticket-documentation, ticket-quality-audit, qa-scorecard, calibration, coaching, sampling, quality-assurance]
level: practitioner
status: draft
description: "Run ticket quality audits that improve work: a weighted scorecard, sampling per agent, calibration sessions between reviewers, coaching from findings, and trend reporting."
sources:
  - "https://www.thinkhdi.com/"
  - "https://www.comptia.org/certifications/a"
  - "https://www.axelos.com/certifications/itil-service-management"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ticket-quality-audits

Goal: consistent ticket quality across the team, measured fairly and used
for coaching rather than punishment.

## Scorecard (example, 100 points)
| Area | Checks | Weight |
|---|---|---|
| Logging | short description searchable, CI/category correct, caller/contact info | 15 |
| Description | expected vs actual, error text, scope, impact | 15 |
| Prioritisation | impact × urgency correct | 10 |
| Troubleshooting notes | steps and results recorded, logical | 15 |
| Knowledge | article searched/linked or created | 10 |
| Communication | customer updates timely, clear, professional tone | 15 |
| Resolution | cause/fix/verification, correct code, user confirmation | 15 |
| Compliance (fail item) | no passwords/PII, identity verification recorded | auto-fail |
Keep it to one page; each item yes/no/NA with a short comment.

## Sampling
- 4–8 tickets per agent per month, random across channels and priorities,
  plus all tickets with complaints or reopenings.
- Reviewers: team leads and senior agents (rotate).

## Calibration
Monthly, reviewers score the same 3 tickets independently, compare, and
agree interpretations. Without calibration, scores reflect the reviewer,
not the agent.

## Coaching
Share results 1:1 within a week: one strength, one or two specific
improvements with the actual ticket as example. Track themes across the
team → training or KB updates (if everyone misses the same item, it's a
process/tooling issue).

## Reporting
Team average by area over time; agent trends privately. Correlate with
reopen rate and CSAT to validate the scorecard.

## Gotchas
- Auditing only resolved tickets misses neglected open ones — include some
  open/aged.
- Too many criteria make audits slow and scores meaningless.

## Verify
Calibration variance between reviewers under ~5 points; team scores and
reopen rate improve quarter over quarter.
