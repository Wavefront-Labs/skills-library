---
id: computing-software.cloud-infrastructure-engineering.crossplane.pt-patch-types
name: pt-patch-types
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [function-patch-and-transform, patch, patchset, fromcompositefieldpath]
level: practitioner
status: docs-checked
description: "Use the function-patch-and-transform patch types, PatchSets and status-based patching between resources."
sources:
  - https://docs.crossplane.io/latest/guides/function-patch-and-transform/
  - https://docs.crossplane.io/latest/composition/compositions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Resources in the `Resources` input have a `name`, a `base` (a normal manifest) and `patches`. Each patch has a `type`, `fromFieldPath` and `toFieldPath`. Field paths are JSONPath subsets such as `spec.desiredRegion`, `spec.resourceRefs[0].name` or `metadata.labels["patchLabel"]`.

Patch types:

- `FromCompositeFieldPath`: XR to composed resource.
- `ToCompositeFieldPath`: composed resource to XR.
- `CombineFromComposite` / `CombineToComposite`: several fields into one.
- `FromEnvironmentFieldPath` / `ToEnvironmentFieldPath`, and `CombineFromEnvironment` / `CombineToEnvironment`: the in-memory environment.
- `PatchSet`: apply a reusable `patchSets` entry by `patchSetName`.

A combine patch uses `combine.variables` (a list of `fromFieldPath`), `strategy: string` and `string.fmt`, for example `my-resource-%s-%s`.

PatchSets cannot nest, and transforms and policies inside them are ignored.

The function cannot patch directly between two composed resources. Instead write to a custom XR status field with `ToCompositeFieldPath`, declared in the XRD schema, and read it with `FromCompositeFieldPath` in the other resource.

Test patches locally with `crossplane composition render`, which prints the composed resources with patches applied.

## Checked

2026-11-03. Confirmed against the Crossplane docs (Function Patch and Transform guide and Compositions page (crossplane composition render), docs.crossplane.io/latest): the field names, values, defaults and behaviours stated above. Removed or reworded: nothing.

Method: documentation only; no commands were run.
