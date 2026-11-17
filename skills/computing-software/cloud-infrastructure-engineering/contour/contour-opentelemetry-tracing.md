---
id: computing-software.cloud-infrastructure-engineering.contour.contour-opentelemetry-tracing
name: contour-opentelemetry-tracing
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [tracing, opentelemetry, otlp, extensionservice, sampling, customtags, otel-collector]
level: advanced
status: docs-checked
description: "Contour tracing to an OpenTelemetry collector: ExtensionService h2c port 4317, tracing config block, sampling rates, custom tags, includePodDetail."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/tracing.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# OpenTelemetry tracing

Contour configures Envoy to export traces to an OpenTelemetry collector.

1. Deploy a collector (the doc uses the OpenTelemetry operator and an `OpenTelemetryCollector` named `simplest` in `projectcontour` with an `otlp` receiver for grpc and http).
2. Create an ExtensionService pointing to it:

```yaml
apiVersion: projectcontour.io/v1alpha1
kind: ExtensionService
metadata:
  name: otel-collector
  namespace: projectcontour
spec:
  protocol: h2c
  services:
  - name: simplest-collector
    port: 4317
```

3. Add to the Contour config file, then restart the Contour deployment:

```yaml
tracing:
  extensionService: projectcontour/otel-collector
  serviceName: some-service-name
  includePodDetail: true
  overallSampling: 100
  clientSampling: 100
  randomSampling: 100
  customTags:
  - tagName: custom-tag
    literal: foo
  - tagName: header-tag
    requestHeaderName: X-Custom-Header
```

Defaults: `serviceName` is `contour`; all three sampling rates are 100; max request path length is 256; `includePodDetail` (default true) sends the pod hostname and namespace. A `requestHeaderName` tag is omitted when the header is absent.

Verify with `kubectl logs deploy/simplest-collector -n projectcontour` after calling an app (the page's collector uses a logging exporter with verbose output). Trace and span identifiers can also be included in access logs to correlate entries with traces; see the access logging page.

## Checked

2026-11-08. Read the Contour main-branch config page tracing.md in full. Confirmed: the ExtensionService with h2c and port 4317, the `tracing` config keys and their defaults (service name, sampling rates of 100, path length 256, `includePodDetail`), custom tags, the restart note and the verification command. Removed the claim that the export is OTLP gRPC and the `%TRACE_ID%` access log token, which the page does not state.

Method: documentation only; no commands were run.
