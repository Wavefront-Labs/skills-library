---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.resource-processor
name: resource-processor
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, processors, resource, resource-attributes, environment]
level: practitioner
status: docs-checked
description: "Add, replace or delete resource attributes such as deployment.environment on all telemetry with the resource processor."
sources:
  - https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/resourceprocessor/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The resource processor applies changes to resource attributes, using the attributes processor's actions. The README example inserts the Kubernetes cluster name from another attribute:

```yaml
processors:
  resource/k8s:
    attributes:
      - key: k8s.cluster.name
        from_attribute: k8s-cluster
        action: insert
```

Details from the README:

- Supported actions are `insert`, `update`, `upsert`, `delete`, `hash` (SHA-256) and `extract`.
- Other forms in its examples: `value: "zone-1"` with `upsert` for `cloud.availability_zone`, and `action: delete` for `redundant-attribute`.
- `default_value` supplies a fallback when the source attribute (`from_attribute`) or context value (`from_context`) is missing, for example `region` from `cloud.region` defaulting to `us-east-1`.
- Stability is beta for traces, metrics and logs, and development for profiles.
- Warning (identity conflict): resource attributes are part of a metric stream's identity. Deleting or changing them with `delete`, `update` or `upsert` can merge distinct streams, because the processor does not re-aggregate data points; adding new resource attributes is safe.
- A note says the component is superseded by the transform processor, which you should migrate to.

The attributes processor modifies attributes of a span, log or metric; the resource processor applies the same kind of actions to resource attributes.

## Checked

Method: docs-checked 2026-11-09 against the resourceprocessor README in opentelemetry-collector-contrib (raw markdown).
