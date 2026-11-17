---
id: computing-software.cloud-infrastructure-engineering.rancher.helm-install-rancher-steps
name: helm-install-rancher-steps
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [helm, install, cert-manager, cattle-system, rancher-stable, hostname]
level: practitioner
status: docs-checked
description: "Install Rancher on a Kubernetes cluster with Helm: repo choice, cattle-system namespace, cert-manager, the install command, and rollout verification."
sources:
  - https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/install-upgrade-on-a-kubernetes-cluster
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rancher can be installed on any Kubernetes cluster, but the Rancher UI and API are exposed through an Ingress, so the cluster needs an ingress controller. RKE2 and K3s ship one. Hosted clusters (EKS, GKE, AKS) need one deployed first, and because the chart does not set an `ingressClassName`, that controller must also watch ingresses without one. GKE Autopilot clusters cannot host Rancher, since Rancher must create resources in `kube-system`.

The sequence is: add a chart repo, create the namespace, choose the TLS source, install cert-manager if needed, install the chart, verify. Repos are `rancher-latest` (newest features), `rancher-stable` (recommended for production) and `rancher-alpha` (preview; upgrades to, from or between alphas are unsupported; installs need `--devel`).

```
kubectl create namespace cattle-system
```

The namespace must always be `cattle-system`, and the Helm release name must always be `rancher`. cert-manager is only required for `ingress.tls.source=rancher` or `letsEncrypt`; skip it for your own certificates or external TLS termination. The page installs it from the Jetstack repo with `crds.enabled=true`.

A minimal install sets `hostname` (the DNS name pointing at your load balancer) and `bootstrapPassword`. For a proof of concept, a name such as `<IP_OF_LINUX_NODE>.sslip.io` works as hostname.

Verify with `kubectl -n cattle-system rollout status deploy/rancher`. If it exceeds the progress deadline, compare DESIRED and AVAILABLE counts from `kubectl -n cattle-system get deploy rancher`.

## Checked

2026-11-04. Checked against the Rancher Manager documentation pages: Install/Upgrade Rancher on a Kubernetes Cluster. Nothing removed.

Method: documentation only; no commands were run.
