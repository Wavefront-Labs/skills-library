---
id: computing-software.devops-ci-cd.flux.kustomization-ignore-drift-rules
name: kustomization-ignore-drift-rules
category: computing-software
field: devops-ci-cd
product: flux
tags: [kustomization, ignore, drift, jsonpointer, hpa]
level: advanced
status: docs-checked
description: "Let other controllers own specific fields by listing JSON Pointer paths in spec.ignore with a scoped target."
sources:
  - https://fluxcd.io/flux/components/kustomize/kustomizations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`.spec.ignore` lets external controllers or tools manage certain fields without kustomize-controller reverting them during drift correction. Each item has:

- `paths` (required): JSON Pointer (RFC 6901) paths excluded from drift detection, such as `/spec/replicas`.
- `target` (optional): a selector scoping the rule to certain resources.

Omitting `target` makes the rule match every object the Kustomization manages, so always scope it unless you really mean that.

```yaml
spec:
  ignore:
    - paths: ["/spec/replicas"]
      target:
        kind: Deployment
        name: podinfo
```

This is the typical fix for a HorizontalPodAutoscaler fighting Flux over replica count.

Related: the annotation `kustomize.toolkit.fluxcd.io/ssa: Merge` keeps non-overlapping fields from other managers on one object.

After changing the rules, run `flux reconcile kustomization NAME`.

## Checked

2026-11-03. Read the Kustomization reference (fluxcd.io/flux/components/kustomize/kustomizations/): `.spec.ignore` paths and target, the default of matching all resources, and the Merge annotation. Removed unsupported alternative and narrowness advice.

Method: documentation only; no commands were run.
