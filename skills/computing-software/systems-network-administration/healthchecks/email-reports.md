---
id: computing-software.systems-network-administration.healthchecks.email-reports
name: email-reports
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, weekly-report, monthly-report, downtime-statistics, report-opt-out]
level: intro
status: docs-checked
description: "What Healthchecks email reports contain, how often they arrive (daily, weekly, monthly), and how to opt out or change frequency."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/configuring_notifications.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/projects_teams.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Reports help you confirm every check is in its expected state.

Content: checks from all projects you own or belong to, grouped by project. For each check: current status, number of downtimes per month for the last two months, and total downtime duration per month for the last two months.

Frequency: set in Account Settings under Email Reports. The projects and teams docs list daily, weekly (Mondays), monthly (1st of the month) or off; the notifications docs describe monthly at the start of each month or weekly on Mondays.

Opt out: turn reports off in Account Settings, Email Reports, or click "Unsubscribe" in the report email footer.

The same settings page controls hourly or daily reminders while any check is down (see repeated-notifications).

Self-hosted: reports and reminders are sent by `sendreports`, which runs automatically in the official Docker images; elsewhere run it with `--loop`.

## Checked

2026-11-04. Confirmed against the Healthchecks Configuring Notifications and Projects and Teams pages and the README: report contents, the daily, weekly (Mondays) and monthly (1st) frequencies, opt-out in Account Settings or the Unsubscribe footer link, hourly or daily reminders, and sendreports with --loop. Nothing removed.

Method: documentation only; no commands were run.
