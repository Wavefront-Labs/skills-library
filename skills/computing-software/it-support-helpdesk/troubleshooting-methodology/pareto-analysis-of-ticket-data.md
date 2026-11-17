---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.pareto-analysis-of-ticket-data
name: pareto-analysis-of-ticket-data
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, pareto-analysis, ticket-analytics, problem-management, continual-improvement, excel]
level: practitioner
status: draft
description: "Run a Pareto analysis on ticket data to find the few causes behind most volume: export, clean categories, rank with cumulative percent, chart it, and act on the top items."
sources:
  - "https://asq.org/quality-resources/pareto"
  - "https://support.microsoft.com/en-us/office/create-a-pareto-chart-a1512496-6dba-4743-9ab1-df5012972856"
  - "https://www.axelos.com/certifications/itil-service-management/itil-4-practice-manager"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# pareto-analysis-of-ticket-data

## 1. Get the data
Export 3-6 months of tickets from the ITSM tool with: category/subcategory, configuration
item or app, resolution code, assignment group, caller department, opened/closed dates.

## 2. Clean before counting
- Merge duplicate categories ("Outlook", "Email - Outlook", "MS Outlook").
- Use resolution code or a quick manual sample when categories are unreliable ("Other"
  over 20% means fix the category scheme first).
- Exclude pure requests if you are hunting faults, or analyse them separately.

## 3. Rank
| Category | Tickets | % | Cumulative % |
|---|---|---|---|
| Password reset / lockout | 820 | 27% | 27% |
| VPN connect failures | 510 | 17% | 44% |
| Printer - floor 3 | 390 | 13% | 57% |
| Teams audio | 300 | 10% | 67% |
| ... | | | |

Sort descending; cumulative % shows where you cross roughly 80%. Excel: select the
category and count columns > Insert > Statistic chart > Pareto.

## 4. Look at more than count
Weight by effort (handle time x count) or business impact; a rare outage can outrank a
frequent nuisance. Re-run the Pareto within the top category (by site, app version, model)
to find the specific cause.

## 5. Act
- Top items become problem records, self-service fixes (password reset portal), knowledge
  articles, or automation.
- Set a target and re-measure next quarter on the same definitions.

## Gotchas
- Pareto shows frequency, not cause. "VPN" at the top still needs root cause analysis.
- Seasonal spikes (onboarding month) distort small samples.

## Verify
The chart and action list are shared with the team, each top item has an owner and
problem/KB/automation reference, and the next period's Pareto shows the change.
