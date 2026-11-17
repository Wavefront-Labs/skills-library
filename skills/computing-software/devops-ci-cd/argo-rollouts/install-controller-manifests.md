---
id: computing-software.devops-ci-cd.argo-rollouts.install-controller-manifests
name: install-controller-manifests
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [install, controller, manifests, namespace-install, crds, argo-rollouts]
level: intro
status: docs-checked
description: "Install the Argo Rollouts controller with install.yaml or the namespace-scoped install plus separately applied CRDs."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/installation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Argo Rollouts ships two manifests. `install.yaml` is the standard cluster-wide install; `namespace-install.yaml` needs only namespace-level privileges, which suits running several controller instances in different namespaces on one cluster.

Standard install:

```bash
kubectl create namespace argo-rollouts
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml
```

If you use a different namespace, edit the ClusterRoleBinding in `install.yaml` so its ServiceAccount subject names that namespace.

The namespace install does not include the CRDs. Apply them separately from the `manifests/crds` directory:

```bash
kubectl apply --server-side -k https://github.com/argoproj/argo-rollouts/manifests/crds\?ref\=stable
```

Two environment notes from the docs. On Kubernetes 1.14 or lower the CRDs must be applied with `--validate=false`, because they use fields added in 1.15. On GKE your account needs permission to create cluster roles, for example by binding `cluster-admin` to your user first.

Released controller images are on Quay.io; older releases on Docker Hub exist, but the project moved to Quay since the introduction of rate limiting.

Verify: `kubectl get pods -n argo-rollouts` shows the controller Running. Then install the CLI with the kubectl-plugin-install-and-completion skill.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/installation/.

Removed or corrected: the quay.io image path, the argo-helm charts claim and the CRD verify command.

Method: documentation only; no commands were run.
