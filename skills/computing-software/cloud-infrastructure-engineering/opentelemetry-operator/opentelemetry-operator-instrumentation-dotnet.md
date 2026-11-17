---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-instrumentation-dotnet
name: opentelemetry-operator-instrumentation-dotnet
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, dotnet, runtime-identifier, linux-musl-x64, inject-dotnet, enabled-instrumentations]
level: practitioner
status: docs-checked
description: "Inject .NET auto-instrumentation, choose the linux-x64 or linux-musl-x64 runtime identifier by annotation, and override the default traces instrumentations list."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/auto-instrumentation/languages/dotnet.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/auto-instrumentation/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# DotNet auto-instrumentation runtime identifiers

Enable with the annotation `instrumentation.opentelemetry.io/inject-dotnet: "true"`.

.NET auto-instrumentation also honors an annotation that sets the .NET Runtime Identifier (RID). Only two RIDs are supported, `linux-x64` (the default) and `linux-musl-x64`:

```
instrumentation.opentelemetry.io/inject-dotnet: "true"
instrumentation.opentelemetry.io/otel-dotnet-auto-runtime: "linux-x64"       # glibc images, default
instrumentation.opentelemetry.io/otel-dotnet-auto-runtime: "linux-musl-x64"  # musl images
```

Default instrumentations: for DotNet the operator sets `OTEL_DOTNET_AUTO_TRACES_ENABLED_INSTRUMENTATIONS` to every instrumentation supported by the `opentelemetry-dotnet-instrumentation` release in the image, i.e. `AspNet,HttpClient,SqlClient`. Override it by configuring the environment variable explicitly, for example in `spec.dotnet.env`.

Exporter port: .NET auto-instrumentation uses http/proto by default, so with `exporter.endpoint` on port 4317 you must add `OTEL_EXPORTER_OTLP_ENDPOINT` with port 4318 under `spec.dotnet.env`.

Other facts: the operator flag `enable-dotnet-instrumentation` defaults to true, and .NET is among the languages that can instrument init containers and that use the `dotnet-container-names` annotation in multi-instrumentation pods.

Related per-container controls: in multi-instrumentation pods use `instrumentation.opentelemetry.io/dotnet-container-names: "dotnet1,dotnet2"` to choose the containers, and note that a container cannot receive several language instrumentations at once. Without a container-names annotation, only the first regular container of the pod is instrumented.

## Checked

2026-11-04. Confirmed against docs/auto-instrumentation/languages/dotnet.md: `inject-dotnet`, the `otel-dotnet-auto-runtime` annotation with only `linux-x64` (default) and `linux-musl-x64`, and `OTEL_DOTNET_AUTO_TRACES_ENABLED_INSTRUMENTATIONS` defaulting to AspNet,HttpClient,SqlClient and overridable. Confirmed against docs/auto-instrumentation/README.md: `spec.dotnet.env` with `OTEL_EXPORTER_OTLP_ENDPOINT` on 4318 when the common endpoint uses 4317. Confirmed against docs/reference/feature-gates.md: `enable-dotnet-instrumentation` true. Confirmed against docs/auto-instrumentation/init-containers.md, multi-container.md and multi-instrumentation.md: .NET init container support, `dotnet-container-names`, first regular container by default, and no multiple languages per container. Nothing removed.

Method: documentation only; no commands were run.
