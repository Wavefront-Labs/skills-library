---
id: computing-software.devops-ci-cd.argocd-image-updater.git-write-back-targets
name: git-write-back-targets
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, write-back-target, helmvalues, kustomization, kustomize-edit-set-image, helm-values, argocd-source-file]
level: advanced
status: docs-checked
description: "Pick the git write-back target: the default .argocd-source file, kustomization for kustomize edit set image behaviour, or helmvalues with a relative or absolute values path."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/update-methods.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/applications.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Git write-back targets

`writeBackConfig.gitConfig.writeBackTarget` selects what file gets committed.

Default: `.argocd-source-<appName>.yaml` (source parameter overrides).

Kustomize: `writeBackTarget: "kustomization"` commits changes as if you ran `kustomize edit set image`. Point at a directory (not a file) either relative to the Application source path or absolute from the repository root:

```yaml
gitConfig:
  writeBackTarget: "kustomization:../../base"      # path relative to spec.source.path
  # writeBackTarget: "kustomization:/config/overlays/bar"   # absolute starts with /
```

Helm: `writeBackTarget: "helmvalues:<path to values file>"` commits to the values file used for rendering, for example `helmvalues:../../values.yaml` or `helmvalues:/helm/config/test-values.yaml`. The values filename must be given.

Plugin applications using `manifestTargets.plugin` automatically use the default target, so do not set `helmvalues` or `kustomization` for them. Plugin apps that consume values files (such as helmfile) can use `manifestTargets.helm` or `.kustomize` with the git method and an explicit target:

| Target | Written |
|---|---|
| `kustomization[:path]` | `kustomization.yaml` image override |
| `helmvalues:path` | Helm values YAML |
| none | `.argocd-source-<app>.yaml` |

For such plugin apps the `argocd` method is unavailable.

## Checked

2026-11-04. Confirmed against update-methods.md (Git Write-Back Target: kustomization and helmvalues forms, relative and absolute paths, plugin default target) and applications.md (plugin source type table and the argocd-method note); images.md warns against helmvalues or kustomization with manifestTargets.plugin.

Method: documentation only; no commands were run.
