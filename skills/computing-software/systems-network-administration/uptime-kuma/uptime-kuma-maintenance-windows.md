---
id: computing-software.systems-network-administration.uptime-kuma.uptime-kuma-maintenance-windows
name: uptime-kuma-maintenance-windows
category: computing-software
field: systems-network-administration
product: uptime-kuma
tags: [maintenance, maintenance-window, cron-expression, recurring-maintenance, suppress-notifications, status-page-banner]
level: practitioner
status: docs-checked
description: "Schedule Uptime Kuma maintenance windows to pause notifications and show banners, with single, cron and recurring strategies."
sources: ["https://github.com/louislam/uptime-kuma/wiki/Maintenance"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Maintenance windows

Available since 1.19.0. Purpose: temporarily disable notifications during a window and show a maintenance message on status pages. Open maintenance management from the top-left menu and use Schedule Maintenance.

Fields:
- **Title** and **Description** (Markdown supported) appear at the top of the selected status pages.
- **Affected Monitors**: searchable list; they show in blue on the dashboard and status pages during the window.
- **Status Pages**: choose specific pages or All Status Pages.
- **Strategy**: Active/Inactive Manually, Single Maintenance Window, Cron Expression, Recurring - Interval, Recurring - Day of Week, Recurring - Day of Month.
- **Timezone**: pick one or `Same as Server Timezone`.
- **Start/End Date/Time**: format `DD.MM.YYYY HH:ii`.

## Checked

2026-11-04. Confirmed against the Uptime Kuma wiki: Maintenance page (1.19.0, fields, strategies, timezone, date format). Removed: Unconfirmed advice on strategy choice and container timezone, and the verify line.

Method: documentation only; no commands were run.
