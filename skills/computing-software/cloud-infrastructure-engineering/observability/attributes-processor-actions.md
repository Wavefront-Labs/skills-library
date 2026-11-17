---
id: computing-software.cloud-infrastructure-engineering.observability.attributes-processor-actions
name: attributes-processor-actions
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [attributes-processor-actions, hash-attribute, extract-attribute-regex, transforming-telemetry, otel-collector]
level: practitioner
status: docs-checked
description: "Use the OTel Collector attributes processor: insert, update, upsert, delete, hash, extract and convert actions, include/exclude matching, and copying request metadata."
sources: ["https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/attributesprocessor", "https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/internal/coreinternal/attraction/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# attributes processor actions

Modifies the attributes of a span, log or metric. Actions run in the order listed. For resource attributes use the
`resource` processor.

```yaml
processors:
  attributes/clean:
    actions:
      - {key: deployment.environment.name, value: prod, action: insert}        # only if missing
      - {key: http.route, from_attribute: http.target, action: insert}         # copy
      - {key: team, value: payments, action: upsert}                           # insert or overwrite
      - {key: db.query.text, action: delete}
      - {pattern: ^http\.request\.header\..*, action: delete}                  # delete by regex on key
      - {key: user.email, action: hash}                                        # hash of the value (algorithm per release, see Notes)
      - {key: http.url, pattern: ^https?://[^/]+/api/(?P<api_version>v\d+)/, action: extract}   # creates api_version
      - {key: http.response.status_code, action: convert, converted_type: int}
      - {key: tenant, from_context: metadata.x-tenant-id, action: upsert}      # from receiver metadata (needs include_metadata: true)
    include:
      match_type: regexp
      services: ["checkout|payments"]
      span_names: ["^GET .*"]
    exclude:
      match_type: strict
      attributes: [{key: debug, value: "true"}]
```

## Notes
- `insert` never overwrites, `update` only overwrites existing, `upsert` does both.
- `extract` uses named capture groups; each group becomes an attribute (overwrites existing ones of that name).
- `hash` keeps joinability (same input -> same hash) while hiding raw values. The attributes README documents SHA1 while the resource processor README documents SHA-256, so confirm the
  algorithm for the release you run. A hash of a
  low-entropy value such as an email can be brute-forced, so treat it as pseudonymised, not anonymous, or drop it.
- `from_context: metadata.<header>` needs `include_metadata: true` on the receiver; `auth.<field>` reads data set by the
  server authenticator; `client.address` gives the client address. Multiple values are joined with `;`. If the key is
  missing no action is taken, unless `default_value` is set. `default_value` applies to insert, update and upsert.
- `include`/`exclude` filters which items the actions apply to; `match_type` (`strict` or `regexp`) is required and `include`
  is checked before `exclude`. Spans accept `services`, `span_names`, `span_kinds`, `attributes`, `resources`, `libraries`;
  logs accept `log_bodies`, `log_severity_texts`, `log_severity_number` (`min`, `match_undefined`), `attributes`, `resources`,
  `libraries`; metrics accept only `metric_names` and `resources`.

## When to use transform (OTTL) instead
Conditional logic, OTTL functions, resource or scope context, or metric renames. The attributes processor is the
simpler choice for static key operations.

## Verify
Run a test pipeline with the `debug` exporter (`verbosity: detailed`) and compare the attributes before and after the processor.

## Checked

2026-10-24. OpenTelemetry Collector contrib attributes processor README (main branch). Confirmed: the action list and required fields (insert, update, upsert, delete, hash, extract, convert; `converted_type` int, double or string), `hash` documented as SHA1 (the resource README says SHA-256), `pattern` accepted by delete and hash, `extract` needs named groups and overwrites existing targets, `from_context` prefixes `metadata.` and `auth.` plus `client.address`, multi-value join with `;`, `default_value`, and the include/exclude fields per signal.

Method: documentation only; no commands were run.
