---
id: computing-software.it-support-helpdesk.servicenow.mttr-and-resolution-time-distributions
name: mttr-and-resolution-time-distributions
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, metrics, kpi, mttr, resolution-time, percentiles, business-hours, performance-analytics]
level: practitioner
status: draft
description: "Report mean time to resolve correctly: business vs calendar time, pause states, median and 90th percentile instead of mean alone, and cutting by priority and assignment group."
sources:
  - "https://www.servicenow.com/docs/"
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://www.thinkhdi.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# mttr-and-resolution-time-distributions
Goal: resolution-time numbers that reflect user experience and point at
where tickets actually wait.

## Define it before you calculate
- Start: ticket opened (or acknowledged, but state which).
- Stop: resolved (not closed; closed adds the auto-close wait).
- Clock: business hours (support schedule) or calendar. Users feel
  calendar time; SLAs often use business time. Report both, labelled.
- Pauses: on-hold awaiting user/vendor. Show with and without pauses.

## Use distributions, not just the mean
A few 90-day tickets drag the mean far above what most users see.
Report:
- **Median** (typical user experience).
- **90th percentile** (the tail).
- Mean (for continuity with old reports).
Example: mean 3.1 days, median 4 hours, P90 6 days tells you most is fast
but a tail rots.

## ServiceNow sources
- `incident` fields: `opened_at`, `resolved_at`, `calendar_stc` (seconds to
  close), `business_stc` (business seconds to close).
- `metric_instance` for time in each state or assignment group (Incident
  metrics: Assigned to Duration, Assignment Group).
- Performance Analytics indicators for trend charts with breakdowns.
- Export and compute percentiles in a spreadsheet if PA lacks them:
  `=PERCENTILE.INC(range,0.9)`.

## Breakdowns that drive action
- By priority (P1 MTTR is a separate story).
- By assignment group: time per group from metrics shows where tickets
  wait.
- By number of reassignments (bounced tickets resolve slower).
- By channel and category.

## Gotchas
- Tickets resolved then reopened: count until final resolution or report
  reopen rate alongside.
- Mixing requests and incidents inflates MTTR (requests include
  procurement lead times). Report separately.
- Improving MTTR by resolving prematurely shows up as higher reopen rate.

## Verify
Monthly report states the clock definition and shows median, P90 and mean
per priority, with group time-in-state for the slowest category.
