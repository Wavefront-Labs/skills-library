---
id: computing-software.software-engineering.spring-boot.metrics-micrometer-registries
name: metrics-micrometer-registries
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, actuator, metrics, micrometer, meterregistry, datadog, dynatrace, graphite, atlas]
level: practitioner
status: docs-checked
description: "Micrometer metrics in Boot: composite registry, disabling registries, global registry, MeterRegistryCustomizer and export settings for Atlas, Datadog, Dynatrace, Elastic and more."
sources:
  - https://docs.spring.io/spring-boot/reference/actuator/metrics.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Boot provides dependency management and auto-configuration for Micrometer. It configures a composite `MeterRegistry` and adds a registry for each supported implementation found on the classpath; a runtime dependency on `micrometer-registry-{system}` is enough. Supported: Atlas, Datadog, Dynatrace, Elastic, Ganglia, Graphite, Humio, Influx, JMX, KairosDB, New Relic, OTLP, Prometheus, simple (in-memory), Stackdriver, StatsD.

Disable one registry (example Datadog) or all unless a registry says otherwise:
```yaml
management:
  datadog:
    metrics:
      export:
        enabled: false
```
```yaml
management:
  defaults:
    metrics:
      export:
        enabled: false
```
Registries are added to the global static registry on `Metrics` unless `management.metrics.use-global-registry: false`. Register `MeterRegistryCustomizer` beans (any number; narrow the generic type for one implementation) to apply, for example, common tags before meters are registered.

Export settings (key prefix `management.<system>.metrics.export.`):
- Atlas: defaults to localhost; `uri: "https://atlas.example.com:7101/api/v1/publish"`.
- Datadog: `api-key`; optional `application-key` also exports metadata (descriptions, types, base units); `uri` (default US site `https://api.datadoghq.com`, for example `https://api.datadoghq.eu`); `step: "30s"`.
- Dynatrace: v2 API recommended (v1 deprecated; a set `v1.device-id` selects v1). v2 auto-configures with a local OneAgent or the Dynatrace Operator in Kubernetes, needing only `io.micrometer:micrometer-registry-dynatrace`. Manual: `uri` including path (`/api/v2/metrics/ingest`) and `api-token` with only the `metrics.ingest` permission. Optional `v2.metric-key-prefix`, `enrich-with-dynatrace-metadata`, `default-dimensions`, `use-dynatrace-summary-instruments`, `export-meter-metadata`. Default `step` is 60s.
- Elastic: `host`.
- Ganglia: `host`, `port`.
- Graphite: `host`, `port`; to change hierarchical name mapping define your own `GraphiteMeterRegistry` with a `HierarchicalNameMapper`.
- Humio: `api-token`, and `tags` identifying the data source.

## Checked

2026-11-07

Read metrics.adoc (docs-repo source of the cited Metrics page) in full, including the registries after Humio (Influx, JMX, KairosDB, New Relic, OTLP, Prometheus, Simple, Stackdriver, StatsD), supported meters, custom metrics and the metrics endpoint. Include-code examples (for example MyMeterRegistryConfiguration, MyGraphiteConfiguration) were not opened.
Confirmed: composite MeterRegistry and the micrometer-registry-{system} classpath rule; the 16-system list; management.datadog.metrics.export.enabled=false and management.defaults.metrics.export.enabled=false; management.metrics.use-global-registry=false; MeterRegistryCustomizer (common tags, narrowing by generic type); Atlas default local machine and uri; Datadog api-key, application-key metadata, uri default https://api.datadoghq.com and .eu example, step 30s; Dynatrace v1/v2 rules, device-id selecting v1, OneAgent / Operator auto-configuration with micrometer-registry-dynatrace, manual uri path /api/v2/metrics/ingest, token metrics.ingest permission, the five optional v2 settings, default step 60s; Elastic host; Ganglia host and port; Graphite host and port with GraphiteMeterRegistry / HierarchicalNameMapper; Humio api-token and tags.
Trimmed: the leftover "Not read: ..." line, since the rest of the page was read and nothing in it contradicts the skill.

Method: documentation only; no commands were run.
