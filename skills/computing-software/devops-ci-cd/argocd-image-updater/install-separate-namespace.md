---
id: computing-software.devops-ci-cd.argocd-image-updater.install-separate-namespace
name: install-separate-namespace
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, install, separate-namespace, rbac, argocd-namespace, metrics-clusterrolebinding, watch-namespaces]
level: advanced
status: docs-checked
description: "Install Argo CD Image Updater in its own namespace: set ARGOCD_NAMESPACE and watch namespaces, patch the metrics ClusterRoleBindings, and grant a Role in the Argo CD namespace."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/installation.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Install in a separate namespace

Option 2 in the install docs trades convenience for workload isolation. Let `<argocd_namespace>` hold Argo CD and `<updater_namespace>` hold the controller.

1. Create the namespace and apply `config/install.yaml` into it with `kubectl apply -n <updater_namespace> -f ...`.
2. Tell the controller where Argo CD lives, by env var, ConfigMap or flag:
   - env: `ARGOCD_NAMESPACE` and `IMAGE_UPDATER_WATCH_NAMESPACES` set to `"<updater_namespace>,<argocd_namespace>"`
   - ConfigMap `argocd-image-updater-config`: `argocd.namespace` and `watch.namespaces`
   - flags: `--argocd-namespace=<argocd_namespace>` and `--watch-namespaces=<updater_namespace>,<argocd_namespace>`

   Watch scope matters because the default is the controller's own namespace only, so it would not see Applications in `<argocd_namespace>`.
3. Patch the metrics `ClusterRoleBinding` subjects (`argocd-image-updater-metrics-auth-rolebinding` and `argocd-image-updater-metrics-reader-rolebinding`). The manifest hardcodes `namespace: argocd`; without the patch the ServiceAccount lacks `TokenReview`, `SubjectAccessReview` and metrics-reader permissions.
4. In `<argocd_namespace>` create a `Role` (`argocd-image-updater-argocd-ns-role`) and `RoleBinding` for the `argocd-image-updater-controller` ServiceAccount. The Role needs get/list/watch on `secrets` and `configmaps`, create on `events`, full verbs on `imageupdaters` (plus `imageupdaters/finalizers` update and `imageupdaters/status` get/patch/update), and get/list/patch/update/watch on `applications` in `argoproj.io`.

`ImageUpdater` CRs must live in the same namespace as the Applications they reference, so they belong in `<argocd_namespace>`.

## Checked

2026-11-04. Confirmed against installation.md (Option 2 steps, env/ConfigMap/flag forms, metrics ClusterRoleBinding names and hardcoded namespace, Role rules and names).

Method: documentation only; no commands were run.
