---
id: computing-software.cloud-infrastructure-engineering.crossplane.xrd-versions-served
name: xrd-versions-served
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [xrd, versions, served, referenceable, breaking-change]
level: advanced
status: docs-checked
description: "Manage XRD versions with served and referenceable, and avoid breaking schema changes."
sources:
  - https://docs.crossplane.io/latest/composition/composite-resource-definitions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each entry in `spec.versions` has a name such as `v1alpha1`, `v1beta1` or `v1`, and its own schema. Follow Kubernetes API versioning conventions.

```yaml
versions:
- name: v1alpha1
  served: true
  referenceable: true
```

- `served: true` lets XRs use that version. Kubernetes rejects XRs using a version with `served: false`; flipping it is a good way to find users of an old schema before you delete it.
- `referenceable: true` marks the version Compositions use. Only one version can be referenceable. Changing it means updating `compositeTypeRef.apiVersion` in every Composition for that XRD.

A new version may add new optional fields. A new required field, or any change to an existing field, is a breaking change and needs a conversion webhook. Crossplane recommends shipping breaking changes as a brand new XRD.

Schema changes only take effect after the Crossplane pod restarts.

## Checked

2026-11-03. Confirmed against the Crossplane docs (Composite Resource Definitions page, docs.crossplane.io/latest): the field names, values, defaults and behaviours stated above. Removed or reworded: the step-by-step retirement plan.

Method: documentation only; no commands were run.
