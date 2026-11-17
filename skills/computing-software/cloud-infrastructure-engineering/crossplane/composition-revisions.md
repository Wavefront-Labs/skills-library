---
id: computing-software.cloud-infrastructure-engineering.crossplane.composition-revisions
name: composition-revisions
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [composition-revision, canary, rollback, update-policy, labels]
level: advanced
status: docs-checked
description: "Use CompositionRevisions to canary Composition changes and roll back individual XRs."
sources:
  - https://docs.crossplane.io/latest/composition/composition-revisions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every edit to a Composition creates an immutable `CompositionRevision` with an increasing revision number. XRs gain `spec.crossplane.compositionRevisionRef` and `spec.crossplane.compositionUpdatePolicy`.

List revisions:

```shell
kubectl get compositionrevision -l crossplane.io/composition-name=example
```

Policies:

- `Automatic` (default): the XR follows the latest revision, so every XR changes immediately when you edit the Composition.
- `Manual`: the XR picks the latest revision at creation and keeps it until you edit `compositionRevisionRef`.

```yaml
spec:
  crossplane:
    compositionUpdatePolicy: Manual
    compositionRef:
      name: example
    compositionRevisionRef:
      name: example-18pdg
```

Crossplane sets `compositionRevisionRef` at creation under either policy.

Revisions copy the Composition's labels, for example `channel: dev`. Use `compositionRevisionSelector.matchLabels` with `Automatic` to follow the latest revision carrying a label. An XR whose selector matches no revision shows no REVISION.

Inspect: `kubectl get compositionrevisions -o custom-columns=NAME:.metadata.name,REVISION:.spec.revision,CHANNEL:.metadata.labels.channel`.

To move individual XRs to an older revision, set the XR to `Manual` and edit `compositionRevisionRef` to name that revision.

## Checked

2026-11-03. Confirmed against the Crossplane docs (Composition Revisions page, docs.crossplane.io/latest): the field names, values, defaults and behaviours stated above. Removed or reworded: the claim that the suffix is random, the diff-two-revisions advice, and the rollback wording.

Method: documentation only; no commands were run.
