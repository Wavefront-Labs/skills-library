---
id: computing-software.devops-ci-cd.kustomize.kustomize-build-command
name: kustomize-build-command
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [kustomize, build, hydrate, cli]
level: intro
status: docs-checked
description: "Render a kustomization into final Kubernetes manifests with kustomize build and its --enable-helm, --reorder and load-restrictor flags."
sources:
  - https://kubectl.docs.kubernetes.io/references/kustomize/cmd/build/
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/helmcharts/
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/sortoptions/
  - https://kubectl.docs.kubernetes.io/references/kustomize/cmd/localize/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`kustomize build` is the primary command. It recursively builds (hydrates) the kustomization.yaml you point it to, resulting in a set of Kubernetes resources ready to deploy.

```bash
kustomize build path/to/overlay
kustomize build --enable-helm path/to/overlay
```

Flags mentioned across these docs:

- `--enable-helm` turns on the helm chart inflation generator (`helmCharts`); without it that generator is not enabled.
- `--reorder` is deprecated; use the `sortOptions` field (kustomize v5.0.0+, respected only in the top-level kustomization).
- `--load-restrictor LoadRestrictionsNone` is the flag the localize page names for builds that need load restrictions relaxed; `kustomize localize` fails on a kustomization that requires it.

## Checked

2026-11-08: confirmed against the kustomize build, helmCharts, sortOptions and localize reference pages on kubectl.docs.kubernetes.io, all read in full. Removed the claims that were not on those pages: the kubectl apply and kubectl kustomize notes, the multi-document output remark, the everyday-checks list, and the older `--load_restrictions none` spelling attributed to the glossary (the glossary was not read in full).

Method: documentation only; no commands were run.
