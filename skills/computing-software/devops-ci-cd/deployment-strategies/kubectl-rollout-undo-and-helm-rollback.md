---
id: computing-software.devops-ci-cd.deployment-strategies.kubectl-rollout-undo-and-helm-rollback
name: kubectl-rollout-undo-and-helm-rollback
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, rollback, kubectl-rollout-undo, helm-rollback, revision-history, revisionhistorylimit, helm-history, helm-atomic, rollout-status, change-cause, gitops-rollback, argo-cd-rollback]
level: practitioner
status: docs-checked
description: "Roll back Kubernetes releases fast: kubectl rollout undo with revision history, helm rollback and --atomic, what each does and doesn't revert, and rollback under GitOps."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-back-a-deployment", "https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/kubectl_rollout_undo/", "https://helm.sh/docs/helm/helm_rollback/", "https://helm.sh/docs/helm/helm_upgrade/", "https://helm.sh/docs/topics/charts/", "https://helm.sh/docs/topics/charts_hooks/", "https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubectl rollout undo and helm rollback

## kubectl (raw manifests)
```bash
kubectl rollout history deploy/api -n shop                  # revisions (ReplicaSets)
kubectl rollout history deploy/api -n shop --revision=7     # pod template of rev 7
kubectl rollout undo deploy/api -n shop                     # back to previous
kubectl rollout undo deploy/api -n shop --to-revision=7
kubectl rollout status deploy/api -n shop --timeout=5m      # wait; non-zero on failure
```
- A Deployment revision is created only when the Pod template (`.spec.template`) changes, so
  undo restores the **pod template**: ConfigMaps, Secrets, Services, HPA and CRDs are not part
  of it. If the bad release changed a ConfigMap the old pods read, undo does not fix it (use
  versioned/hashed ConfigMap names). The kubectl reference shows `rollout undo` for
  deployments and daemonsets.
- History depends on `.spec.revisionHistoryLimit` (default 10); setting it to 0 removes old
  ReplicaSets so the Deployment cannot roll back.
- Record why: `kubectl annotate deploy/api kubernetes.io/change-cause="v1.42 ($GIT_SHA)"`
  so `rollout history` shows a CHANGE-CAUSE (the `--record` flag is deprecated).
- After undo, the live object differs from git/your pipeline's manifests; the next
  `kubectl apply` reintroduces the bad version. Revert in source too.

## Helm
```bash
helm history api -n shop                       # REVISION, STATUS, CHART, APP VERSION
helm rollback api 41 -n shop --wait --timeout 5m
helm rollback api -n shop                      # previous revision
helm upgrade --install api ./chart -n shop --rollback-on-failure --timeout 10m   # Helm 4; --atomic in Helm 3
```
- `helm rollback RELEASE [REVISION]` goes to the previous release when the revision is omitted
  or 0; find revision numbers with `helm history`. It rolls back the chart's resources, not just
  the pod template.
- Hooks: `pre-rollback` and `post-rollback` hooks run (`--no-hooks` skips them); a database
  migration run by a `pre-upgrade` hook is not undone. Schema rollback is separate (see
  `computing-software.devops-ci-cd.deployment-strategies.database-migration-rollback-strategy`).
- `helm upgrade --rollback-on-failure` (Helm 4; `--atomic` in Helm 3) rolls the upgrade back to the
  previous successful release on failure and defaults `--wait` to `watcher`.
- `--history-max` (default 10) limits the revisions saved per release (0 means no limit).
- CRDs in `crds/` are only created on install: never installed on upgrade or rollback, and never
  deleted by Helm.

## GitOps (Argo CD / Flux)
Rollback = `git revert` the commit that bumped the image/values; the controller syncs.
Argo CD documents that rollback cannot be performed against an application with automated
sync enabled; `argocd app rollback APPNAME [ID]` rolls back to a history ID (previous when omitted).
Keep the image tag bump commit small so revert is clean.

## Runbook essentials
1. Decide fast: rollback criteria (error rate, SLO burn) agreed before the deploy.
2. Roll back app, verify (`rollout status`, dashboards), then investigate.
3. Revert in source of truth and block re-deploy of the bad artifact.

## Verify
In staging: deploy a broken image, run the rollback command, `rollout status` reports
success within the target time, and `kubectl get deploy api -o jsonpath='{..image}'`
shows the previous tag.

## Checked

2026-10-25, against the Kubernetes Deployment concept page and `kubectl rollout undo` reference, Helm 4 docs (`helm rollback`, `helm upgrade`, `helm history`, chart hooks, CRD limitations) and Argo CD auto-sync and `argocd app rollback` docs. Confirmed: pod-template-only revisions, `revisionHistoryLimit` default 10 and the 0 effect, `kubernetes.io/change-cause` and deprecated `--record`, `--history-max` default 10, `--rollback-on-failure` and its `--wait` default, pre/post-rollback hooks, CRD limitations, Argo CD rollback versus automated sync. Removed as unconfirmed: the pending-upgrade recovery claim, the 'recorded as an upgrade' revision detail, and StatefulSet undo support (the reference shows deployments and daemonsets).

Method: documentation only; no commands were run.
