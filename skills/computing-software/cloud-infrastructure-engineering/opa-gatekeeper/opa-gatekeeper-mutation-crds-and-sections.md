---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-mutation-crds-and-sections
name: opa-gatekeeper-mutation-crds-and-sections
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, mutation, assign, assignmetadata, modifyset, assignimage, mutators]
level: practitioner
status: docs-checked
description: "Choose between the Gatekeeper mutator CRDs Assign, AssignMetadata, ModifySet and AssignImage, and read their three sections: extent, intent and conditions."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/mutation.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper mutation crds and sections

Mutation (stable since v3.10) changes resources at admission time, using mutators rather than ConstraintTemplates.

- `AssignMetadata`: changes metadata, limited to adding labels or annotations; existing ones cannot be modified.
- `Assign`: any change outside metadata.
- `ModifySet`: adds or removes list entries, such as container args.
- `AssignImage`: changes domain, path or tag of an image string.

Every mutator has three parts:
1. Extent of changes: `applyTo` (required for all except AssignMetadata) and `match`, which selects the resources.
2. Intent: `location` (the path) and `parameters.assign.value`.
3. Conditions: `pathTests` that require a path to exist or not.

```yaml
apiVersion: mutations.gatekeeper.sh/v1
kind: AssignMetadata
metadata:
  name: demo-annotation-owner
spec:
  match:
    scope: Namespaced
    name: nginx-*
    kinds:
      - apiGroups: ["*"]
        kinds: ["Pod"]
  location: "metadata.annotations.owner"
  parameters:
    assign:
      value: "admin"
```

Mutation is separate from validation: the mutators use mutation-specific CRDs under `mutations.gatekeeper.sh` instead of ConstraintTemplate and Constraint, so use validation constraints when you only need deny, warn, dry-run or audit reporting without changing the object. The match criteria and namespace exclusions are shared concepts between the two areas. Metadata rules are stricter than for the rest of the object because changing name or namespace could have unintended consequences, which is why AssignMetadata only adds labels and annotations.

## Checked

2026-11-08: read the whole of website/docs/mutation.md in the Gatekeeper repo. Confirmed the four mutator CRDs, the three sections, the applyTo requirement, the pathTests example and the stricter metadata rules. Removed: the sentence that validation runs on the final object, which that page does not state.

Method: documentation only; no commands were run.
