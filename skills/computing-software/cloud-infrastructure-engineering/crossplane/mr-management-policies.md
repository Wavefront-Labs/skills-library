---
id: computing-software.cloud-infrastructure-engineering.crossplane.mr-management-policies
name: mr-management-policies
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [managed-resource, managementpolicies, observe, late-initialize, pause]
level: advanced
status: docs-checked
description: "Limit what Crossplane may do to an external resource with managementPolicies."
sources:
  - https://docs.crossplane.io/latest/managed-resources/managed-resources/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`spec.managementPolicies` is a list controlling Crossplane's permissions. The provider must support it; check the provider docs.

Policies:

- `*` (default): full control.
- `Create`: create the external resource if it does not exist.
- `Observe`: observe only, no changes.
- `Update`: change the external resource when the MR changes.
- `Delete`: delete the external resource when the MR is deleted.
- `LateInitialize`: copy provider-assigned values into `spec.forProvider`.

```yaml
spec:
  managementPolicies: ["Create", "Delete", "Observe"]
```

That example creates and deletes but never updates. Typical combinations:

- Drop `Delete` so deleting the MR leaves the external resource in place.
- Drop `Update` to stop Crossplane changing settings after creation.
- Drop `LateInitialize` to stop importing provider defaults.
- Only `["Observe"]`: Crossplane only observes the resource and changes nothing.

An empty array `[]` pauses the resource, as an alternative to the paused annotation.

Without `Delete`, Crossplane does not delete the external resource when the MR is deleted. The provider determines support for management policies, so check its docs before relying on the field. `managementPolicies` is a beta feature.

## Checked

2026-11-03. Confirmed against the Crossplane docs (Managed Resources page, docs.crossplane.io/latest): the field names, values, defaults and behaviours stated above. Removed or reworded: the deletionPolicy comparison and the claim about unsupported providers.

Method: documentation only; no commands were run.
