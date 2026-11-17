---
id: computing-software.cloud-infrastructure-engineering.observability.otel-java-agent-configuration-and-extensions
name: otel-java-agent-configuration-and-extensions
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [java-agent-configuration, java-agent-extensions, disable-instrumentation-java, language-instrumentation, zero-code-instrumentation]
level: advanced
status: docs-checked
description: "Configure the OpenTelemetry Java agent: properties file and env vars, enabling or disabling instrumentations, method spans, header capture, debug mode, and extension jars."
sources: ["https://opentelemetry.io/docs/zero-code/java/agent/configuration/", "https://opentelemetry.io/docs/zero-code/java/agent/disable/", "https://opentelemetry.io/docs/zero-code/java/agent/extensions/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenTelemetry Java agent: configuration and extensions

## Attach
```bash
export JAVA_TOOL_OPTIONS="-javaagent:/otel/opentelemetry-javaagent.jar"
export OTEL_SERVICE_NAME=checkout OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-agent:4318
java -jar app.jar
```
Every `-Dotel.x.y` property has an env form `OTEL_X_Y`. Collect them in a file:
`-Dotel.javaagent.configuration-file=/otel/agent.properties`.

## Turning instrumentations on/off
```properties
# disable one
otel.instrumentation.jdbc.enabled=false
# opt-in model: everything off, enable the ones you want
otel.instrumentation.common.default-enabled=false
otel.instrumentation.spring-webmvc.enabled=true
otel.instrumentation.http-url-connection.enabled=true
```
Names are the module names in the agent's supported-libraries list (`otel.instrumentation.[name].enabled`). Disable noisy ones rather than filtering spans downstream.

## Common knobs
| Property | Purpose |
|---|---|
| `otel.instrumentation.experimental.span-suppression-strategy` | controls suppression of nested spans (see the configuration page for values) |
| `otel.javaagent.logging` | agent log mode; `simple` (stderr, INFO and above) is the default, `application` is the other documented mode |
`@WithSpan` (with `otel.instrumentation.opentelemetry-instrumentation-annotations.enabled=true` when default-enabled is false) for code-level spans.

## Extensions
Custom samplers, span processors, resource providers, propagators or even new instrumentation modules are packaged
as an extension jar: `-Dotel.javaagent.extensions=/otel/acme-ext.jar` (see the extensions page for accepted values).
```java
@AutoService(AutoConfigurationCustomizerProvider.class)
public class AcmeCustomizer implements AutoConfigurationCustomizerProvider {
  public void customize(AutoConfigurationCustomizer c) {
    c.addTracerProviderCustomizer((b, cfg) -> b.addSpanProcessor(new DropHealthChecksProcessor()));
  }
}
```
The docs show extensions built on the `AutoConfigurationCustomizerProvider` SPI.

## Gotchas
- Versions 2.0+ of the Java agent use http/protobuf as the default OTLP protocol, not grpc (so the endpoint is 4318); read release notes on upgrade.

## Verify
Run locally with a console or debug exporter as described in the agent docs, confirm expected spans, then switch to OTLP.

## Checked
- 2026-10-28. Checked against the OpenTelemetry Java agent configuration, disable-instrumentation and extensions pages (docs as served 2026-10).
- Confirmed: `otel.javaagent.configuration-file`, env-var form rule, `otel.instrumentation.common.default-enabled`, `otel.instrumentation.[name].enabled`, `otel.javaagent.extensions`, `otel.javaagent.logging` modes, `AutoConfigurationCustomizerProvider`, `addTracerProviderCustomizer`, `@WithSpan`, 2.0+ http/protobuf default.
- Removed (unconfirmed): `methods.include`, header capture and DB sanitizer properties, `otel.javaagent.debug`, span-suppression value, `@SpanAttribute`, `otel.traces.exporter=logging`, `jdbc-datasource` and other module-name examples, two-agent and startup-overhead claims.
Method: documentation only; no commands were run.
