---
id: computing-software.cloud-infrastructure-engineering.crossplane.usage-protection-ordering
name: usage-protection-ordering
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [usage, clusterusage, deletion-protection, deletion-ordering, replaydeletion]
level: advanced
status: docs-checked
description: "Block deletion of in-use resources and order deletions with Usage objects."
sources:
  - https://docs.crossplane.io/latest/managed-resources/usages/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A `Usage` has a mandatory `spec.of` (the protected resource). The `reason` and `by` (the resource using it) fields are optional, but at least one of them must be set.

Deletion protection, with `of` only:

```yaml
apiVersion: protection.crossplane.io/v1beta1
kind: Usage
metadata:
  namespace: default
  name: protect-production-database
spec:
  of:
    apiVersion: rds.aws.m.upbound.io/v1beta1
    kind: Instance
    resourceRef:
      name: my-database
  reason: "Production Database - should never be deleted!"
```

Deletion ordering adds `by`: the `of` resource cannot be deleted until the `by` resource is gone.

Details:

- `resourceSelector` (with `matchLabels` and `matchControllerRef`) can replace `resourceRef`. Selectors resolve once; with several matches one is chosen at random, and the name is stored in `resourceRef`.
- `replayDeletion: true` replays a blocked deletion right after the using resource disappears, skipping the garbage collector's long backoff. Useful inside compositions.
- Use `matchControllerRef` in compositions so Usages bind to resources of the same XR.
- Put `namespace` in the `of` ref to reference another namespace.
- `ClusterUsage` protects cluster-scoped resources.
- Usages are beta and on by default. Disable them with `--enable-usages=false`.

## Checked

Required fields, both examples, selector resolution, replayDeletion, composition use, cross-namespace `of` and ClusterUsage confirmed on the Usages page. The at-least-one rule was misstated (it applies to `reason` and `by`, not `of`); corrected.

Method: docs-checked 2026-11-09 against the raw Usages page (docs repo, current content folder), read in full.
