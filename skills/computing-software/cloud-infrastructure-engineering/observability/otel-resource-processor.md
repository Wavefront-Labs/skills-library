---
id: computing-software.cloud-infrastructure-engineering.observability.otel-resource-processor
name: otel-resource-processor
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [resource-processor-config, transforming-telemetry, resource-attributes, collector-config, deployment-environment-attribute]
level: practitioner
status: docs-checked
description: "Add, overwrite, delete or hash resource attributes in the collector with the resource processor (insert, update, upsert, delete, hash, extract); superseded by transform."
sources: ["https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/resourceprocessor", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/attributesprocessor", "https://opentelemetry.io/docs/specs/semconv/resource/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource processor

Applies attribute actions to **resource** attributes (shared by all spans/metrics/logs of a resource). Same action syntax as the attributes processor. The README marks this component as superseded by the `transform` processor and says to migrate to it; see the transform skills for the OTTL `resource` context.

```yaml
processors:
  resource/env:
    attributes:
      - {key: deployment.environment.name, value: prod, action: upsert}
      - {key: cloud.region, value: eu-west-1, action: insert}        # only if missing
      - {key: service.namespace, from_attribute: k8s.namespace.name, action: insert}
      - {key: host.ip, action: delete}
      - {key: user.email, action: hash}
```
| Action | Effect |
|---|---|
| `insert` | add if absent |
| `update` | change if present |
| `upsert` | insert or update |
| `delete` | remove (also `pattern` regex for keys) |
| `hash` | SHA-256 hash of the value (per the resource processor README) |
| `extract` | regex named groups into new attributes |

## Typical uses
- Stamp environment/cluster on everything from a collector tier.
- Remove resource attributes you do not want sent downstream.
- Copy a value to a new key with `from_attribute`, or use `default_value` when the source is missing.

## Order
Actions run in the order listed. Place the processor after any processor that creates the attributes you want to change.

## Gotchas
- Changing or deleting resource attributes changes what downstream queries can filter on; check dashboards and alerts that use them.
- For conditional logic use the transform processor with OTTL in the `resource` context.

## Verify
- [ ] Debug exporter shows the attributes on the Resource section, not on each span.

## Checked

2026-10-24. OpenTelemetry Collector contrib resource processor README and attributes processor README (main branch). Confirmed: supported actions (insert, update, upsert, delete, hash, extract), `default_value`, `from_attribute` and `from_context`, the README note that the component is superseded by transform, and that the README states SHA-256 for hash. Removed `convert` (not listed for this processor) and unconfirmed claims about pipeline order and Prometheus.

Method: documentation only; no commands were run.
