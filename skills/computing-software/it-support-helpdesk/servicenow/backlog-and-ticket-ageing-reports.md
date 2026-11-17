---
id: computing-software.it-support-helpdesk.servicenow.backlog-and-ticket-ageing-reports
name: backlog-and-ticket-ageing-reports
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, backlog-report, ticket-ageing, aged-backlog, opened-vs-closed, metrics, performance-analytics]
level: practitioner
status: draft
description: "Build backlog and ageing reports in ServiceNow: open backlog by age bucket, opened vs closed trend, per-group ageing, on-hold exclusions, and driving burn-down."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-now-intelligence/page/use/reporting/concept/c_ReportingOverview.html"
  - "https://www.servicenow.com/docs/bundle/zurich-now-intelligence/page/use/performance-analytics/concept/c_PerformanceAnalytics.html"
  - "https://www.thinkhdi.com/library/supportworld/2017/metric-of-month-backlog"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# backlog-and-ticket-ageing-reports

Backlog size alone tells you nothing. Backlog *age* and the opened-vs-closed trend tell
you whether a queue is healthy, slowly drowning or hiding work.

## Core views
1. **Open backlog by age bucket** (bar, stacked by priority): 0-2 days, 3-5, 6-10, 11-30,
   30+. Base on `opened_at` with relative conditions, or a calculated "age" field.
   Filter: `active=true^state!=6` (exclude Resolved awaiting closure).
2. **Opened vs closed per week** (two trend lines, last 13 weeks): closed below opened for
   3+ weeks means the backlog will grow regardless of effort.
3. **Ageing by assignment group** (pivot: group x bucket): spots the queue that hides old
   tickets.
4. **Oldest 20 tickets** list with assigned to, state, last update: the weekly review list.
5. **On-hold share**: tickets On Hold / total open, and on-hold age. A healthy-looking
   backlog with 40% on hold is not healthy.

## Performance Analytics
- Indicators: "Number of open incidents" (daily snapshot), breakdowns by age bucket,
  group, priority. Snapshots let you see last month's backlog shape, which plain reports
  can't (they show *current* state only).
- Add a target/threshold per group (e.g. no P3 older than 10 business days).

## Working the backlog
- Weekly 30-minute review per group: oldest 20, each gets a next action and owner or is
  closed with the user's agreement.
- Separate "waiting on others" (vendor, change, problem) from "waiting on us".
- Bulk-closing old tickets without contacting users wrecks CSAT and hides demand; send a
  "still needed?" comment and auto-resolve after 5 days if no reply.
- Requests vs incidents: report separately; request backlogs often reflect procurement
  lead times, not desk performance.

## Gotchas
- Age from `opened_at` restarts nothing on reassignment; group-level age needs the
  assignment time (`metric_instance` for assignment_group or the reassignment metric).
- Reports filtered on `state` values differ between incident (numeric) and other tables;
  check the choice list per table.

## Verify
The dashboard shows the bucket chart, opened/closed trend and oldest list per group, and
the weekly review reduces the 30+ bucket over a month.
