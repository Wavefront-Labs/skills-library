---
id: computing-software.devops-ci-cd.argocd-image-updater.migration-annotations-to-crd
name: migration-annotations-to-crd
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, migration, annotations-to-crd, legacy-annotations, v1-crd, image-list, annotation-mapping]
level: practitioner
status: docs-checked
description: "Convert legacy argocd-image-updater annotations on Applications into an ImageUpdater CR: image-list, strategy, tags, pull-secret, platforms, Helm, Kustomize and write-back."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/migration.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Migrating annotations to the ImageUpdater CRD

v1.0.0 moved configuration from annotations to CRDs; docs for v0.x (for example 0.17.0) hold the legacy form. Mapping:

| Annotation | CR field |
|---|---|
| `image-list: nginx=nginx:1.20,redis=redis:6.2` | `images[]` with `alias` + `imageName` |
| `<alias>.update-strategy: latest` | `commonUpdateSettings.updateStrategy: "newest-build"` |
| `<alias>.allow-tags: regexp:...` | `allowTags: "regexp:..."` (escape backslashes) |
| `<alias>.ignore-tags: latest,dev` | `ignoreTags: ["latest", "dev"]` |
| `<alias>.pull-secret: secret:ns/name#username` | `pullSecret: "secret:ns/name#username"` |
| `<alias>.platforms: linux/amd64,linux/arm64` | `platforms: ["linux/amd64", "linux/arm64"]` |
| `<alias>.helm.image-name` / `image-tag` | `manifestTargets.helm.name` / `tag` |
| `<alias>.kustomize.image-name` | `manifestTargets.kustomize.name` |
| `write-back-method`, `git-repository`, `git-branch`, `write-back-target` | `writeBackConfig.method`, `gitConfig.repository`, `branch`, `writeBackTarget` |

Application selection replaces per-app annotations with `namePattern` globs and label selectors; group many apps in one CR, and shared settings can move to `spec.writeBackConfig` and `commonUpdateSettings`.

Pitfalls:

- the namespace comes from the CR's `metadata.namespace`, not per application
- `platforms` and `ignoreTags` changed from comma-separated strings to arrays
- the renamed strategies: `latest` to `newest-build`, `name` to `alphabetical`

Annotation-templated ApplicationSets can keep annotations with `useAnnotations: true`.

## Checked

2026-11-04. Confirmed against migration.md (step-by-step mappings, common pitfalls), the docs index page (v1.0.0 transition, v0.x docs for legacy form) and applications.md (useAnnotations).

Method: documentation only; no commands were run.
