---
id: computing-software.cloud-infrastructure-engineering.crossplane.xrd-names-schema
name: xrd-names-schema
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [xrd, schema, openapi, names, required]
level: practitioner
status: docs-checked
description: "Define an XRD's group, names and OpenAPI schema, including required fields and the fields Crossplane reserves."
sources:
  - https://docs.crossplane.io/latest/composition/composite-resource-definitions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An XRD defines the schema of a custom API. It becomes a Kubernetes CRD.

```yaml
apiVersion: apiextensions.crossplane.io/v2
kind: CompositeResourceDefinition
metadata:
  name: mydatabases.example.org
spec:
  scope: Namespaced
  group: example.org
  names:
    kind: XMyDatabase
    plural: mydatabases
```

Rules:

- `metadata.name` must be `<plural>.<group>`.
- You cannot change `group` or `names`; delete and recreate the XRD instead.
- `kind` is UpperCamelCase; Crossplane recommends starting it with `X`. `plural` is lowercase.
- Each version has `schema.openAPIV3Schema`, a structural schema with `spec.properties`.
- Fields are optional by default. Use `required: [region, size]`; `required` applies per object, so nested objects need their own list.
- Crossplane ignores `spec.crossplane`, `status.crossplane` and `status.conditions` in your schema.
- Changing or expanding the schema requires restarting the Crossplane pod to take effect.

Check status with `kubectl get xrd`: `ESTABLISHED` True means the CRD exists. The condition reason `WatchingCompositeResource` is healthy; `TerminatingCompositeResource` means the CRD is being deleted.

## Checked

2026-11-03. Confirmed against the Crossplane docs (Composite Resource Definitions page, docs.crossplane.io/latest): the field names, values, defaults and behaviours stated above. Removed or reworded: the closing advice about deleting every XR.

Method: documentation only; no commands were run.
