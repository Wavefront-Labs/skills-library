---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.attributes-processor-actions
name: attributes-processor-actions
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, processors, attributes, insert, update, delete, hash]
level: practitioner
status: docs-checked
description: "Add, change, hash and remove span, log and metric attributes with the attributes processor actions."
sources:
  - https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/attributesprocessor/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The attributes processor modifies attributes of spans, logs and metrics through a list of actions performed in the order written. The README's sample configuration includes an `account_id` insert:

```yaml
processors:
  attributes/example:
    actions:
      - key: account_id
        value: 2245
        action: insert
```

Actions from the README:

- `insert` adds only when the key is absent; `update` changes only when it exists; `upsert` does either.
- `delete` removes a key, and takes `key` and/or a regex `pattern`.
- `hash` replaces the value with a SHA2-256 hash.
- `extract` pulls named regex groups from a key's value into new attributes, overwriting existing ones, and leaves the source key unchanged.
- `convert` changes the type with `converted_type` of `int`, `double` or `string`.
- Insert, update and upsert need a `key` plus one of `value`, `from_attribute`, `from_context` or `default_value`. `from_attribute` does nothing when the source is missing.
- `from_context` reads `metadata.` (gRPC metadata or HTTP headers, needing `include_metadata: true` on the receiver), `auth.` or `client.address`.

The processor also supports `include` and `exclude` filtering by properties such as services, span names, attributes, resources and metric names; `include` is checked before `exclude`. Warning (identity conflict): reducing or changing existing data point attributes can create an identity conflict because the processor does not re-aggregate data points; adding attributes is safe.

The README notes this processor is superseded by `transform`, so prefer that for new work.

## Checked

Method: docs-checked 2026-11-09 against the attributesprocessor README in opentelemetry-collector-contrib (raw markdown).
