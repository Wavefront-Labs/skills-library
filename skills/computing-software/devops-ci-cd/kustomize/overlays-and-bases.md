---
id: computing-software.devops-ci-cd.kustomize.overlays-and-bases
name: overlays-and-bases
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [overlay, base, layout, environments]
level: intro
status: docs-checked
description: "Structure a base kustomization shared by dev and prod overlays that add their own prefixes, patches and settings."
sources:
  - https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/
  - https://kubectl.docs.kubernetes.io/references/kustomize/glossary/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A base is a directory with a kustomization.yaml containing resources and associated customization. It can be a local directory or a directory from a remote repo, as long as a kustomization.yaml is present inside. An overlay is a directory with a kustomization.yaml that refers to other kustomization directories as its bases. A base has no knowledge of an overlay and can be used in multiple overlays. An overlay may refer to multiple bases, combining all their resources, and can apply customizations on top.

The task page's example, with `base/deployment.yaml` and `base/service.yaml` created beforehand:

```yaml
# base/kustomization.yaml
resources:
- deployment.yaml
- service.yaml
```

```yaml
# dev/kustomization.yaml
resources:
- ../base
namePrefix: dev-
```

```yaml
# prod/kustomization.yaml
resources:
- ../base
namePrefix: prod-
```

The glossary describes the common layout: a `base` directory beside `overlays/dev`, `overlays/staging` and `overlays/prod`, each overlay holding its own kustomization.yaml and patch.yaml. An overlay is unusable without its bases, and may itself act as a base to another overlay.

Dependency rule from the glossary: if kustomization A depends on B, B may not contain A and B may not depend on A, even transitively. A may contain B, but it might be simplest to have A depend directly on B's resources and absorb B into A.

The glossary builds an overlay with `kustomize build <overlay directory>` piped to `kubectl apply -f -`; `kubectl kustomize <directory>` also views a kustomization directory.

## Checked

2026-11-08: confirmed against the Kubernetes kustomize task page (Bases and Overlays section, read in full) and the kustomize glossary page (base, overlay, root, build example). Removed nothing substantive; added the glossary's build example in place of the unsourced one-liner.

Method: documentation only; no commands were run.
