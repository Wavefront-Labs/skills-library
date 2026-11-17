---
id: computing-software.cloud-infrastructure-engineering.linkerd.helm-install-crds-then-control-plane
name: helm-install-crds-then-control-plane
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, helm, install, crds, control-plane]
level: practitioner
status: docs-checked
description: "Install Linkerd with Helm as two charts in order, linkerd-crds then linkerd-control-plane, passing your own certificates."
sources:
  - https://linkerd.io/2.19/tasks/install-helm/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Helm installs use two charts installed in succession. First check that the Gateway API CRDs are present, since authorization policy and dynamic routing depend on them. Generate trust anchor and issuer certificates yourself, because Helm cannot generate them.

```bash
helm repo add linkerd-edge https://helm.linkerd.io/edge

helm install linkerd-crds linkerd-edge/linkerd-crds \
  -n linkerd --create-namespace

helm install linkerd-control-plane \
  -n linkerd \
  --set-file identityTrustAnchorsPEM=ca.crt \
  --set-file identity.issuer.tls.crtPEM=issuer.crt \
  --set-file identity.issuer.tls.keyPEM=issuer.key \
  linkerd-edge/linkerd-control-plane
```

Omit `--create-namespace` if the `linkerd` namespace already exists.

Variations:

- With the Linkerd CNI plugin, add `--set cniEnabled=true` to both installs.
- On a cluster using Cilium in kube-proxy replacement mode, extra steps are listed on the cluster configuration page.
- For high availability, the control-plane chart ships a `values-ha.yaml` that overrides some default values for a high-availability setup, analogous to `linkerd install --ha`.

## Checked

2026-11-03. Confirmed against: https://linkerd.io/2.19/tasks/install-helm/.

Removed or reworded: Secret-store/GitOps advice and the replicas/affinities detail.

Method: documentation only; no commands were run.
