---
id: computing-software.devops-ci-cd.argo-cd.app-of-apps-pattern
name: app-of-apps-pattern
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, argocd, gitops, app-of-apps, root-app, parent-application, child-application, cluster-bootstrap, bootstrapping, applicationset, application-health, sync-waves, argocd-cm, resource-customizations, lua-health-check, finalizers, cascade-delete, appproject, platform-components, kubernetes, k8s]
level: advanced
status: gated
description: "Bootstrap a cluster from one Argo CD root Application: layout, child ordering by sync wave, Application health check, safe deletion, when to switch to ApplicationSet."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/upgrading/1.7-1.8/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Argo CD app-of-apps: bootstrapping a cluster from one root Application

**Goal:** one `kubectl apply` (or `argocd app create`) of a single *root* Application
brings up every platform component and team app on a fresh cluster in the right order,
and deleting or renaming a child never takes production with it.

The overview of app-of-apps vs ApplicationSet lives in
`computing-software.devops-ci-cd.argo-cd.gitops-app-of-apps-and-sync`; this skill is the
detailed build of the pattern itself.

## 1. Layout
```
bootstrap/
  root.yaml                 # the only thing applied by hand
apps/                       # root's source path: ONLY Application/AppProject CRs
  00-projects.yaml          # AppProjects (wave -10)
  10-cert-manager.yaml      # wave -5
  20-ingress-nginx.yaml     # wave -3
  30-external-secrets.yaml  # wave -3
  50-payments.yaml          # wave 0
platform/<component>/       # what each child actually deploys (Helm values, kustomize)
```
Rules that keep it sane:
- The root's path contains **only** `Application` and `AppProject` manifests, never
  workloads. Mixing them makes the root's sync status meaningless.
- The root Application lives in the `argocd` namespace, in a locked-down project (e.g.
  `platform-admin`) — whoever can write to `apps/` can deploy anything anywhere.
- Use a kustomization or a Helm chart in `apps/` if child specs differ only by values
  (cluster URL, `targetRevision`); a Helm-templated `apps/` chart is the classic form.

## 2. Ordering children: the health-check gotcha
Put `argocd.argoproj.io/sync-wave` on the **child Application CRs**. But since Argo CD
1.8 the health of an `Application` resource is no longer assessed by default, so the
root treats each child as healthy immediately and the waves don't wait. Restore it in
`argocd-cm`:
```yaml
data:
  resource.customizations.health.argoproj.io_Application: |
    hs = {}
    hs.status = "Progressing"
    hs.message = ""
    if obj.status ~= nil and obj.status.health ~= nil then
      hs.status = obj.status.health.status
      if obj.status.health.message ~= nil then hs.message = obj.status.health.message end
    end
    return hs
```
Only with this does "cert-manager (wave -5) Healthy before ingress (wave -3)" hold.
The Argo CD health documentation gives this customization for restoring Application health assessment (the docs say the built-in assessment was removed in 1.8); verify the exact Lua against the docs for your release.

CRD-then-CR across children (e.g. cert-manager CRDs, then a `ClusterIssuer` in another
child) still needs the CR's child in a later wave **or** the `SkipDryRunOnMissingResource=true` sync option (gated: unconfirmed, source is paywalled or blocked).

## 3. Sync policy of root vs children
- Root: `automated` with `selfHeal: true`, but think hard about `prune: true`. With
  prune on, deleting a file from `apps/` deletes the child Application, and if the child
  has the `resources-finalizer.argocd.argoproj.io` finalizer, **its workloads too**.
- A safe default: root prunes, children carry the finalizer only where cascade-delete is
  intended (ephemeral/preview apps); stateful platform pieces (databases, operators with
  CRDs) omit it so removal only "unmanages".
- To retire a child deliberately: remove the finalizer in Git, sync, then delete the file.
- Renaming a child file is harmless; renaming `metadata.name` is a delete + create —
  with a finalizer, that is a full teardown and redeploy.

## 4. Bootstrapping a new cluster
1. Install Argo CD itself (Helm or manifests). Optionally have the root also manage an
   `argocd` child pointing at Argo CD's own config — Argo CD managing itself works, but
   keep the install reproducible outside Argo CD for disaster recovery.
2. `kubectl apply -n argocd -f bootstrap/root.yaml`.
3. Watch: `argocd app list`, `argocd app wait root --health --timeout 900`.

## 5. When to stop using app-of-apps
Switch the `apps/` folder to an **ApplicationSet** when children become "N services ×
M clusters/envs" generated from a pattern; keep app-of-apps for the hand-curated
platform layer. Mixing works well: root → (platform children) + (one ApplicationSet per
team). Avoid nesting app-of-apps more than two levels; debugging which level is OutOfSync
becomes painful.

## Gotchas
- Children created in a project that the root's project can't target fail with a
  permission error that looks like a sync failure on the root.
- `argocd app delete root` with cascade = deleting everything. Protect with RBAC.
- A child stuck Progressing (e.g. a LoadBalancer Service with no external IP on a local
  cluster) blocks every later wave once the health check is enabled.

## Verify
- [ ] Fresh cluster + one `kubectl apply` reaches all-Synced/Healthy with no manual step.
- [ ] Waves actually wait: a deliberately unhealthy wave -5 child stops wave -3 from syncing.
- [ ] Removing a stateful child's file from `apps/` leaves its workloads running.
- [ ] Only `Application`/`AppProject` kinds appear in the root's resource tree.
- [ ] Root lives in a restricted AppProject; write access to `apps/` is reviewed.

## Checked

2026-11-02. Confirmed against the Argo CD cluster bootstrapping and resource health pages: app-of-apps with resources-finalizer.argocd.argoproj.io, finalizer cascade behaviour, removal of Application health assessment in 1.8 and the resource.customizations.health.argoproj.io_Application Lua; and the argocd app wait reference (--health, --timeout). Gated: the SkipDryRunOnMissingResource option name. Layout, wave numbering and project examples are illustrative design advice, not documented facts.

Method: documentation only; no commands were run.
