---
id: computing-software.cloud-infrastructure-engineering.crossplane.xr-composition-selection
name: xr-composition-selection
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [composite-resource, compositionref, selector, update-policy]
level: practitioner
status: docs-checked
description: "Choose which Composition or revision a composite resource uses with compositionRef, selectors and update policy."
sources:
  - https://docs.crossplane.io/latest/composition/composite-resources/
  - https://docs.crossplane.io/latest/composition/composite-resource-definitions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Crossplane picks the Composition whose `compositeTypeRef` matches the XR's group and kind. Under `spec.crossplane` on the XR you can steer the choice:

```yaml
spec:
  crossplane:
    compositionRef:
      name: my-other-composition
```

- `compositionRef.name` selects a Composition by name.
- `compositionSelector.matchLabels` selects by Composition labels, for example `environment: production`.
- `compositionUpdatePolicy` is `Automatic` (default, always use the latest revision) or `Manual`.
- `compositionRevisionRef.name` pins a specific CompositionRevision; get names with `kubectl get compositionrevision`.
- `compositionRevisionSelector.matchLabels` picks a revision by label, for example `channel: dev`.

The chosen Composition must allow the XR via `compositeTypeRef`.

Verify with `kubectl get composite`, which shows SYNCED, READY and COMPOSITION, or `kubectl describe composite NAME` to see Composition Ref, Composition Revision Ref and the Resource Refs of composed resources.

Composed resources get the label `crossplane.io/composite` set to the XR name, so you can list everything an XR created.

If more than one Composition references the XRD and the XR does not choose, the XRD's `defaultCompositionRef` supplies the default.

## Checked

2026-11-03. Confirmed against the Crossplane docs (Composite Resources page and Composite Resource Definitions page, docs.crossplane.io/latest): the field names, values, defaults and behaviours stated above. Removed or reworded: the random-selection and change-compositionRef claims.

Method: documentation only; no commands were run.
