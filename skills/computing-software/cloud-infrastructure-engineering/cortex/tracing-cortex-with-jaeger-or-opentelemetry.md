---
id: computing-software.cloud-infrastructure-engineering.cortex.tracing-cortex-with-jaeger-or-opentelemetry
name: tracing-cortex-with-jaeger-or-opentelemetry
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [tracing, jaeger, opentelemetry, sampling, troubleshooting]
level: practitioner
status: docs-checked
description: "Send Cortex traces to Jaeger or OpenTelemetry, including the environment variables and which components should sample."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/guides/tracing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Cortex can use Jaeger or OpenTelemetry for distributed tracing.

Jaeger: you need a Jaeger deployment (all-in-one or agent, collector and query). Configure two things:

1. Set `JAEGER_AGENT_HOST` in every component to point at the Jaeger agent (default `localhost`).
2. Enable sampling. The ingester and ruler start traces themselves and should have sampling enabled explicitly. For the distributor and query frontend, sampling can be enabled in Cortex or in an upstream front door service.

Set `JAEGER_SAMPLER_MANAGER_HOST_PORT` for remote sampling, or `JAEGER_SAMPLER_TYPE` and `JAEGER_SAMPLER_PARAM` for manual sampling. Each component must have either `JAEGER_AGENT_HOST` or `JAEGER_SAMPLER_MANAGER_HOST_PORT` set for Jaeger to be enabled, even if you intend to use the defaults. The full variable list is in the Jaeger Go client documentation.

OpenTelemetry: send traces to an OpenTelemetry Collector and configure it in the tracing section of the configuration file. Cortex keeps Jaeger support for backward compatibility and has not fully migrated from OpenTracing to OpenTelemetry; it uses the OpenTracing bridge.

## Checked

2026-11-04. Claims were read against the Cortex docs page: Tracing guide (see sources). Removed filler and unconfirmed wording.

Method: documentation only; no commands were run.
