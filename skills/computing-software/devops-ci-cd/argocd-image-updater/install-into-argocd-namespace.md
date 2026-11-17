---
id: computing-software.devops-ci-cd.argocd-image-updater.install-into-argocd-namespace
name: install-into-argocd-namespace
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, install, install-yaml, kubectl-apply, kustomize-base, log-level, default-scope]
level: intro
status: docs-checked
description: "Install the Argo CD Image Updater controller into the Argo CD namespace with install.yaml or the Kustomize base, with namespace-scoped RBAC by default and a log level set."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/installation.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Install into the Argo CD namespace

Goal: run the controller next to Argo CD, the recommended layout (Option 1 in the docs).

The controller must run in the same Kubernetes cluster as the Argo CD `Application` resources. It cannot manage applications through a remote cluster connection.

```shell
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj-labs/argocd-image-updater/stable/config/install.yaml
```

A Kustomize base is also published at `https://github.com/argoproj-labs/argocd-image-updater/config/default`; use it as a remote base and layer overlays on top.

The default scope is namespace-scoped: the controller watches only its own namespace using a `Role` and `RoleBinding`. Older installs that watched every namespace with a `ClusterRole` must now set `--watch-namespaces="*"` and switch RBAC. If you use Argo CD's Applications in any namespace feature, set `--watch-namespaces` and create a `Role` plus `RoleBinding` in each extra namespace.

Set the log level explicitly while you are learning, in the `argocd-image-updater-config` ConfigMap:

```yaml
data:
  log.level: debug   # trace, debug, info, warn or error; default is info
```

## Checked

2026-11-04. Confirmed against installation.md (Option 1 command, Kustomize base URL, remote-cluster restriction, namespace-scoped default and warning, log.level keys and default info). Removed a generic self-check line and a cross-reference the page does not state.

Method: documentation only; no commands were run.
