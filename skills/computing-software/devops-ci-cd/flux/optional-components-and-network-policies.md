---
id: computing-software.devops-ci-cd.flux.optional-components-and-network-policies
name: optional-components-and-network-policies
category: computing-software
field: devops-ci-cd
product: flux
tags: [components, components-extra, image-automation, networkpolicy, cluster-domain]
level: sme
status: docs-checked
description: "Choose which Flux controllers to install with --components and --components-extra, plus network policy and cluster domain flags."
sources:
  - https://fluxcd.io/flux/installation/configuration/optional-components/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`flux bootstrap` and `flux install` deploy controllers, CRDs, RBAC and network policies into `flux-system`.

Default components (`--components`):

```sh
flux bootstrap git --components source-controller,kustomize-controller,helm-controller,notification-controller
```

The minimum for bootstrapping is source-controller and kustomize-controller.

Extra components (`--components-extra`) are off by default:

```sh
flux bootstrap git --components-extra image-reflector-controller,image-automation-controller
flux bootstrap git --components-extra source-watcher
```

The image controllers enable image update automation. source-watcher enables source composition and decomposition.

Network policies: by default they block all ingress to `flux-system` except the notification-controller webhook receiver, so only Flux components can read source artifacts from source-controller. You can deploy without them with `--network-policy false`, which is not recommended.

Cluster domain: components talk to source-controller and notification-controller using FQDNs built from the cluster domain, to cut DNS queries (for example `http://source-controller.flux-system.svc.cluster.local./`). Default is `cluster.local`; change it with:

```sh
flux bootstrap git --cluster-domain cluster.internal
```

Without the flags, both `flux bootstrap` and `flux install` deploy the default components and no extras.

## Checked

2026-11-08. Read in full: https://fluxcd.io/flux/installation/configuration/optional-components/ (raw source in the fluxcd/website repository).

Removed or corrected: the closing advice on installing only what you use and repeating flags on rerun, which is not on the page.

Method: documentation only; no commands were run.
