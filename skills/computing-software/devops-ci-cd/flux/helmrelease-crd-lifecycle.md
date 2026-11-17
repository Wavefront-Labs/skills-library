---
id: computing-software.devops-ci-cd.flux.helmrelease-crd-lifecycle
name: helmrelease-crd-lifecycle
category: computing-software
field: devops-ci-cd
product: flux
tags: [helmrelease, crds, createreplace, install-crds, upgrade-crds]
level: advanced
status: docs-checked
description: "Opt in to upgrading CRDs shipped in a Helm chart with install.crds and upgrade.crds policies Skip, Create or CreateReplace."
sources:
  - https://fluxcd.io/flux/components/helm/helmreleases/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Helm installs CRDs from a chart but does not upgrade or delete them; that was a deliberate decision to avoid data loss. Flux lets you opt in with `.crds` in `.spec.install` and `.spec.upgrade`:

- `Skip`: do not install or upgrade CRDs.
- `Create` (default for both): create CRDs that do not exist, never upgrade or delete.
- `CreateReplace`: create new CRDs and replace existing ones, but do not delete CRDs that vanished from the chart.

```yaml
apiVersion: helm.toolkit.fluxcd.io/v2
kind: HelmRelease
metadata:
  name: my-operator
  namespace: default
spec:
  interval: 15m
  chart:
    spec:
      chart: my-operator
      sourceRef:
        kind: HelmRepository
        name: my-repo
  install:
    crds: CreateReplace
  upgrade:
    crds: CreateReplace
```

Note:
- Persistent client (`.spec.persistentClient`, default true) can make CRDs created outside Helm CRD hooks invisible to post-install hooks in some charts; disable it for those.

## Checked

2026-11-03. Read the HelmRelease reference (fluxcd.io/flux/components/helm/helmreleases/): Helm CRD limitation, `Skip`, `Create` (default) and `CreateReplace` for `.spec.install.crds` and `.spec.upgrade.crds`, and the `.spec.persistentClient` note (default true). Removed unsupported claims about the crds/ directory scope, separate Kustomizations and release notes.

Method: documentation only; no commands were run.
