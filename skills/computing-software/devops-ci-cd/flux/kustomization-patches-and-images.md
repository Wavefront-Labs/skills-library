---
id: computing-software.devops-ci-cd.flux.kustomization-patches-and-images
name: kustomization-patches-and-images
category: computing-software
field: devops-ci-cd
product: flux
tags: [kustomization, patches, images, strategicmerge, json6902]
level: sme
status: docs-checked
description: "Patch rendered manifests and override image names, tags or digests inline in a Flux Kustomization without editing the base."
sources:
  - https://fluxcd.io/flux/components/kustomize/kustomizations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use `.spec.patches` and `.spec.images` to change what a base produces without forking it.

`.spec.patches` is a list of Kustomize patches. Each item needs `patch` (inline strategic merge or JSON6902 operations) and `target` (selects the resources; can match several, for example by `labelSelector`).

```yaml
spec:
  patches:
    - patch: |-
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: not-used
        spec:
          template:
            metadata:
              annotations:
                cluster-autoscaler.kubernetes.io/safe-to-evict: "true"
      target:
        kind: Deployment
        labelSelector: "app.kubernetes.io/part-of=my-app"
    - patch: |
        - op: add
          path: /spec/template/spec/securityContext
          value:
            runAsUser: 10000
      target:
        kind: Deployment
        name: podinfo
```

`.spec.images` overrides `name`, `newName`, `newTag` or `digest` of container images:

```yaml
spec:
  images:
    - name: podinfo
      newName: my-registry/podinfo
      newTag: v1
```

`.spec.components` (Kustomize components) and `.spec.buildMetadata` (`originAnnotations`, `transformerAnnotations`) are related options.

The first patch above is a strategic merge: its `metadata.name` is a placeholder, because `target` with a `labelSelector` decides which Deployments receive it. The second is JSON6902, with `op`, `path` and `value`, and is aimed at a single Deployment by `name`.

## Checked

2026-11-03. Read the Kustomization reference (fluxcd.io/flux/components/kustomize/kustomizations/): `patches` (strategic merge or JSON6902, `target`, `labelSelector`), `images` (name, tag, digest) and `buildMetadata` values. Removed an unsupported preference sentence.

Method: documentation only; no commands were run.
