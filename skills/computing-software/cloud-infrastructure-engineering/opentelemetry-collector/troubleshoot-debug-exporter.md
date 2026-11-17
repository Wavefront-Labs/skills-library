---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.troubleshoot-debug-exporter
name: troubleshoot-debug-exporter
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, troubleshooting, debug-exporter, verbosity, pipeline]
level: intro
status: docs-checked
description: "Print telemetry passing through a pipeline with the debug exporter at basic, normal or detailed verbosity."
sources:
  - https://github.com/open-telemetry/opentelemetry-collector/blob/main/exporter/debugexporter/README.md
  - https://opentelemetry.io/docs/collector/troubleshooting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For live troubleshooting, the troubleshooting page recommends the `debug` exporter, which prints what the Collector receives, processes and exports to its logs. Its example sends Zipkin data to it:

```yaml
receivers:
  zipkin:
exporters:
  debug:
    verbosity: detailed
service:
  pipelines:
    traces:
      receivers: [zipkin]
      processors: []
      exporters: [debug]
```

Post a payload with `curl -X POST localhost:9411/api/v2/spans -H'Content-Type: application/json' -d @trace.json`. At the default verbosity you get one line such as `TracesExporter ... "resource spans": 1, "spans": 2`; `detailed` also prints each span's IDs, name, kind, times, status and attributes.

Details from the exporter README:

- `verbosity` defaults to `basic`: a single-line summary with a count per batch. `normal` prints about one line per telemetry record, and `detailed` prints all details over multiple lines.
- `sampling_initial` (default 2) and `sampling_thereafter` (default 1, meaning no sampling) throttle messages; raise `sampling_thereafter` to enable sampling.
- `use_internal_logger` defaults to true. With `false`, `output_paths` (default `stdout`) can send output to `stderr` or files.
- `sending_queue` is disabled by default.

## Checked

2026-11-03. Claims were read against these official pages:

- https://github.com/open-telemetry/opentelemetry-collector/blob/main/exporter/debugexporter/README.md
- https://opentelemetry.io/docs/collector/troubleshooting/

Removed or reworded where the pages did not confirm them.

Method: documentation only; no commands were run.
