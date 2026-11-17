---
id: computing-software.devops-ci-cd.flux.flux-upgrade-procedure
name: flux-upgrade-procedure
category: computing-software
field: devops-ci-cd
product: flux
tags: [upgrade, flux-install, gotk-components, flux-check, bootstrap]
level: sme
status: docs-checked
description: "Upgrade the Flux CLI and bootstrapped controllers by regenerating gotk-components.yaml and pushing it to Git."
sources:
  - https://fluxcd.io/flux/installation/upgrade/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
Flux upgrades from any v2.x to any other v2.x release (latest patch). For v2.7 and later the project publishes a dedicated step-by-step discussion, so read it before a minor upgrade.

CLI: `flux check --pre` reports whether a newer version exists. Update through a package manager or GitHub releases and verify with `flux --version`.

Controllers installed by bootstrap can upgrade themselves through Git, with no direct cluster access:

```shell
git clone https://<git-host>/<org>/<bootstrap-repo>
cd <bootstrap-repo>
flux install --export > ./clusters/my-cluster/flux-system/gotk-components.yaml
git add -A && git commit -m "Update $(flux -v) on my-cluster"
git push
```

If you enabled extra components, include them when exporting:

```shell
flux install \
  --components-extra image-reflector-controller,image-automation-controller \
  --export > ./clusters/my-cluster/flux-system/gotk-components.yaml
```

Then wait, or force it now:

```sh
flux reconcile ks flux-system --with-source
```

Alternatively rerun `flux bootstrap` with the same arguments as before (it updates `gotk-components.yaml` and pushes to the remote branch), then verify with `flux check`. The Flux GitHub Action can automate the components manifest update and open a PR when a new version is available.

Kubectl installs: `kubectl apply --server-side -f https://github.com/fluxcd/flux2/releases/latest/download/install.yaml`. Terraform provider installs: update the provider and run `terraform apply`. Flux Operator installs: update the operator, then the `FluxInstance` `spec.distribution.version`.

## Checked

2026-11-08. Read in full: https://fluxcd.io/flux/installation/upgrade/ (raw source in the fluxcd/website repository).

Removed or corrected: the claims that sharded controllers upgrade together with the main ones, that customisation patches stay in place, and the release-notes advice; added the other documented upgrade routes.

Method: documentation only; no commands were run.
