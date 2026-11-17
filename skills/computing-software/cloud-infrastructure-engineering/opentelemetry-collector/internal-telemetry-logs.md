---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.internal-telemetry-logs
name: internal-telemetry-logs
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, internal-telemetry, logs, log-level, encoding]
level: practitioner
status: docs-checked
description: "Set the Collector's own log level, encoding and output, and export its logs over OTLP."
sources:
  - https://opentelemetry.io/docs/collector/internal-telemetry/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default the Collector emits its own logs to `stderr`. Configure them under `service::telemetry::logs`. Defaults from the page's table:

- `level`: `INFO`; also `DEBUG`, `WARN`, `ERROR`.
- `encoding`: `console`; the other value is `json`.
- `development`: `false`.
- `disable_caller`: `false`, so logs are annotated with file name and line number.
- `disable_stacktrace`: `false`; stacktraces are captured at `WARN` and above in development and `ERROR` and above in production.
- `sampling::enabled` `true`, `sampling::tick` `10s`, `sampling::initial` `10`, `sampling::thereafter` `100` (every Nth message after the initial ones).
- `output_paths` and `error_output_paths`: `["stderr"]`, lists of URLs or file paths.
- `initial_fields`: static key-value pairs added to every entry; none by default.

On a Linux systemd host you can also read logs with `journalctl | grep otelcol`, adding `| grep Error` for errors only.

To emit internal logs to an OTLP/HTTP backend:

```yaml
service:
  telemetry:
    logs:
      processors:
        - batch:
            exporter:
              otlp:
                protocol: http/protobuf
                endpoint: https://backend:4318
```

The page warns the declarative configuration schema is under development and may have breaking changes.

## Checked

2026-11-03. Claims were read against these official pages:

- https://opentelemetry.io/docs/collector/internal-telemetry/

Removed or reworded where the pages did not confirm them.

Method: documentation only; no commands were run.
