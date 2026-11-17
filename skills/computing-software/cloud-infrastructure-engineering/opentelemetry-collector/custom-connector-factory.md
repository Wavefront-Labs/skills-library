---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.custom-connector-factory
name: custom-connector-factory
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, custom-component, connector, factory, go]
level: sme
status: docs-checked
description: "Build a custom Collector connector in Go with connector.NewFactory and signal-specific create functions."
sources:
  - https://opentelemetry.io/docs/collector/extend/custom-component/connector/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A connector is one component that acts as an exporter at the end of one pipeline and a receiver at the start of another. In Go you describe it with a factory built by `connector.NewFactory`.

The factory takes:

- a component type (the name used in configuration)
- a function returning the default configuration
- options naming which signal pairs it supports, for example traces to metrics, built with the `connector.WithTracesToMetrics`, `connector.WithMetricsToMetrics` or similar options, each given a create function and a stability level (the tutorial uses `component.StabilityLevelAlpha`)

The create function receives the context, `connector.Settings`, your config and the next consumer in the downstream pipeline (for example `consumer.Metrics`), and returns a component such as `connector.Traces`. The tutorial's component implements `Capabilities` (reporting whether it mutates data) and `ConsumeTraces`; `Start` and `Shutdown` are optional, and embedding `component.StartFunc` and `component.ShutdownFunc` is enough when no special behaviour is needed. Inside `ConsumeTraces` it computes the output and passes it to the next consumer for the output signal.

A `Config` struct with `mapstructure` tags holds the settings and may have a `Validate` method. The connector appears as an exporter in the source pipeline and as a receiver in the destination one.

Test with unit tests (`go test -cover -v ./...` in the tutorial). To run it, add it under `connectors:` in an `ocb` manifest by `gomod` entry, with a `replaces` directive pointing at the local path while it is unpublished.

## Checked

Method: docs-checked 2026-11-09 against the Build a connector tutorial (raw index.md, read in full).
