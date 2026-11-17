---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.ocb-build-custom-collector
name: ocb-build-custom-collector
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, ocb, builder, manifest, custom-distribution, gomod]
level: advanced
status: docs-checked
description: "Build a custom Collector distribution with ocb from a builder-config.yaml manifest listing dist settings and gomod modules."
sources:
  - https://opentelemetry.io/docs/collector/extend/ocb/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The OpenTelemetry Collector Builder (`ocb`) generates a custom binary containing custom, upstream and other public components. It requires a compatible version of Go. Download the `ocb` asset for your OS and chipset from the releases with `cmd/builder` tags, run `chmod +x ocb`, and check it with `./ocb help`. On macOS run `brew tap open-telemetry/tap`, `brew trust open-telemetry/tap`, then `brew install ocb`.

The YAML manifest has a `dist` section and module-type sections. All `dist` tags are optional: `module`, `name` (default `otelcol-custom`), `description`, `output_path`, `version` (default `1.0.0`), `go` (default from PATH) and `debug_compilation` (default false).

```yaml
dist:
  name: otelcol-dev
  description: Basic OTel Collector distribution for Developers
  output_path: ./otelcol-dev
exporters:
  - gomod: go.opentelemetry.io/collector/exporter/otlpexporter <version>
processors:
  - gomod: go.opentelemetry.io/collector/processor/batchprocessor <version>
receivers:
  - gomod: go.opentelemetry.io/collector/receiver/otlpreceiver <version>
providers:
  - gomod: go.opentelemetry.io/collector/confmap/provider/fileprovider <version>
```

Build with `./ocb --config builder-config.yaml`. The log shows sources created, Go modules fetched, then compiled. The output folder holds `components.go`, `go.mod`, `main.go` and the binary named by `name`, so you can debug components in an IDE.

The page's example also adds the debug exporter and the env, http, https and yaml providers. The OpenTelemetry Registry lists each component's name and version.

## Checked

2026-11-03. Claims were read against these official pages:

- https://opentelemetry.io/docs/collector/extend/ocb/

Removed or reworded where the pages did not confirm them.

Method: documentation only; no commands were run.
