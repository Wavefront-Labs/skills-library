---
id: computing-software.cloud-infrastructure-engineering.crossplane.pt-patch-policies
name: pt-patch-policies
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [function-patch-and-transform, patch-policy, required, merge, tofieldpath]
level: practitioner
status: docs-checked
description: "Control missing source fields and merge behavior of patches with fromFieldPath and toFieldPath policies."
sources:
  - https://docs.crossplane.io/latest/guides/function-patch-and-transform/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Add `policy` to a patch:

```yaml
patches:
- type: FromCompositeFieldPath
  fromFieldPath: spec.desiredRegion
  toFieldPath: metadata.annotations["eu"]
  policy:
    fromFieldPath: Required
    toFieldPath: MergeObjectsAppendArrays
```

`fromFieldPath`:

- `Optional` (default): Crossplane skips the patch when the source field is missing.
- `Required`: the composite resource reports an error. Use this to debug a patch that silently does nothing.

`toFieldPath`:

- `Replace` (default): overwrite the destination.
- `MergeObjects`: recursive merge, keeping conflicting existing keys.
- `ForceMergeObjects`: recursive merge, replacing conflicting keys.
- `MergeObjectsAppendArrays`: like MergeObjects but appends arrays.
- `ForceMergeObjectsAppendArrays`: like ForceMergeObjects but appends arrays.

Policies inside a PatchSet are ignored, so set them on the patches that use it.

Debugging tip: temporarily set `fromFieldPath: Required` on a patch that seems to do nothing. If the XR then reports an error, the source field does not exist at that path.

Policies sit inside the patch object next to `type`, `fromFieldPath` and `toFieldPath`.

## Checked

2026-11-03. Confirmed against the Crossplane docs (Function Patch and Transform guide, docs.crossplane.io/latest): the field names, values, defaults and behaviours stated above. Removed or reworded: the claim that the error names the path, the example paths, and the by-destination-type advice (not on the page).

Method: documentation only; no commands were run.
