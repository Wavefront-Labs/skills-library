---
id: computing-software.cloud-infrastructure-engineering.observability.pruning-span-attributes-to-cut-trace-volume
name: pruning-span-attributes-to-cut-trace-volume
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [span-attribute-pruning, trace-payload-reduction, observability-cost, attributes-processor, transform-processor, span-limits]
level: practitioner
status: docs-checked
description: "Reduce trace bytes by limiting span attributes and events with SDK span limits and by deleting or truncating attributes in collector processors."
sources: ["https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-limits", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/transformprocessor", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/attributesprocessor"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pruning span attributes

Cut at the SDK (limits) or in the collector (processors). Measure first: compare backend ingest bytes against span
counts before and after.

## SDK span limits (specification)
Span attributes follow the common attribute-limit rules, and SDK spans may also discard links and events beyond
configured limits. Defaults in the specification and the SDK environment variable table:
| Environment variable | Meaning | Default |
|---|---|---|
| `OTEL_SPAN_ATTRIBUTE_VALUE_LENGTH_LIMIT` | max attribute value size | no limit |
| `OTEL_SPAN_ATTRIBUTE_COUNT_LIMIT` | max span attribute count | 128 |
| `OTEL_SPAN_EVENT_COUNT_LIMIT` | max span event count | 128 |
| `OTEL_SPAN_LINK_COUNT_LIMIT` | max span link count | 128 |
The generic `OTEL_ATTRIBUTE_VALUE_LENGTH_LIMIT` and `OTEL_ATTRIBUTE_COUNT_LIMIT` apply to attributes in general.
The SDK should log a message once per span when something is discarded due to a limit, and counts of dropped
attributes, events and links must be available to exporters. Per-event and per-link attribute limits also exist
(`AttributePerEventCountLimit`, `AttributePerLinkCountLimit`, default 128).

## Collector: transform processor
Allowed span-related path prefixes are `resource`, `scope`, `span` and `spanevent`. The README's examples use
`keep_keys`, `limit` and `truncate_all`:
```yaml
processors:
  transform/prune:
    error_mode: ignore
    trace_statements:
      - keep_keys(span.attributes, ["service.name", "service.namespace", "cloud.region"])
      - limit(span.attributes, 100, [])
      - truncate_all(span.attributes, 4096)
```
`ignore` is the default `error_mode` and the recommended one.

## Collector: attributes processor
Actions run in the configured order. `delete` removes an attribute and needs `key` and/or `pattern` (a regex on
attribute names) plus `action: delete`. Actions can be restricted with `include` and `exclude` filters; include is
checked before exclude.
```yaml
processors:
  attributes/drop:
    actions:
      - key: http.request.header.cookie
        action: delete
      - pattern: ^http\.request\.header\..*
        action: delete
```

## Verify
- [ ] Average bytes per span (backend ingest bytes divided by spans) drops as expected.
- [ ] Attributes your on-call queries rely on still arrive.

## Checked
2026-11-09. Confirmed against the specification trace SDK Span Limits section, the SDK environment variable
table (read from raw markdown), the transform processor README (config and basic examples) and the attributes
processor README (actions, delete, include/exclude). Removed unconfirmed claims: lists of usual heavy attributes,
TraceQL and tempo-cli tips, the SDK limit values the old text suggested, processor ordering advice
(memory_limiter before batch), the 2-4 KB stack trace guidance, the interplay with tail sampling and spanmetrics,
and the Java agent sanitizer flag.
Method: docs-checked 2026-11-09 against the specification trace SDK and environment variable markdown, the transformprocessor README and the attributesprocessor README; documentation only, no commands run.
