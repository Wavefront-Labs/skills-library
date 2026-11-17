---
id: computing-software.cloud-infrastructure-engineering.crossplane.xrd-scope-defaults
name: xrd-scope-defaults
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [xrd, scope, namespaced, default-composition, enforced-composition]
level: practitioner
status: docs-checked
description: "Set XRD scope (Namespaced, Cluster, LegacyCluster) and the default and enforced Composition fields."
sources:
  - https://docs.crossplane.io/latest/composition/composite-resource-definitions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`spec.scope` decides where XRs live:

- `Namespaced` (default in v2): XRs exist in a namespace and can only compose resources in that namespace.
- `Cluster`: XRs are cluster-scoped and can compose resources in any namespace or at cluster scope.
- `LegacyCluster`: cluster-scoped with claim support, for v1 compatibility.

Prefer `Namespaced` for isolation. Use `Cluster` only for platform-level things like RBAC or cluster configuration.

XRD-level defaults for XRs:

```yaml
spec:
  defaultCompositionRef:
    name: myComposition
  defaultCompositionUpdatePolicy: Manual
  enforcedCompositionRef:
    name: myComposition
```

- `defaultCompositionRef` applies when several Compositions match the XRD and the XR does not choose.
- `defaultCompositionUpdatePolicy` defaults to `Automatic`; `Manual` stops XRs following new revisions.
- `enforcedCompositionRef` forces every XR to use that Composition.

An XRD can also expose the Kubernetes `scale` subresource, so `kubectl scale`, the HPA and KEDA can drive the XR.

Check an XRD with `kubectl get xrd`.

## Checked

2026-11-03. Confirmed against the Crossplane docs (Composite Resource Definitions page, docs.crossplane.io/latest): the field names, values, defaults and behaviours stated above. Removed or reworded: the closing advice on Manual and enforcedCompositionRef.

Method: documentation only; no commands were run.
