---
id: computing-software.data-engineering.metabase.alerts
name: alerts
category: computing-software
field: data-engineering
product: metabase
tags: [alerts, goal-line, results-alert, quartz-cron, webhook, notifications]
level: practitioner
status: docs-checked
description: "Set up Metabase question alerts: results, goal line and progress bar types, schedules including Quartz cron, channels, who can edit them, and delivery gotchas."
sources:
  - https://www.metabase.com/docs/latest/questions/alerts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Alert types:
- Results alerts fire when a question returns any result.
- Goal line alerts fire when a time series in a line, bar or area chart crosses a goal line, above or below, on every crossing or only the first.
- Progress bar alerts fire when a single number reaches or drops below its goal.

Schedule: minutely, hourly, daily, weekly, monthly, or a custom Quartz cron schedule.

Channels: email, Slack or webhook. Only admins and users with settings access can use webhooks. An admin must configure at least one channel first.

Other options: a one-time alert sends once and is then deleted. "Send now" tests an alert, but nothing is sent if the question returns no results.

Permissions: users can edit only their own alerts. Admins can edit or delete any alert, change recipients and bulk-manage; admin deletions cannot be undone. Alerts are for questions only; dashboards use subscriptions.

Gotchas:
- Renaming a Slack channel stops delivery until you update the target.
- Removing a goal line converts a goal alert into a results alert.
- Deleting a question deletes its alerts.
- Alerts keep working if the creator is deactivated, but deactivated recipients stop receiving them.
- Alerts from embedded questions omit Metabase links, and custom visualizations fall back to the default chart.

## Checked
2026-11-03. Confirmed against the Metabase docs page Questions, Alerts: channel prerequisite and webhook restriction, three alert types, schedule options incl. Quartz cron, one-time alerts, Send now behaviour, edit and delete permissions, Slack rename, goal-line removal, question deletion, deactivated creator, embedded-question links, custom visualization fallback. Nothing removed.
Method: documentation only; no commands were run.
