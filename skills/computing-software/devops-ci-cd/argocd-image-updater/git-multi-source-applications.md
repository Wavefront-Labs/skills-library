---
id: computing-software.devops-ci-cd.argocd-image-updater.git-multi-source-applications
name: git-multi-source-applications
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, multi-source, applicationset, source-types, kustomize-source, helm-source, write-back-target]
level: advanced
status: docs-checked
description: "Write back to the right source in a multi-source Application mixing Kustomize, Helm and plugin sources, using writeBackTarget and Status.SourceTypes detection."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/update-methods.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Multi-source Applications

Argo CD multi-source Applications (and ApplicationSets) list several sources, commonly your own Kustomize workload plus third-party Helm charts. Image Updater picks the correct write-back source from the `writeBackTarget` you configure and the source type detected from `Status.SourceTypes`; the other sources are left untouched.

ApplicationSet template example:

```yaml
spec:
  writeBackConfig:
    method: "git"
    gitConfig:
      writeBackTarget: "kustomization"  # targets the Kustomize git source only
```

With sources such as a Git path `./deployments/myapp/overlays/staging`, a Helm chart `redis` from `registry-1.docker.io/bitnamicharts`, and a `ref: values` source, only the first is written to.

How the Kustomize source is found:

1. a source with an explicit `kustomize:` spec block
2. otherwise `Status.SourceTypes` index alignment, because Argo CD records the detected type for every source, so an implicit Kustomize source (auto-detected from `kustomization.yaml`) is still identified

So you do not need to add `kustomize: {}` to the source.

Equivalent annotation form on an ApplicationSet template:

```yaml
argocd-image-updater.argoproj.io/write-back-method: git
argocd-image-updater.argoproj.io/write-back-target: kustomization
```

## Checked

2026-11-04. Confirmed against update-methods.md (Multi-Source Applications section: Kustomize plus Helm example, the two-step source lookup, annotation equivalent).

Method: documentation only; no commands were run.
