---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-ui-only-limitation
name: jaeger-ui-only-limitation
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, query-only, jaeger-storage-schema, existing-elasticsearch, otel-exporter-schema]
level: advanced
status: docs-checked
description: "Understand why Jaeger query and UI cannot read traces another exporter wrote into Elasticsearch or ClickHouse."
sources:
  - https://www.jaegertracing.io/docs/2.22/faq/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: avoid an unsupported setup.

Question from the FAQ: traces already go to an Elasticsearch cloud setup via sidecar OpenTelemetry Collectors (index pattern `traces-${date}`); can you run only the Jaeger query service and UI, without the Jaeger collector?

Answer: no, that setup is not supported. Every exporter chooses its own way of storing traces in a database like Elasticsearch or ClickHouse. Jaeger has its own storage implementation, used by both collector and query service, with a database schema specific to Jaeger that may not be compatible with other exporters' schemas.

## Checked

2026-11-08: read the whole FAQ (raw markdown from the jaegertracing/documentation repo, v2/2.22). Confirmed the question and answer. Removed unsupported claims: the config-query.yaml detail and the advice to keep sidecar collectors in front.

Method: documentation only; no commands were run.
