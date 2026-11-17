---
id: computing-software.devops-ci-cd.argocd-image-updater.kustomize-targets-and-force-update
name: kustomize-targets-and-force-update
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, kustomize, manifest-targets, force-update, kustomize-edit-set-image, image-override, custom-resources]
level: practitioner
status: docs-checked
description: "Swap or follow images in Kustomize apps with manifestTargets.kustomize.name, and use forceUpdate for images not yet running, such as custom resources and PodTemplates."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/images.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/migration.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/index.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/update.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Kustomize targets and forceUpdate

To use an image from another registry (or a different image) than the manifests, set `manifestTargets.kustomize.name` to the original image name; `imageName` is the image to update to:

```yaml
images:
  - alias: "argocd"
    imageName: "ghcr.io/argoproj/argocd:latest"
    manifestTargets:
      kustomize:
        name: "quay.io/argoproj/argocd"
```

This equals `kustomize edit set image quay.io/argoproj/argocd=ghcr.io/argoproj/argocd`. It replaces the old annotation `<alias>.kustomize.image-name`.

forceUpdate. By default an image is only updated if it is actually used, meaning present in the Application's status. The check is strict on the full name including registry (`docker.io/some/image` differs from `quay.io/some/image`). Force it for custom resources, PodTemplates that create no container, or when the overriding image is not running yet:

```yaml
images:
  - alias: "argocd"
    imageName: "ghcr.io/argoproj/argocd:latest"
    commonUpdateSettings:
      forceUpdate: true
    manifestTargets:
      kustomize:
        name: "quay.io/argoproj/argocd"
```

`forceUpdate` defaults to `false`. With git write-back, `writeBackTarget: "kustomization"` commits the override into the Kustomization file.

Gotcha in v1.4.0 CRDs: earlier CRDs stored `forceUpdate: false` and `updateStrategy: semver` explicitly, blocking inheritance; remove them from old resources.

## Checked

2026-11-04. Confirmed against images.md (Custom images with Kustomize, forceUpdate, defaults), migration.md (old kustomize.image-name annotation), update.md (strict full-name check) and the docs index page (v1.4.0 CRD inheritance warning).

Method: documentation only; no commands were run.
