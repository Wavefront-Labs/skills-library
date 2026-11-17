---
id: computing-software.cloud-infrastructure-engineering.datadog.downtimes-muting
name: downtimes-muting
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, downtimes, scheduled-downtime, mute, maintenance]
level: practitioner
status: docs-checked
description: "Schedule Datadog downtimes to silence monitor notifications during maintenance, scoped by monitor name or tags and group scope, one-time or recurring with RRULE."
sources: ["https://docs.datadoghq.com/monitors/downtimes/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Downtimes and muting
Goal: avoid alert noise during planned work without hiding real incidents.

Create at Manage Downtime > Schedule Downtime, or click the mute icon on a monitor status page to make a downtime for that monitor.

- A downtime silences alerts and notifications but does not stop monitor state transitions; monitors still evaluate.
- Choose targets "By Monitor Name" (an empty field silences all monitors) or "By Monitor Tags" (up to 32 tags, each up to 256 characters; a monitor must have all selected tags). Use Preview affected monitors to check. Monitors created or edited later are included automatically if they match.
- Group scope narrows further and is matched after the monitor targeting. Use `*` for all groups. Examples from the docs: `service:web-store AND env:dev`, `env:(dev OR staging)`, `host:authentication-*`, `service:web-store AND -env:prod`. A scope on `service:web-store` mutes every group containing it, such as `service:web-store,host:a`.
- Scope limits: at most two levels of nesting; negation only for key/value pairs and `-key(A OR B)`; no top-level `OR` between different keys (use two downtimes); keys are required (no bare `prod`); `?` wildcard is not supported, use `*`.
- One-time: start date, time and time zone, with optional end. Recurring: start, time zone, repeat and duration, with optional end date or occurrence count, defined with RRULEs (a monthly example is the third Monday). RRULE attributes for duration (`DTSTART`, `DTEND`, `DURATION`) are not supported. Each recurrence is created as a new downtime owned by the original creator.
- Notifications: a message (markdown and `@` handles) is sent when the downtime is scheduled, started, cancelled or expired.
- By default a recovery that happens during a downtime for a monitor that triggered before it is still notified; a checkbox mutes this first recovery notification. Further transitions during the downtime are always muted.
- Permissions: Manage Downtimes permission to schedule, edit or cancel. With downtime access controls (Preview) a downtime only silences monitors you have Muter or Editor access to.
- History: Monitor Status page overlay, or Event Explorer search `tags:audit downtime`.
- If SLOs share tags with a new downtime, the editor can create a matching SLO status correction.

Gotcha: a scope of `*` with no monitor targeting mutes everything; keep scopes narrow and set an end time.

## Verify
- Manage Downtime lists it as Active and Preview affected monitors shows only the intended monitors.

## Checked
2026-11-03. Confirmed against the Downtimes page. Removed: the v2 API curl example and `notify_end_states` (not on the page), the "re-check Manage Monitors after the window" and Terraform advice.
Method: documentation only; no commands were run.
