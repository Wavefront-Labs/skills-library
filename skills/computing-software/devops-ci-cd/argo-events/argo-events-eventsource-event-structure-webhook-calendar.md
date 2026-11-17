---
id: computing-software.devops-ci-cd.argo-events.argo-events-eventsource-event-structure-webhook-calendar
name: argo-events-eventsource-event-structure-webhook-calendar
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, cloudevents, event-structure, webhook, calendar, schedule, interval, userpayload]
level: intro
status: docs-checked
description: "Know the CloudEvent shape that webhook and calendar EventSources publish and how the calendar source generates events."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/eventsources/setup/calendar.md", "https://github.com/argoproj/argo-events/blob/master/docs/eventsources/setup/webhook.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events eventsource event structure webhook calendar

Every EventSource wraps its output in a CloudEvent: a `context` (type, specversion, source, id, time, datacontenttype, subject) plus type-specific `data`.

Webhook: an HTTP server lets external systems trigger workloads. `data` holds `header` (the request headers) and `body` (the request payload). Setup: apply `examples/event-sources/webhook.yaml`; it listens on port 12000, endpoint `/example`. Then apply the sensor `examples/sensors/webhook.yaml` and POST to the service once the Sensor pod runs. The spec is `WebhookContext` in the API docs.

Calendar: generates events on a cron schedule or at an interval, so Sensors can run periodic workloads. `data` holds `eventTime` (UTC time of the event) and `userPayload` (a static payload configured in the EventSource). The example `calendar.yaml` fires every 10 seconds; apply `examples/sensors/calendar.yaml` and wait for the next interval for the workflow to be created. The spec type is `CalendarEventSource`.

In `context`, `source` is the name of the event source and `subject` is the name of the configuration within the event source.

For troubleshooting see the FAQ page. Calendar also supports catch-up of missed schedules via persistence (Calendar EventSource Catch Up page).

## Checked

2026-11-04. Confirmed against the Webhook and Calendar EventSource pages: the `context` fields, webhook `data` (`header`, `body`), calendar `data` (`eventTime`, `userPayload`), the spec types `WebhookContext` and `CalendarEventSource`, port `12000` and endpoint `/example`, the 10-second calendar interval and the example manifest paths. Removed the sentence on reading fields through `dataKey: body.message` and the claim that `subject` equals the map key, which these pages do not state.
Method: documentation only; no commands were run.
