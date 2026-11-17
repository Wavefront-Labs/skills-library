---
id: computing-software.cloud-infrastructure-engineering.observability.span-processor-renaming
name: span-processor-renaming
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [span-processor-rename, span-name-from-attributes, transforming-telemetry, span-naming, otel-collector]
level: practitioner
status: docs-checked
description: "Fix span names in the collector: span processor from_attributes and to_attributes rules, extracting IDs from names into attributes, setting status, and OTTL alternatives."
sources: ["https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/spanprocessor", "https://opentelemetry.io/docs/specs/otel/trace/api/#span"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Span processor renaming

High-cardinality span names (`GET /users/8812/orders`) break span metrics, service graphs and search. Fix in the app
first (route template); use the collector when you cannot.

## Name from attributes
```yaml
processors:
  span/db-name:
    name:
      from_attributes: [db.operation.name, db.collection.name]
      separator: " "                 # -> "SELECT orders"
    include:
      match_type: strict
      attributes: [{key: db.system.name}]
```
`from_attributes` is required and `separator` optional. The README notes the span processor must come after the `attributes`
processor if renaming depends on attributes that processor changes. The README marks the span processor as superseded by
`transform`.

## Extract IDs from the name into attributes (and template the name)
```yaml
processors:
  span/templatize:
    name:
      to_attributes:
        rules:
          - ^/api/v1/users/(?P<user_id>\d+)/orders$
          - ^/api/v1/documents/(?P<document_id>[0-9a-f-]{36})$
        break_after_match: true
```
Result: name `/api/v1/users/{user_id}/orders`, attribute `user_id=8812`. Rules apply in the listed order and each later rule sees
the name as modified by the previous one unless `break_after_match: true` (default false). `keep_original_name: true` (default
false) adds the attributes but leaves the name unchanged. Existing attributes with the same names are overwritten.

## Set status
```yaml
processors:
  span/status:
    status: {code: Error, description: "upstream 5xx"}      # code: Unset, Error or Ok; description only with Error
    include: {match_type: strict, attributes: [{key: http.response.status_code, value: 503}]}
```

## OTTL alternative (more flexible)
```yaml
transform/spans:
  trace_statements:
    - context: span
      statements:
        - set(span.name, Concat([span.attributes["http.request.method"], span.attributes["http.route"]], " ")) where span.attributes["http.route"] != nil and span.kind == SPAN_KIND_SERVER
        - replace_pattern(span.name, "/\\d+", "/{id}")
```

## Gotchas
- Rename before `spanmetrics`/`servicegraph` connectors and before tail sampling policies that match names.
- Renaming in the collector hides the bug in the SDK from other consumers (direct exporters); fix upstream too.

## Checked

2026-10-24. OpenTelemetry Collector contrib span processor README (main branch). Confirmed: `name.from_attributes` and `separator`, `to_attributes.rules` with named groups, `break_after_match` and `keep_original_name` defaults, `status.code` values and description restriction, include/exclude support, and the superseded-by-transform note. Removed an unconfirmed claim that a missing attribute leaves the name unchanged, and a span_kinds example whose value format the README does not document. The OTTL alternative was checked against the OTTL functions reference (`set`, `Concat(vals[], delimiter)`, `replace_pattern(target, regex_pattern, replacement)`), the span context paths (`span.name`, `span.attributes`, `span.kind`, `SPAN_KIND_*` enums) and the transform processor `trace_statements` with `context` form; paths are now written with the `span.` prefix.

Method: documentation only; no commands were run.
