---
id: computing-software.it-support-helpdesk.servicenow.servicenow-reports-and-sharing
name: servicenow-reports-and-sharing
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, servicenow-reports, report-designer, scheduled-reports, dashboards, report-sharing, sys-report]
level: practitioner
status: gated
description: "Build and share ServiceNow reports as an agent or lead: report designer types, group by and trend, dot-walked conditions, scheduling to email, dashboards and access."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-now-intelligence/page/use/reporting/concept/c_ReportingOverview.html"
  - "https://www.servicenow.com/docs/bundle/zurich-now-intelligence/page/use/reporting/task/t_ScheduleAReport.html"
  - "https://www.servicenow.com/docs/bundle/zurich-now-intelligence/page/use/reporting/task/t_ShareAReport.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# servicenow-reports-and-sharing

Most desk reporting is plain Reports (`sys_report`), not Performance Analytics. Reports
show *current* data; trends over time need either a date-grouped trend report or PA
snapshots.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Create (Reports > Create New, or right-click a list column header > Bar chart)
1. **Data**: name, source = table (incident, sc_req_item, task_sla, metric_instance) or a
   saved report source, or a database view for joins.
2. **Type**: List, Bar, Pie/Donut, Single score, Pivot table, Trend, Line, Heatmap,
   Time series.
3. **Configure**: group by (assignment group, category), stack by (priority), aggregation
   (count, sum, avg of a numeric field such as `business_duration`), trend per week.
4. **Conditions**: same builder as list filters, including dot-walking
   (`Caller > Location > Country is UK`) and relative dates (`Opened on Last 30 days`).
5. Save; Visible to: Me / Group / Everyone / Roles.

## Common desk reports
- Single score: open P1/P2 now (`active=true^priorityIN1,2`).
- Pivot: assignment group x priority of open incidents.
- Bar: resolved last month by close code (spot "Closed by caller" overuse).
- Task SLA list: `has_breached=true` for last month, grouped by SLA definition.
- Trend: opened per week, last 13 weeks.

## Sharing and scheduling
- Share: report > Sharing > users, groups; or add to a dashboard (Dashboards > add widget
  > Report). Viewers still need read access (ACLs) to the underlying records.
- Schedule: report > Schedule; recipients, run (daily/weekly/monthly), type (PDF, Excel,
  CSV), "Omit if no records" for exception reports. Stored in `sysauto_report`.
- Export for others: Excel/CSV respects the export row limit (`glide.export.limit`
  style properties, often 10,000 rows).

## Gotchas
- Report on `task` table mixes incidents, changes and requests; filter `sys_class_name`.
- Averages of duration fields include outliers; use median via PA or bucket the data.
- Scheduled reports run as the creator; if that user leaves (inactive), the schedule
  fails silently. Own shared schedules with a service account or group lead.
- Database views are slow on large tables; prefer dot-walking where possible.

## Verify
Report opens for an intended viewer (impersonate), counts match the equivalent list
filter, and the scheduled email arrives with data.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
