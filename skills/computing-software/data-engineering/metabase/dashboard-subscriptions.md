---
id: computing-software.data-engineering.metabase.dashboard-subscriptions
name: dashboard-subscriptions
category: computing-software
field: data-engineering
product: metabase
tags: [subscriptions, dashboard-subscriptions, attachments, attachment-row-limit, slack, email]
level: practitioner
status: docs-checked
description: "Schedule Metabase dashboard subscriptions: frequencies, email and Slack targets, filter value limits by plan, CSV/XLSX/PDF attachments and MB_ATTACHMENT_ROW_LIMIT."
sources:
  - https://www.metabase.com/docs/latest/dashboards/subscriptions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Scheduling: hourly, daily, weekly or monthly, with a time of day plus a day for weekly and monthly sends. Dashboard edits apply the next time a subscription is delivered. "Send email/Slack now" sends a test immediately to all subscribers, so test with your own address first.

Channels: email or Slack, both needing admin setup. Email can go to Metabase users or any external address. Slack can target a channel or an individual by username, not display name. Private Slack channels need extra configuration, and renaming a channel requires updating the subscription.

Filters: customizing filter values per subscription is plan-gated (the page shows a plans notice); dashboard filter default values are applied to subscriptions.

Attachments: CSV or XLSX, optionally unformatted. Default row limit is 1,048,575; self-hosters change it with `MB_ATTACHMENT_ROW_LIMIT`. PDF attachments are generated on the server, can take a minute or more, and use a light theme only. Iframe cards may render as links or fail.

Gotchas:
- "Don't send if there aren't results" can skip empty sends.
- Subscriptions from embedded dashboards omit Metabase links.
- Custom visualizations fall back to the default chart, because no one is signed in during delivery.
- The Usage analytics collection (plan-gated) lists all alerts and subscriptions.

## Checked

Method: 2026-11-08 read the cited page in full as raw markdown from the Metabase docs repository. Softened the Pro/Enterprise claims to the plans notices the page shows. Otherwise unchanged.
