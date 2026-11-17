---
id: computing-software.cloud-infrastructure-engineering.observability.otel-collector-builder-ocb-custom-distributions
name: otel-collector-builder-ocb-custom-distributions
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [ocb-manifest, builder-config, custom-distribution, collector-config, otel-collector]
level: advanced
status: docs-checked
description: "Build a custom OpenTelemetry Collector distribution with OCB: builder manifest, component gomod versions, providers, replaces, Docker image and CI version bumps."
sources: ["https://opentelemetry.io/docs/collector/custom-collector/", "https://github.com/open-telemetry/opentelemetry-collector/tree/main/cmd/builder", "https://github.com/open-telemetry/opentelemetry-collector-releases"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OCB builder and custom distributions

`otelcol-contrib` ships hundreds of components (large binary, bigger attack surface). Build your own with only
what you use, plus private components.

## Manifest (builder-config.yaml)
```yaml
dist:
  name: otelcol-acme
  description: Acme OpenTelemetry Collector
  output_path: ./_build
  version: 1.4.0
receivers:
  - gomod: go.opentelemetry.io/collector/receiver/otlpreceiver v0.163.0
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/filelogreceiver v0.163.0
processors:
  - gomod: go.opentelemetry.io/collector/processor/batchprocessor v0.163.0
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/processor/k8sattributesprocessor v0.163.0
exporters:
  - gomod: go.opentelemetry.io/collector/exporter/otlpexporter v0.163.0
  - gomod: go.opentelemetry.io/collector/exporter/otlphttpexporter v0.163.0
extensions:
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/extension/healthcheckextension v0.163.0
providers:
  - gomod: go.opentelemetry.io/collector/confmap/provider/envprovider v1.69.0
  - gomod: go.opentelemetry.io/collector/confmap/provider/fileprovider v1.69.0
replaces:
  - github.com/acme/otel/processor/tenantprocessor => ../tenantprocessor   # local component
```
Versions: the otelcol-contrib manifest at v0.163.1 pins beta components to v0.163.0 and the stable confmap providers to v1.69.0
(the builder's own defaults are the same pair), so pick component versions from one collector release. Module types are
`extensions`, `exporters`, `receivers`, `processors`, `connectors`, `providers` and `converters`; each entry needs at least
`gomod`. `dist.module`, `name`, `description`, `output_path`, `version`, `go` and `debug_compilation` are optional.

## Build
```bash
go install go.opentelemetry.io/collector/cmd/builder@v0.163.0
builder --config=builder-config.yaml
./_build/otelcol-acme components     # lists compiled-in components
```
The builder README recommends the official release Docker image (`otel/opentelemetry-collector-builder`, mount your manifest at
`/build/builder-config.yaml` and pass `--config`) or the release binaries over `go install`, and notes that with `go install` the
binary is called `builder`. It also needs a compatible Go version. By default LDflags are `-s -w`, which strips debug symbols
(`debug_compilation: true` keeps them). Steps can be skipped with `--skip-generate`, `--skip-get-modules` and `--skip-compilation`.
Example multi-stage Dockerfile:
```dockerfile
FROM golang:<compatible Go version> AS build
RUN go install go.opentelemetry.io/collector/cmd/builder@v0.163.0
COPY builder-config.yaml .
RUN CGO_ENABLED=0 builder --config=builder-config.yaml
FROM gcr.io/distroless/static
COPY --from=build /go/_build/otelcol-acme /otelcol-acme
ENTRYPOINT ["/otelcol-acme"]
```

## Operating it
- Bump the builder and every gomod together; validate configs in CI with `otelcol-acme validate --config=<file>`.
- The builder has default providers (env, file, http, https, yaml). If you list `providers` yourself, include every provider you
  need, and add contrib providers such as `s3provider` explicitly. `conf_resolver.default_uri_scheme: env` makes a bare `${VAR}`
  expand as an env var.
- For the Helm chart, check the chart README for the image and command settings.

## Checked

2026-10-24. OpenTelemetry Collector cmd/builder README and builder config.go (main branch), otelcol-contrib manifest v0.163.1, and the collector confmap resolver. Confirmed: manifest keys (`dist.*`, module types, `replaces`, `conf_resolver.default_uri_scheme`), `gomod` requirement, builder binary name for `go install`, recommended install methods, default LDflags and `debug_compilation`, skip flags, default providers (env, file, http, https, yaml), default versions v0.163.0 / v1.69.0, and the `components` and `validate` subcommands. Removed the claim that mixed versions panic, that providers must always be listed, and the Helm chart value names (not covered by these sources). Old pinned v0.115.0/v1.21.0 versions replaced with the v0.163.0/v1.69.0 pair.

Method: documentation only; no commands were run.
