---
id: computing-software.devops-ci-cd.flux.bootstrap-customization-patches
name: bootstrap-customization-patches
category: computing-software
field: devops-ci-cd
product: flux
tags: [bootstrap, kustomize-patches, gotk-components, controller-args, flux-system]
level: sme
status: docs-checked
description: "Customise Flux controller deployments at bootstrap using kustomize patches in the flux-system directory of the fleet repo."
sources:
  - https://fluxcd.io/flux/installation/configuration/bootstrap-customization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
To customise controllers, edit the Git repository that bootstrap writes to. Create the structure first:

```sh
mkdir -p clusters/my-cluster/flux-system
touch clusters/my-cluster/flux-system/gotk-components.yaml \
    clusters/my-cluster/flux-system/gotk-sync.yaml \
    clusters/my-cluster/flux-system/kustomization.yaml
```

Controller deployments, container command arguments, node affinity and similar can be customised with Kustomize strategic merge patches and JSON patches. `kustomization.yaml` lists the generated manifests as resources and applies the patches:

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - gotk-components.yaml
  - gotk-sync.yaml
patches:
  - patch: |
      - op: add
        path: /spec/template/spec/containers/0/args/-
        value: --concurrent=5
    target:
      kind: Deployment
      name: "source-controller"
```

Targets can be all controllers (`labelSelector: "app.kubernetes.io/part-of=flux"`) or a regex of names such as `"(kustomize-controller|helm-controller)"`.

Push to the main branch, then run bootstrap against that path:

```sh
flux bootstrap git --url=ssh://git@<host>/<org>/<repository> \
  --branch=main --path=clusters/my-cluster
```

To amend later, pull the changes locally, edit `kustomization.yaml`, push upstream and rerun bootstrap.

## Checked

2026-11-08. Read in full: https://fluxcd.io/flux/installation/configuration/bootstrap-customization/ (raw source in the fluxcd/website repository).

Removed or corrected: the claims about patches persisting across upgrades, idempotent reruns, CLI pinning and the verification commands, none of which is on the page.

Method: documentation only; no commands were run.
