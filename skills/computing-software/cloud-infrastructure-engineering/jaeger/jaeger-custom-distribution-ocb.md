---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-custom-distribution-ocb
name: jaeger-custom-distribution-ocb
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, custom-distribution, ocb, builder-yaml, skip-strict-versioning]
level: sme
status: docs-checked
description: "Build a custom Jaeger binary with the OpenTelemetry Collector Builder using a builder.yaml manifest and --skip-strict-versioning."
sources:
  - https://www.jaegertracing.io/docs/2.22/deployment/custom-distribution/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: add or remove components in the Jaeger binary.

Reasons: add third-party Collector components, remove unused ones (smaller binary and attack surface), pin dependency versions for compliance.

Install ocb first. The manifest `builder.yaml` has `dist` (`module`, `name`, `description`, `output_path`), `telemetry`, and component lists whose entries use `gomod: github.com/jaegertracing/jaeger v2.19.0` plus an `import` such as `github.com/jaegertracing/jaeger/components/extension/jaegerstorage`, `.../jaegerquery`, `.../exporter/storageexporter`, `.../ext/receiver/otlpreceiver`, `.../ext/processor/batchprocessor`. Replace the version with the Jaeger release you base on; all component packages in a release share one version. The repository's reference manifest uses v0.0.0 with a replaces directive for in-repo builds, so outside the repo use a real release.

Components: Jaeger-specific ones under components/extension, exporter and processor; upstream OpenTelemetry ones re-exported under components/ext so versions stay consistent.

To add a component, append it, for example the resource detection processor from opentelemetry-collector-contrib. Use the same OpenTelemetry version Jaeger builds with (check Jaeger's go.mod) or builds may fail.

Build: `ocb --config builder.yaml --skip-strict-versioning`; run `./build/jaeger --config config.yaml`. Cross-compile with `GOOS=linux GOARCH=arm64 ocb --config builder.yaml`.

## Checked

2026-11-03. Confirmed against the Custom Distribution page: purpose, manifest layout, gomod and import entries, the v0.0.0 note about the reference manifest, component locations, matching OTel versions, ocb command with --skip-strict-versioning, the output binary run command, cross-compilation and single release version. Nothing removed.
Method: documentation only; no commands were run.
