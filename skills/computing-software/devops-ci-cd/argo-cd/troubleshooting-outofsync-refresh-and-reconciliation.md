---
id: computing-software.devops-ci-cd.argo-cd.troubleshooting-outofsync-refresh-and-reconciliation
name: troubleshooting-outofsync-refresh-and-reconciliation
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, argocd, outofsync, out-of-sync, hard-refresh, refresh-vs-sync, reconciliation-timeout, argocd-cli, app-diff, app-get, app-manifests, app-sync-dry-run, app-wait, app-history, app-rollback, comparison-error, sync-stuck, progressing-forever, unknown-sync-status, terminate-operation, orphaned-finalizer, mutating-webhook-drift, defaulted-fields, ignoredifferences-quick-fix, application-conditions, repo-server-logs, controller-logs, gitops, kubernetes]
level: practitioner
status: docs-checked
description: "Diagnose Argo CD apps stuck OutOfSync, Progressing or mid-sync: refresh vs hard refresh, app diff/manifests, drift causes, ignoreDifferences, polling interval."
sources: ["https://argo-cd.readthedocs.io/en/stable/faq/", "https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_app/", "https://argo-cd.readthedocs.io/en/stable/user-guide/diffing/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/health/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting OutOfSync, refresh and reconciliation

**Goal:** a repeatable path from "it is yellow" to the field, resource or component at fault.

## 1. Useful commands
From the `argocd app` reference:
- `argocd app get <app>` (add `--refresh` or `--hard-refresh` to force a refresh; a hard refresh refreshes application data as well as the target manifests cache).
- `argocd app diff <app>`: diff of target against live state; it also accepts `--hard-refresh`.
- `argocd app manifests <app> --source git|live`: manifests from Git (the default) or from the cluster.
- `argocd app history`, `argocd app rollback` (by history ID, previous version if omitted), `argocd app terminate-op`, `argocd app wait`, `argocd app logs`, `argocd app actions`, `argocd app list`, `argocd app set`, `argocd app sync`.
For an unreachable cluster, the FAQ shows how to rebuild the cluster config inside an Argo CD pod with `argocd admin cluster kubeconfig` and test it with `kubectl`. If a cluster Secret does not show in the CLI or UI, check it has the label `argocd.argoproj.io/secret-type: cluster`.

## 2. Stays OutOfSync after a successful sync
The diffing page lists the causes:
- extra or unknown fields in the manifest that Kubernetes drops from the live object;
- a sync with pruning disabled while resources still need deleting;
- a controller or mutating webhook altering the object after submission;
- a Helm template function such as `randAlphaNum` producing different output on each render;
- the HPA controller reordering `spec.metrics` (order them in Git the way the controller does);
- the tool adding `app.kubernetes.io/instance`, which Argo CD uses to track the app (e.g. Kustomize common labels); change `application.instanceLabelKey` in `argocd-cm` (the FAQ recommends `argocd.argoproj.io/instance`), after which apps need a re-sync;
- unit normalisation by Kubernetes (`1000m` becomes `1`, `0.1` becomes `100m`, `3072Mi` becomes `3Gi`, a number gets quoted).
When you cannot fix the source, ignore the difference. Application level:
```yaml
spec:
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas
```
`group` is the API group without the version, and `name` / `namespace` can narrow the match. `jqPathExpressions` select list items by content, and `managedFieldsManagers` ignore fields owned by a named manager from `metadata.managedFields`. In a JSON pointer, write `/` inside a key as `~1`. System level, in `argocd-cm`: `resource.customizations.ignoreDifferences.<group>_<Kind>` or `resource.customizations.ignoreDifferences.all`. `resource.compareoptions` has `ignoreResourceStatusField` (`crd`, `all` (default), `none`) and `ignoreAggregatedRoles`. A JQ path expression times out after one second by default; raise `ignore.normalizer.jq.timeout` in `argocd-cmd-params-cm`. Add the `RespectIgnoreDifferences=true` sync option if sync should leave those fields alone.

## 3. Progressing forever
Health comes from built-in checks (the health page): Deployment, ReplicaSet, StatefulSet and DaemonSet need matching observed generation and updated replica count; a LoadBalancer Service and an Ingress need a non-empty `status.loadBalancer.ingress`; a Job with `.spec.suspended: true` is suspended; a CronJob is Degraded if its last job failed and Progressing if running; a PVC must be `Bound`. The FAQ lists known causes of a stuck Progressing state: Ingress controllers that do not populate `status.loadBalancer.ingress` (contour, traefik; Traefik can publish its address via `publishedService`), StatefulSets affected by a Kubernetes status bug, and StatefulSets or DaemonSets using `OnDelete`. The fix is a custom health check. Argo CD removed the health assessment of `Application` resources in 1.8; restore it with a `resource.customizations.health.argoproj.io_Application` Lua entry if app-of-apps ordering relies on it.

## 4. Slow or missing reconciliation
By default Argo CD polls Git every 3 minutes (`timeout.reconciliation: 120s` plus up to `timeout.reconciliation.jitter: 60s`, both in `argocd-cm`). Changed apps with auto-sync enabled sync; others show OutOfSync. Setting the timeout to 0 disables polling, leaving webhooks and manual refresh (and possibly `ARGOCD_DEFAULT_CACHE_EXPIRATION`); the FAQ advises against 0 and suggests a low-frequency interval such as `15m` or `1h` when webhooks are in use.

## 5. Stuck operations and deletion
- Terminate a running sync with `argocd app terminate-op <app>` (or the UI synchronization panel).
- If the repo is deleted or corrupted so manifests cannot be generated, an app cannot be deleted normally: fix the repo, or delete with `--cascade=false` and remove the resources by hand.
- Orphaned-resource monitoring is a project setting with performance implications; scope it to well-defined namespaces.

## Verify
- [ ] `argocd app diff <app>` is empty after a sync, or every remaining diff has a documented `ignoreDifferences`.
- [ ] Each Progressing resource is either genuinely rolling out or has a custom health check.
- [ ] The polling interval (or webhook setup) matches how quickly you need changes picked up.

## Checked
2026-11-09. Confirmed against the Argo CD FAQ (Progressing causes, polling interval, instance label, normalisation, deletion without repo, terminate, cluster troubleshooting), the diffing page (causes, ignoreDifferences forms, system-level keys, JQ timeout), the resource health page (built-in checks, Application health removal) and the `argocd app` command reference (subcommand list, manifests `--source`, `--hard-refresh` on diff and get). Removed: the `--show-operation` flag, condition names (ComparisonError, InvalidSpecError and others), log commands, `activeDeadlineSeconds` and `failurePolicy` advice, the rollback-disables-auto-sync claim, `argocd admin app` reconcile commands, the Delete=false remark, `ARGOCD_EXEC_TIMEOUT`, `workqueue_depth`, and all example values such as chart tags.
Method: documentation only; no commands were run.
