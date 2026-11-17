---
id: computing-software.cloud-infrastructure-engineering.kubernetes.helm-release-operations-and-storage
name: helm-release-operations-and-storage
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, helm, helm-rollback, helm-history, helm-atomic, pending-upgrade, helm-release-secrets, helm-storage-driver]
level: practitioner
status: gated
description: "Operate Helm releases: upgrade --install --atomic, history and rollback, fixing 'another operation is in progress', and release Secret storage limits."
sources: ["https://helm.sh/docs/helm/helm_upgrade/", "https://helm.sh/docs/helm/helm_rollback/", "https://helm.sh/docs/topics/advanced/#storage-backends", "https://helm.sh/docs/faq/troubleshooting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Helm release operations and release storage

## Upgrade safely
```bash
helm upgrade --install web ./chart -n web --create-namespace \
  -f values-prod.yaml --atomic --timeout 10m --history-max 10
```
- `--atomic` (Helm 3 and 4.3.1) implies `--wait` and rolls back on failure or timeout. On Helm 4's main branch the flag
  is `--rollback-on-failure` and `--atomic` is a deprecated alias (`pkg/cmd/upgrade.go`).
- `--wait` waits for Pods, PVCs, Services and the minimum Pods of Deployments/StatefulSets/ReplicaSets; with it,
  `--wait-for-jobs` also waits for all Jobs to complete (`helm upgrade --help`).
- `--history-max` (default 10, 0 means no limit) bounds stored revisions.
- `helm diff upgrade` (plugin) before prod upgrades.

## History and rollback
```bash
helm history web -n web                   # REVISION STATUS CHART APP VERSION DESCRIPTION
helm get values web -n web --revision 7   # what was deployed
helm get manifest web -n web --revision 7
helm rollback web 7 -n web --wait         # creates a new revision (e.g. 9) with rev 7's content
```
Rollback re-applies old manifests with a 3-way merge; it does **not** roll back CRDs or data
migrations, and resources created by hooks aren't removed (gated: unconfirmed, source is paywalled or blocked). `helm rollback --cleanup-on-fail` deletes new
resources created during a failed rollback.

## "another operation (install/upgrade/rollback) is in progress"
The latest revision is stuck in `pending-install`, `pending-upgrade` or `pending-rollback`
(CI job killed mid-upgrade, timeout without --atomic).
```bash
helm history web -n web | tail -3    # cluster commands in this section were not run here (gated: unconfirmed, source is paywalled or blocked)
# safest: roll back to the last deployed revision
helm rollback web <last-deployed-rev> -n web
# if no deployed revision exists (failed first install): helm uninstall web -n web
# last resort: delete only the stuck revision's storage object
kubectl -n web get secrets -l owner=helm,name=web
kubectl -n web delete secret sh.helm.release.v1.web.v12     # the pending one only
```
Prevent it: never cancel CI jobs running Helm without cleanup; serialize deploys per release.

## Release storage
- Default driver **Secret** in the release namespace: `sh.helm.release.v1.<name>.v<rev>`,
  type `helm.sh/release.v1`, labels `owner=helm` and `name=<release>`, data = gzip+base64 of the release (chart + values + manifest).
- Each Secret is limited to 1MiB (Kubernetes Secret docs): huge charts (many CRDs, big embedded files) fail with
  `Secret "sh.helm.release..." is invalid: data: Too long`. Options:
  `HELM_DRIVER=configmap` (same limit (gated: unconfirmed, source is paywalled or blocked)), **`HELM_DRIVER=sql`** (Postgres) for very large
  releases, or slim the chart (install CRDs separately).
- Anyone with `get secrets` in the namespace can read all values (incl. passwords) of every
  revision — another reason to keep secrets out of values.
- Storage objects are what `helm list` reads; deleting them "forgets" a release without
  touching resources.

## Verify
- [ ] `helm list -A --pending` and `--failed` empty; history bounded.
