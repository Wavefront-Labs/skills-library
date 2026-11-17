---
id: computing-software.devops-ci-cd.flux.helmrelease-post-renderers
name: helmrelease-post-renderers
category: computing-software
field: devops-ci-cd
product: flux
tags: [helmrelease, postrenderers, kustomize-patches, images, chart-customization]
level: advanced
status: docs-checked
description: "Patch rendered chart manifests and override images in a HelmRelease with kustomize post renderers."
sources:
  - https://fluxcd.io/flux/components/helm/helmreleases/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`.spec.postRenderers` modifies chart output without forking the chart. Built-in Kustomize directives are `kustomize.patches` and `kustomize.images`. Renderers run in the order listed and are persisted by Helm into the release manifest in storage.

```yaml
spec:
  postRenderers:
    - kustomize:
        patches:
          - target:
              version: v1
              kind: Deployment
              name: metrics-server
            patch: |
              - op: add
                path: /metadata/labels/environment
                value: production
        images:
          - name: docker.io/bitnami/metrics-server
            newName: docker.io/bitnami/metrics-server
            newTag: 0.4.1-debian-10-r54
```

Limitation: the reference notes that Helm currently prevents post renderers from being applied to chart hooks. `.spec.postRenderStrategy` sets how hooks are sent to post-renderers: `nohooks` (Helm 3 behaviour), `combined` (hooks and templates in one stream) or `separate`; it defaults to `combined`, or `nohooks` when the `UseHelm3Defaults` feature gate is enabled.

The rendered manifest stored for the release can be read with `helm get manifest RELEASE_NAME -n STORAGE_NAMESPACE`.

## Checked

2026-11-03. Read the HelmRelease reference (fluxcd.io/flux/components/helm/helmreleases/) and the helm get manifest reference (helm.sh/docs/helm/helm_get_manifest/): `.spec.postRenderers` with `kustomize.patches` and `kustomize.images`, order and storage persistence, the hooks limitation and `.spec.postRenderStrategy`. Removed unsupported claims about patch types and when to prefer post renderers.

Method: documentation only; no commands were run.
