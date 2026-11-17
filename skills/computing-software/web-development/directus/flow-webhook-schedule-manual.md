---
id: computing-software.web-development.directus.flow-webhook-schedule-manual
name: flow-webhook-schedule-manual
category: computing-software
field: web-development
product: directus
tags: [flow-webhook, flow-schedule-cron, flow-manual-trigger, flow-chaining]
level: practitioner
status: docs-checked
description: "Set up Directus flow webhook, cron schedule, another-flow and manual button triggers with their options for async responses and confirmation inputs."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/06.flows/3.triggers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Webhook**: call `GET` or `POST` on `/flows/trigger/<trigger-id>` (copy the URL from the panel). Options: method, Asynchronous, Response Body, Error on Reject, Cache (GET responses). Async responds immediately without a body; sync waits and returns the Response Body. With no Response Body defined the response is empty.

**Schedule (CRON)**: 6-point syntax, seconds first:

```
second minute hour day-of-month month day-of-week
```

**Another Flow**: runs via the Trigger Flow operation; its Response Body is appended under that operation's key. Passing an array runs the flow once per item.

**Manual**: a Studio button. Pick Collections and Location (item page, collection page, both, or None (Hidden) for use from a Button Links interface). It needs item IDs, passed to `$trigger` as an array; the collection-page button is grey until items are selected (toggle controls that). Options: Asynchronous, Require Confirmation, Error on Reject. Confirmation dialog can have a description and input fields; user input lands in `$trigger.body`.

## Checked

2026-11-04: confirmed against the Directus docs Triggers page (Webhook, Schedule, Another Flow, Manual sections): webhook path and options, asynchronous behaviour, 6-point cron order, response body on another flow, manual trigger options, confirmation inputs in $trigger.body. Removed the unsupported verify line.

Method: documentation only; no commands were run.
