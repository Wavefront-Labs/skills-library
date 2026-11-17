---
id: computing-software.cloud-infrastructure-engineering.kubernetes.fleet-gitops-argocd-applicationsets
name: fleet-gitops-argocd-applicationsets
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, argocd, argo-cd, applicationset, gitops, cluster-generator, git-generator, matrix-generator, pull-request-generator, multi-cluster, fleet, progressive-sync, templating]
level: advanced
status: docs-checked
description: "Deploy the same or templated app manifests to hundreds of clusters with Argo CD ApplicationSets using cluster, git, and matrix generators."
sources: ["https://argo-cd.readthedocs.io/en/latest/operator-manual/applicationset/", "https://argo-cd.readthedocs.io/en/latest/operator-manual/applicationset/Progressive-Syncs/", "https://argo-cd.readthedocs.io/en/latest/operator-manual/applicationset/Application-Deletion/", "https://argo-cd.readthedocs.io/en/latest/operator-manual/applicationset/GoTemplate/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Argo CD ApplicationSets — one spec, N clusters

**Goal:** generate an `Application` per cluster (or per cluster x app, or per PR) from
one `ApplicationSet`, so adding a cluster to the fleet means registering it, not writing
new Argo CD YAML. Related: `computing-software.cloud-infrastructure-engineering.kubernetes.rancher-fleet-management`
covers the same problem with Fleet instead of Argo CD — pick one GitOps engine per fleet,
don't run both against the same clusters.

## 1. Generators
- **Cluster generator** — one `Application` per cluster registered in Argo CD
  (`argocd cluster add` or a `Secret` labeled `argocd.argoproj.io/secret-type: cluster`).
  Filter with `selector.matchLabels` so e.g. only `env: prod` clusters get an app.
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata: {name: platform-agent}
spec:
  generators:
  - clusters:
      selector: {matchLabels: {env: prod}}
  template:
    metadata: {name: "platform-agent-{{name}}"}
    spec:
      destination: {server: "{{server}}"}
      source: {repoURL: https://git.example.com/platform.git, path: apps/platform-agent, targetRevision: main}
```
- **Git generator** (`directories` or `files`) — one `Application` per matching folder
  or JSON/YAML file in a repo; used for "one app per tenant folder" patterns.
- **Matrix generator** — combines two generators (e.g. clusters x git directories) so
  every tenant app is deployed to every matching cluster without a manual cross-product.
- **Pull Request generator** — one `Application` per open pull request, for preview environments.

## 2. Templating per cluster
- Generator output fields (`{{name}}`, `{{server}}`, and any label/annotation on the
  cluster Secret) are available in `spec.template` — use cluster labels to pass
  per-cluster values (region, size tier) into Helm `valueFiles` or Kustomize patches
  referenced by the generated `Application`.
- `goTemplate: true` switches from the default `{{name}}` substitution to Go templates (`{{ .name }}`) with
  the Sprig functions (except `env`, `expandenv`, `getHostByName`). The docs recommend
  `goTemplateOptions: ["missingkey=error"]` so undefined values fail instead of rendering silently.

## 3. Progressive/staged rollout
- `strategy: RollingSync` with `steps` rolls a change group by group. It is a **Beta** feature (since
  Argo CD v3.3.0) and must be enabled explicitly: `--enable-progressive-syncs` on the ApplicationSet
  controller, `ARGOCD_APPLICATIONSET_CONTROLLER_ENABLE_PROGRESSIVE_SYNCS=true`, or
  `applicationsetcontroller.enable.progressive.syncs: "true"` in `argocd-cmd-params-cm`.
- Each step's `matchExpressions` select generated Applications by label (all expressions must be true;
  `In` needs at least one matching value). `maxUpdate` limits simultaneous updates per group (default 100%).
- RollingSync forces autosync off on the generated Applications and triggers syncs like the UI would,
  so sync windows apply.

## Gotchas
- Deleting an `ApplicationSet` deletes the Applications it generated. By default each Application carries the
  `resources-finalizer.argocd.argoproj.io` finalizer, so its deployed resources are deleted too, even with
  `kubectl delete ApplicationSet --cascade=orphan`. Set `spec.syncPolicy.preserveResourcesOnDeletion: true`
  to keep the resources. The controller `--policy` (`sync`, `create-only`, `create-update`, `create-delete`)
  restricts what the controller may do to Applications.
- The cluster generator targets clusters from Secrets labelled `argocd.argoproj.io/secret-type: cluster`
  and automatically includes the local cluster when it matches the selector; test selectors against the
  live cluster list.
- A matrix generator combines the parameters of exactly two child generators (every combination), so an
  empty leg yields no Applications.

## Verify
- [ ] `kubectl get applicationset <name> -o yaml` and `kubectl get applications` show the expected number of generated Applications.
- [ ] Adding a new cluster with the right label produces a new `Application` and a
      healthy sync within the expected interval, with no manual Argo CD edit.
- [ ] If using `RollingSync`, progressive syncs are enabled and stages roll in order (tested with a deliberately broken manifest).
- [ ] Deleting the ApplicationSet behaves as intended (prune vs preserve) — confirmed
      in a non-prod fleet before relying on it in prod.

## Checked

2026-10-26, against Argo CD ApplicationSet docs (argoproj/argo-cd docs/operator-manual/applicationset on main: Generators-Cluster, Generators-Matrix, GoTemplate, Progressive-Syncs, Application-Deletion, Controlling-Resource-Modification). Confirmed: cluster generator Secret label and `selector.matchLabels`, matrix generator behaviour, `goTemplate` and `missingkey=error`, RollingSync status (Beta since v3.3.0), how to enable it, `matchExpressions` and `maxUpdate`, forced autosync-off, finalizer and `preserveResourcesOnDeletion`, `--policy` values. Wrong or missing: RollingSync needs explicit enabling and is Beta; the prune-based explanation of deletion was wrong (the resources-finalizer causes it); `preserveResourcesOnDeletion` lives under `spec.syncPolicy`. Removed unconfirmed claims about silent skipping of mis-labelled cluster Secrets and PR cleanup.

Method: documentation only; no commands were run.
