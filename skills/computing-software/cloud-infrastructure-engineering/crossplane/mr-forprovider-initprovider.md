---
id: computing-software.cloud-infrastructure-engineering.crossplane.mr-forprovider-initprovider
name: mr-forprovider-initprovider
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [managed-resource, forprovider, initprovider, late-initialize, immutable]
level: practitioner
status: docs-checked
description: "How forProvider, initProvider, late initialization and immutable fields behave on a managed resource."
sources:
  - https://docs.crossplane.io/latest/managed-resources/managed-resources/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`spec.forProvider` maps to the external resource's parameters and is the source of truth. Crossplane reverts out-of-band changes (for example from a cloud console) back to it.

`spec.initProvider` holds values applied only at creation. Crossplane ignores later changes to those external fields, which suits settings another system mutates, such as an autoscaling node group:

```yaml
spec:
  managementPolicies: ["Observe", "Create", "Update", "Delete"]
  initProvider:
    scalingConfig:
      desiredSize: 1
  forProvider:
    scalingConfig:
      maxSize: 4
      minSize: 1
```

Late initialization: fields you omit from `forProvider` are populated with values the provider assigned (for example `availabilityZone`). Remove `LateInitialize` from `managementPolicies` to turn that off. Crossplane recommends configuring `managementPolicies` without `LateInitialize` to avoid conflicts with `initProvider` settings. `initProvider` is a beta feature related to `managementPolicies`.

Immutable fields, such as an RDS Instance `region`: Crossplane lets you edit them but does not apply the change. Unlike Terraform it never deletes and recreates; it deletes an external resource only when you delete the managed resource.

## Checked

2026-11-03. Confirmed against the Crossplane docs (Managed Resources page, docs.crossplane.io/latest): the field names, values, defaults and behaviours stated above. Removed or reworded: the wrong recommendation to keep LateInitialize with initProvider (the page recommends omitting it) and the closing paragraph.

Method: documentation only; no commands were run.
