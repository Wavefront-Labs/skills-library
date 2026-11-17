---
id: computing-software.cloud-infrastructure-engineering.alertmanager.event-recorder-config
name: event-recorder-config
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, event-recorder, feature-flag, audit-events]
level: sme
status: docs-checked
description: "Alertmanager event_recorder: gated by --enable-feature=event-recorder, with file, webhook, Kafka and stdout outputs and their delivery settings."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# event_recorder

The event recorder captures process start and shutdown, alert lifecycle transitions, silence creation, notification delivery and mute/inhibit suppressions. Each event includes a timestamp, the instance hostname, the cluster position (when HA is on) and event-specific data. Every event goes to every output.

It is gated behind a feature flag; without it the recorder silently discards events:

```
alertmanager --enable-feature=event-recorder
```

Configure under top-level `event_recorder` with output lists:

```yaml
event_recorder:
  stdout_outputs: [{}]
  file_outputs:
    - path: /path/to/events.jsonl
  webhook_outputs:
    - url: https://events.example.org/ingest
      workers: 1
```

- `file_outputs`: one JSON line per event at `path`; the file is reopened after rename, remove or create for logrotate.
- `stdout_outputs`: one JSON line per event, no extra fields. Consider `--log.format=json` so logs share one format.
- `webhook_outputs`: `timeout` 10s, `workers` 4, `max_retries` 3, `retry_backoff` 500ms (exponential, capped at 30s). Retries resend the event, so receivers should tolerate duplicates; use `workers: 1` when ordering matters. Batching: `batch`, `batch_max_events` 100, `batch_max_bytes` 1048576, `batch_flush_interval` 100ms.
- `kafka_outputs`: `brokers`, `topic` (must exist), `client_id` default `alertmanager`, `format` json or protobuf, `acks` none/leader/all (default leader), `compression`, `buffer_size` 1024 (events dropped when full), `tls_config`.

## Checked

2026-11-03. Confirmed against the Alertmanager Configuration page (prometheus.io/docs/alerting/latest/configuration): event_recorder feature flag, file/webhook/kafka/stdout outputs and defaults.

Method: documentation only; no commands were run.
