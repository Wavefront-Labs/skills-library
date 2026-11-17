---
id: computing-software.cloud-infrastructure-engineering.observability.otel-declarative-configuration-file
name: otel-declarative-configuration-file
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [declarative-configuration-yaml, otel-config-file, language-instrumentation, sdk-configuration, otel-configuration-schema]
level: advanced
status: docs-checked
description: "Configure OpenTelemetry SDKs with a declarative YAML file: schema, env substitution, tracer/meter/logger provider blocks, samplers, views, and language support."
sources: ["https://opentelemetry.io/docs/specs/otel/configuration/", "https://github.com/open-telemetry/opentelemetry-configuration", "https://github.com/open-telemetry/opentelemetry-configuration/blob/main/language-support-status.md", "https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/configuration/data-model.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Declarative configuration file

Env vars cannot express views, multiple exporters or per-processor settings. The declarative config file (schema in
`open-telemetry/opentelemetry-configuration`) describes the whole SDK in YAML. Point the SDK at it with
`OTEL_CONFIG_FILE=/etc/otel/sdk.yaml` (`OTEL_EXPERIMENTAL_CONFIG_FILE` is deprecated). When set, the file takes precedence
over all other SDK configuration environment variables; env values can still be pulled in with substitution.

## Example
```yaml
file_format: "1.0"            # use a version your SDK supports (see Language support); the schema repo's current example uses "1.2"
disabled: ${OTEL_SDK_DISABLED:-false}
resource:
  attributes:
    - {name: service.name, value: "${OTEL_SERVICE_NAME:-checkout}"}
    - {name: deployment.environment.name, value: prod}
propagator:
  composite: [{tracecontext: {}}, {baggage: {}}]
tracer_provider:
  processors:
    - batch:
        schedule_delay: 1000
        exporter:
          otlp_http:
            endpoint: ${OTEL_EXPORTER_OTLP_ENDPOINT:-http://localhost:4318}/v1/traces
            headers: [{name: authorization, value: "Bearer ${API_TOKEN}"}]
  sampler:
    parent_based:
      root:
        trace_id_ratio_based: {ratio: 0.1}
meter_provider:
  readers:
    - periodic:
        interval: 60000
        exporter:
          otlp_http: {endpoint: http://localhost:4318/v1/metrics, temporality_preference: cumulative}
  views:
    - selector: {instrument_name: http.server.request.duration}
      stream:
        aggregation:
          base2_exponential_bucket_histogram: {max_size: 160}
        attribute_keys: {included: [http.request.method, http.route, http.response.status_code]}
logger_provider:
  processors:
    - batch: {exporter: {otlp_http: {endpoint: http://localhost:4318/v1/logs}}}
```
Substitution (spec data model): `${VAR}`, `${env:VAR}` and `${VAR:-default}`; the default applies when the variable is null, empty
or undefined, and an undefined variable without a default becomes an empty value. Only scalar values are substituted, not mapping
keys. `$$` is an escape for a literal `$` (`$${API_KEY}` yields `${API_KEY}`). Implementations may add prefixes such as `sys:`.
Key names change between schema versions (unstable keys carry a `/development` suffix, for example `instrumentation/development`),
so validate against the schema release your SDK supports.

## Language support
The schema repo's language support status page lists cpp, go, java, js, php and python. Latest supported file format there:
`1.0.0` for cpp, go and python; `1.0.0-rc.3` for java and js; `1.0.0-rc.2` for php. Go uses the module
`go.opentelemetry.io/contrib/otelconf`. Per-type support (supported, ignored, not_implemented) is on that page, so check it before
relying on a field, for example views or cardinality limits.

## Why use it
- One reviewed file per environment in Git, rendered via ConfigMap.
- Views and multiple exporters (e.g. OTLP + Prometheus pull) without code.
- Same file across languages.

## Verify
Start with `disabled: false` and add a `console` exporter to a span processor; spans print with the configured resource.
Validate the file against the JSON schema (`opentelemetry_configuration.json` in the schema repo) before deploying.

## Checked

2026-10-24. opentelemetry-configuration repository (release v1.2.0): opentelemetry_configuration.json schema, examples/otel-sdk-config.yaml, language-support-status.md; OpenTelemetry specification configuration/data-model.md and sdk-environment-variables.md; opentelemetry-go-contrib otelconf module. Confirmed: `OTEL_CONFIG_FILE` precedence and the deprecated experimental variable, resource, propagator composite list, batch processor and otlp_http fields (`endpoint`, `headers` as name/value list, `compression`, `timeout`, `temporality_preference`), `trace_id_ratio_based.ratio`, view `selector.instrument_name`, `stream.aggregation.base2_exponential_bucket_histogram.max_size`, `stream.attribute_keys.included`, substitution and escape rules, and per-language file format support. Removed unconfirmed Java agent property and fail-fast claims.

Method: documentation only; no commands were run.
