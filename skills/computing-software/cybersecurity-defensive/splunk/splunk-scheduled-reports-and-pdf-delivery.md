---
id: computing-software.cybersecurity-defensive.splunk.splunk-scheduled-reports-and-pdf-delivery
name: splunk-scheduled-reports-and-pdf-delivery
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, scheduled-reports, pdf-delivery, savedsearches-conf, report-acceleration, email-alerts, siem-dashboards]
level: practitioner
status: draft
description: "Build Splunk scheduled reports with PDF/CSV email delivery: cron schedules, time ranges, schedule windows, priority, PDF server settings and report acceleration."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/Report/Schedulereports", "https://docs.splunk.com/Documentation/Splunk/latest/Report/GeneratePDFsofyourreportsanddashboards", "https://docs.splunk.com/Documentation/Splunk/latest/Admin/Savedsearchesconf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Scheduled reports and PDF delivery

## Schedule
Report > Edit Schedule: cron, time range, schedule priority, schedule window. In
`savedsearches.conf`:
```
[Weekly - Privileged Group Changes]
search = `wineventlog_security` EventCode IN (4728,4732,4756) | table _time user member Group_Name src_user
cron_schedule = 0 7 * * 1
dispatch.earliest_time = -7d@d
dispatch.latest_time = @d
enableSched = 1
schedule_window = 60
action.email = 1
action.email.to = soc-leads@example.com
action.email.sendpdf = 1
action.email.sendcsv = 1
action.email.inline = 0
```
- Snap time ranges (`-7d@d` to `@d`) so consecutive reports neither overlap nor gap.
- `schedule_window` lets the scheduler defer within N minutes to smooth load; use for reports, never
  for time-critical alerts. `schedule_priority = higher` for important reports.
- Stagger cron minutes (`7 7 * * 1`, not `0 * * * *` for everything).

## PDF
- Dashboards: Export > Schedule PDF Delivery (Classic Simple XML). Dashboard Studio supports
  PDF/PNG export and scheduled export on recent versions; check your version.
- Server settings: Settings > Server settings > Email settings (mail host, TLS, sender), PDF
  report server: paper size, logo. Long tables truncate to `reportserver` limits; set
  `action.email.pdf.*` or summarise.
- Recipients see results with the owner's permissions; never schedule a report owned by an admin
  to a wide audience without checking what it exposes.

## Performance
Turn on **report acceleration** for reports with transforming commands over large ranges, or base
them on accelerated data models via `tstats`. Check skipped searches in the Monitoring Console
(Search > Scheduler Activity).

## Gotchas
- Email size limits silently drop large CSVs; use `action.email.maxresults` and link to results.
- Owner disabled or SAML-resolution failure = report stops running; use a service owner.

## Verify
Run once with "Send test", check PDF content, then confirm `index=_internal sourcetype=scheduler savedsearch_name="Weekly*" status=success`.
