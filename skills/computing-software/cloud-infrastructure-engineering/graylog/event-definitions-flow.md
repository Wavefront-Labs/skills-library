---
id: computing-software.cloud-infrastructure-engineering.graylog.event-definitions-flow
name: event-definitions-flow
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [event-definitions, events, alerts, notifications, event-procedures]
level: practitioner
status: docs-checked
description: "How an event definition works: evaluate, record, notify, respond; events versus alerts versus notifications."
sources:
  - https://go2docs.graylog.org/current/interacting_with_your_log_data/event_definitions.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# event definitions flow

An enabled event definition repeats a cycle:
1. **Evaluate**: on its schedule Graylog checks the condition. Depending on type it looks at log messages, other events, or signals such as anomaly results and asset risk scores.
2. **Record**: when met, Graylog creates an **event** carrying the definition's title, priority, tags and defined event fields; it appears on the Alerts & Events page.
3. **Notify**: if notifications are attached, Graylog sends them and the event is treated as an **alert**.
4. **Respond**: analysts triage by priority, follow event procedures, add events to investigations.

Terms: the *event definition* is the logic; the *event* is the record of each match; an *alert* is an event that triggered notifications; a *notification* is what is sent. Notification channels include email, Slack and HTTP request.

## Checked

2026-11-04. Confirmed against the Event Definitions page. Reworded the channel list to the page list (email, Slack, HTTP request) and removed the cron claim, which appears only as a link title.

Method: documentation only; no commands were run.
