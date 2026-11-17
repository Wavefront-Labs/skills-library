---
id: computing-software.devops-ci-cd.argocd-image-updater.install-cluster-scoped-watch
name: install-cluster-scoped-watch
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, watch-namespaces, cluster-scoped, clusterrole, clusterrolebinding, namespace-scope, rbac]
level: advanced
status: docs-checked
description: "Control which namespaces Argo CD Image Updater watches with --watch-namespaces, and swap the Role for a ClusterRole when you need wildcard cluster-wide watching."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/installation.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/cmd/run.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Namespace scope and cluster-scoped install

`--watch-namespaces` (env `IMAGE_UPDATER_WATCH_NAMESPACES`, ConfigMap key `watch.namespaces`) decides which namespaces the controller watches for `ImageUpdater` CRs and Applications:

| Value | Scope | RBAC |
|---|---|---|
| not set | controller's own namespace | `Role` + `RoleBinding` there |
| `ns1,ns2` | listed namespaces | `Role` + `RoleBinding` in each |
| `*` | all namespaces | `ClusterRole` + `ClusterRoleBinding` |

Example flag: `--watch-namespaces=argocd,team-a,team-b`.

Cluster-scoped steps (Option 3):

1. Apply `install.yaml` as usual.
2. Delete the namespace-scoped RBAC: `kubectl delete role argocd-image-updater-manager-role -n argocd` and `kubectl delete rolebinding argocd-image-updater-manager-rolebinding -n argocd`.
3. Create a `ClusterRole` named `argocd-image-updater-manager-role` (create on `events`, full verbs on `imageupdaters`, `imageupdaters/finalizers` update, `imageupdaters/status` get/patch/update, and get/list/patch/update/watch on `applications`) and a `ClusterRoleBinding` named `argocd-image-updater-manager-rolebinding` for the `argocd-image-updater-controller` ServiceAccount.
4. Set the env var `IMAGE_UPDATER_WATCH_NAMESPACES` to `"*"`.

Note: the previous default was cluster-wide watching. The docs say existing installs that rely on it must explicitly set `--watch-namespaces="*"` and switch to ClusterRole and ClusterRoleBinding RBAC.

## Checked

2026-11-04. Confirmed against installation.md (namespace scope table, Option 3 steps, ClusterRole rules and names, default-scope warning) and the run command page (--watch-namespaces, env var). Removed the unconfirmed claim that old installs break silently.

Method: documentation only; no commands were run.
