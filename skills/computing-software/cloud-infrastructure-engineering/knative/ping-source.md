---
id: computing-software.cloud-infrastructure-engineering.knative.ping-source
name: ping-source
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [pingsource, cron-schedule, ceoverrides, event-source, timezone]
level: intro
status: docs-checked
description: "Emit fixed-payload CloudEvents on a cron schedule with a PingSource and its spec fields."
sources:
  - https://knative.dev/docs/eventing/sources/ping-source/
  - https://knative.dev/docs/eventing/sources/ping-source/reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: generate scheduled test or heartbeat events for a sink.

A PingSource produces events with a fixed payload on a cron schedule. It is enabled by default when Knative Eventing is installed, and you can create components with either `kubectl` or `kn`.

Spec fields from the reference page:
- `spec.schedule`: cron expression, defaulting to `* * * * *`. The creation page says both standard and Quartz Scheduler cron formats are supported, the latter adding a seconds field.
- `spec.timezone`: shifts the schedule relative to a tz database zone; defaults to the system time zone.
- `spec.data`: the event body. Default is empty. Mutually exclusive with `dataBase64`.
- `spec.dataBase64`: base64-encoded body, for binary payloads.
- `spec.contentType`: media type of `data` or `dataBase64`. Default is empty.
- `spec.sink`: required reference resolving to the destination URI.
- `spec.ceOverrides.extensions`: attributes added or overridden on each outbound event.

```yaml
apiVersion: sources.knative.dev/v1
kind: PingSource
metadata:
  name: test-ping-source
spec:
  schedule: "*/1 * * * *"
  contentType: "application/json"
  data: '{"message": "Hello world!"}'
  sink:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: event-display
```

`status.sinkUri` shows the sink address the controller resolved, and `status.conditions` reports readiness.

The page uses a Service that dumps incoming messages to its log as the sink; reading that log shows each event as it arrives.

## Checked

2026-11-04. Confirmed against the Creating a PingSource object page and the PingSource reference page (knative/docs source): fixed payload on a cron schedule, enabled by default with Knative Eventing, `kubectl` or `kn` usage, every spec field with its default (`schedule` `* * * * *`, `timezone` defaults to the system zone, `data` and `dataBase64` mutually exclusive, `contentType`, required `sink`, `ceOverrides.extensions`), `status.sinkUri` and `status.conditions`, and the event-display sink used to verify. Added the cron-format note from the creation page and the reference page to sources. Nothing removed.

Method: documentation only; no commands were run.
