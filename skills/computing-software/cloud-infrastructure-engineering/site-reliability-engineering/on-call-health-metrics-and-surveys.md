---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.on-call-health-metrics-and-surveys
name: on-call-health-metrics-and-surveys
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, on-call, on-call-health-survey, pager-load, burnout, sustainability]
level: practitioner
status: docs-checked
description: "Measure on-call health with pager metrics (pages per shift, night pages, time to ack) and periodic surveys, set thresholds, and act on unsustainable load."
sources: ["https://sre.google/sre-book/being-on-call/", "https://sre.google/workbook/on-call/", "https://sre.google/sre-book/dealing-with-interrupts/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# On-call health metrics and surveys

**Goal:** detect unsustainable on-call before people burn out or quit.

## Quantitative metrics (per rotation, monthly)
| Metric | Target (SRE guidance) |
|---|---|
| Incidents per 12-hour shift | At most 2 (SRE Book: time to handle each, including postmortem, ~6 hours) |
| Pages outside working hours | As low as possible; track separately |
| Time to acknowledge (p50/p90) | Within policy |
| Pages with no action needed (noise) | Near zero; each is an alerting bug |
| Repeat pages (same alert) | Trend to zero |
| Time spent on-call on interrupts vs project work | Toil under 50% overall |
| Number of people in rotation | 8 for single-site, 6 per site for dual-site (SRE Book) |

Sources: paging tool exports (PagerDuty/Opsgenie/Grafana OnCall analytics), ticket system.

## Survey (after each shift or quarterly)
Short, consistent questions (1-5 scale + comments):
1. How much did on-call disrupt your sleep / personal time?
2. Were pages actionable?
3. Did you have the runbooks, access and knowledge to respond?
4. Did you feel supported (secondary, escalation)?
5. How sustainable is the current rotation for you?
Plus free text: worst alert of the shift.

## Act on it
- Thresholds trigger actions: pages per shift over 2 for a quarter -> alert review and reliability work prioritised (pager load caps); rotation size under minimum -> hire/merge rotations or hand back the service.
- Review in the monthly ops meeting with management present.
- Share trend charts openly with the team.

## Verify
- [ ] Monthly on-call health report with metrics and survey trends exists, and each threshold breach has an action item.

## Checked
2026-11-01. Confirmed in SRE Book Being On-Call: 2 incidents per 12-hour shift at about 6 hours each, 50% operations cap, minimum rotation of 8 single-site or 6 per site dual-site, every paging alert actionable, and the example overload goals (fewer than 5 daily tickets, fewer than 2 paging events per shift); corrective measures are expected when a limit is exceeded for a quarter, so the breach window was changed from two months. The survey questions are suggestions, not claims from the sources.
Method: documentation only; no commands were run.
