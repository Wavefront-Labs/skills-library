---
id: computing-software.systems-network-administration.patch-management.patch-exception-metrics
name: patch-exception-metrics
category: computing-software
field: systems-network-administration
product: patch-management
tags: [exception-metrics, patch-exceptions, risk-acceptance, patch-metrics, patch-management]
level: practitioner
status: draft
description: "Track patch exception count and age: open exceptions by severity and owner, overdue reviews, renewals per exception, coverage of findings, and thresholds for escalation."
sources:
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
  - https://csrc.nist.gov/pubs/sp/800/55/v1/final
  - https://www.cisecurity.org/controls/continuous-vulnerability-management
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Patch exception metrics

Exceptions are normal; a growing pile of renewed exceptions is a hidden backlog. Measure them.

## Metrics
| Metric | Why |
|---|---|
| Open exceptions by severity (and KEV) | size of accepted risk |
| Findings covered by exceptions / total open findings | how much of the backlog is "accepted" |
| Age of exception (days since first approval, across renewals) | long-lived = systemic issue |
| Renewals per exception | 3+ renewals means the plan is not working |
| Exceptions past review/expiry date | governance failure |
| Exceptions per owner / business unit | where to push |
| New vs closed per month | trend |
| Exceptions without compensating controls evidence | quality |

## Data model
Each exception: ID, scope (asset list or query), findings (CVE/plugin), severity, owner, approver, approved date, expiry, renewal count, compensating controls, linked risk register entry. Store in the GRC/ticketing tool, not in the scanner's comment field alone.

## Report
- Monthly: table by BU with counts, oldest age, overdue reviews.
- Quarterly to risk committee: KEV/critical exceptions older than 90 days, each with plan date.

## Thresholds
- Overdue review > 0 -> escalate to owner's manager.
- Critical exception age > 180 days -> must become a risk register entry.
- Coverage > 20% of open findings -> program review.

## Gotchas
- Scanner "accepted" findings disappear from dashboards; include them in denominators.
- Exceptions scoped to "all servers" are unmeasurable; require explicit scope.

## Verify
Every scanner suppression and patch tool exclusion maps to an exception record; metrics reconcile with the GRC tool count.
