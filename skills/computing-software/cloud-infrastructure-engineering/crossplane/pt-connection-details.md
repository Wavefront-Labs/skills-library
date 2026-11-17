---
id: computing-software.cloud-infrastructure-engineering.crossplane.pt-connection-details
name: pt-connection-details
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [function-patch-and-transform, connection-details, secret, writeconnectionsecrettoref]
level: advanced
status: docs-checked
description: "Aggregate composed resource connection details into an XR Secret with function-patch-and-transform."
sources:
  - https://docs.crossplane.io/latest/guides/function-patch-and-transform/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
This function aggregates connection details automatically; unlike other functions it cannot read observed connection details to build a Secret by hand.

Steps:

1. Set `writeConnectionSecretToRef` on each composed resource that produces details.
2. Declare `connectionDetails` on that resource.
3. Choose where the aggregated Secret goes.

```yaml
connectionDetails:
- name: my-username
  type: FromConnectionSecretKey
  fromConnectionSecretKey: username
- name: my-field-secret
  type: FromFieldPath
  fromFieldPath: spec.forProvider.user
- name: my-status-secret
  type: FromValue
  value: "docs.crossplane.io"
```

Only listed details reach the combined Secret. If two resources use the same key name, only one value survives, so give distinct `name`s. A `FromValue` value must be a string.

Secret name and namespace, in priority order:

1. The XR's `spec.writeConnectionSecretToRef` (the XRD schema must include it).
2. The function input's `writeConnectionSecretToRef`, static or with `patches`.
3. Generated: `<xr-name>-connection` in the XR's namespace. Cluster-scoped XRs cannot use this and need option 1 or 2.

In v2 the function composes the Secret as a composed resource. Use go-templating, python or kcl when you need to transform details.

## Checked

2026-11-03. Confirmed against the Crossplane docs (Function Patch and Transform guide, docs.crossplane.io/latest): the field names, values, defaults and behaviours stated above. Removed or reworded: nothing.

Method: documentation only; no commands were run.
