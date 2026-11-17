---
id: computing-software.cloud-infrastructure-engineering.rancher.air-gapped-helm-install-rancher
name: air-gapped-helm-install-rancher
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [air-gap, helm, systemdefaultregistry, usebundledsystemchart, certmanager-version, private-registry]
level: advanced
status: docs-checked
description: "Install Rancher from a fetched chart tarball in an air gap: chart options for registry and bundled system charts, offline cert-manager, and secret-based certificates."
sources:
  - https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/other-installation-methods/air-gapped-helm-cli-install/install-rancher-ha
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Air gapped Kubernetes installs work from a chart tarball. On an internet-connected machine run `helm fetch rancher-<CHART_REPO>/rancher` (optionally with `--version`), and copy the result to a machine that can reach the cluster. Only two certificate sources are recommended offline: Rancher-generated (`ingress.tls.source=rancher`, the default, needs cert-manager) and your own files (`ingress.tls.source=secret`).

Chart options built for air gaps:

| Option | Purpose |
|---|---|
| `certmanager.version` | Pick the right Rancher TLS issuer for the running cert-manager version |
| `systemDefaultRegistry` | Always pull from your private registry when provisioning clusters |
| `useBundledSystemChart` | Use the system charts packaged with Rancher (monitoring, logging, alerting, global DNS) instead of a Git mirror |

For the default certificate, fetch the cert-manager chart (`helm fetch jetstack/cert-manager --version v1.11.0` in the page) and its CRD file, then install it offline with `image.repository`, `webhook.image.repository`, `cainjector.image.repository` and `startupapicheck.image.repository` all pointing at your registry.

Install Rancher from the tarball:

```plain
   helm install rancher ./rancher-<VERSION>.tgz \
    --namespace cattle-system \
    --set hostname=<RANCHER.YOURDOMAIN.COM> \
    --set certmanager.version=<CERTMANAGER_VERSION> \
    --set image.registry=<REGISTRY.YOURDOMAIN.COM:PORT> \
    --set systemDefaultRegistry=<REGISTRY.YOURDOMAIN.COM:PORT> \ # Set a default private registry to be used in Rancher
    --set useBundledSystemChart=true # Use the packaged Rancher system charts
```

To pin a version use `--set image.tag=`. With your own certificates, publish the secrets first and add `--set ingress.tls.source=secret` (plus `privateCA=true` for a private CA). The certificate common name must match `hostname`.

## Checked

2026-11-04. Checked against the Rancher Manager documentation pages: Air Gap: Kubernetes install (Install Rancher). Nothing removed.

Method: documentation only; no commands were run.
