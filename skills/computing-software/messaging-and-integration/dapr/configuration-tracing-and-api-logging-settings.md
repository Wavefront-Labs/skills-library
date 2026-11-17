---
id: computing-software.messaging-and-integration.dapr.configuration-tracing-and-api-logging-settings
name: configuration-tracing-and-api-logging-settings
category: computing-software
field: messaging-and-integration
product: dapr
tags: [configuration, tracing, samplingrate, otel, zipkin, api-logging, obfuscateurls, omithealthchecks]
level: practitioner
status: docs-checked
description: "Sidecar Configuration for tracing (samplingRate, otel, zipkin, OTEL_EXPORTER_OTLP variables) and apiLogging (enabled, obfuscateURLs, omitHealthChecks), with documented defaults."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/configuration/configuration-overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Tracing block:

```yml
tracing:
  samplingRate: "1"
  otel: 
    endpointAddress: "otelcollector.observability.svc.cluster.local:4317"
  zipkin:
    endpointAddress: "http://zipkin.default.svc.cluster.local:9411/api/v2/spans"
```

- `samplingRate` (string, range 0 to 1): `"1"` samples every trace, `"0"` disables tracing; default is 0.0001 (1 in 10,000).
- `stdout` (bool): more verbose trace output.
- `otel.endpointAddress`, `otel.isSecure`, `otel.protocol` (`http` or `grpc`). Whether the address needs a scheme depends on your OTEL provider.
- `zipkin.endpointAddress` must include `http://` or `https://`.

The OTEL exporter can instead come from the environment; the presence of `OTEL_EXPORTER_OTLP_ENDPOINT` turns tracing on for the sidecar. Others: `OTEL_EXPORTER_OTLP_INSECURE` (true/false) and `OTEL_EXPORTER_OTLP_PROTOCOL` (`grpc`, `http/protobuf`, `http/json`).

Logging block:

```yml
logging:
  apiLogging:
    enabled: false
    obfuscateURLs: false
    omitHealthChecks: false
```

- `apiLogging.enabled` is the default for the `--enable-api-logging` flag (annotation `dapr.io/enable-api-logging`); an explicit flag value wins over the Configuration.
- `obfuscateURLs` logs the abstract route name instead of the full path, which may contain personally identifiable information.
- `omitHealthChecks` skips `/v1.0/healthz` calls when API logging is on, reducing noise.

## Checked

2026-11-08. Read the cited dapr/docs v1.15 page in full and compared each claim; all claims matched the page and none were changed.

Method: documentation only; no commands were run.
