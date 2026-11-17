---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.troubleshoot-zpages-and-pprof
name: troubleshoot-zpages-and-pprof
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, troubleshooting, zpages, pprof, extensions, performance]
level: advanced
status: docs-checked
description: "Inspect a running Collector with the zpages extension on port 55679 and profile it with the pprof extension on port 1777."
sources:
  - https://github.com/open-telemetry/opentelemetry-collector/blob/main/extension/zpagesextension/README.md
  - https://opentelemetry.io/docs/collector/troubleshooting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The troubleshooting page lists two debugging extensions. The pprof extension is available locally on port `1777` and lets you profile the Collector as it runs; the page calls this an advanced use case rarely needed. The zPages extension is exposed locally on port `55679` and inspects live data from the Collector's receivers and exporters.

```yaml
extensions:
  pprof:
    endpoint: 0.0.0.0:1777
  zpages:
    endpoint: 0.0.0.0:55679
service:
  extensions: [pprof, zpages]
```

The page suggests changing zPages `endpoint` for containers, to `0.0.0.0:55679`, so the port is reachable beyond the container.

Details from the pages and README:

- The TraceZ page at `/debug/tracez` helps with latency issues, spans that never end (deadlocks and instrumentation problems), and the types and locations of errors. It can show error logs the Collector does not emit itself.
- Other routes: `/debug/servicez` (overview, build and runtime information), `/debug/pipelinez` (pipelines and their components), `/debug/extensionz` and `/debug/featurez` (feature gates).
- The zPages `endpoint` default is `localhost:55679`; `:<port>` exposes it on all interfaces.
- Core exporters and receivers provide zPage instrumentation, with no backend needed.
- Check zPages and logs when the Collector is not receiving or exporting data.

## Checked

2026-11-03. Claims were read against these official pages:

- https://github.com/open-telemetry/opentelemetry-collector/blob/main/extension/zpagesextension/README.md
- https://opentelemetry.io/docs/collector/troubleshooting/

Removed or reworded where the pages did not confirm them.

Method: documentation only; no commands were run.
