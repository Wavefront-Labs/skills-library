---
id: computing-software.devops-ci-cd.argo-cd.velero-backups-vs-argocd-admin-export
name: velero-backups-vs-argocd-admin-export
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, velero-argocd, argocd-backup, argocd-admin-export]
level: advanced
status: gated
description: "Decide between argocd admin export and Velero for backing up Argo CD: what each captures (CRs, secrets, Redis), restore order, and the Git-first recovery model."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/disaster_recovery/", "https://velero.io/docs/main/backup-reference/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Velero backups vs argocd admin export

Argo CD state = Applications, ApplicationSets, AppProjects (CRs) + ConfigMaps/Secrets
(argocd-cm, argocd-rbac-cm, repo creds, cluster secrets, argocd-secret). Redis is treated as a cache (gated: unconfirmed, source is paywalled or blocked).

## argocd admin export
```bash
argocd admin export -n argocd > argocd-backup-$(date +%F).yaml
argocd admin import -n argocd - < argocd-backup-2026-10-01.yaml
```
- The Argo CD disaster-recovery page documents running `argocd admin export`/`import` from the `quay.io/argoproj/argocd:$VERSION` image matching your server version, with `-n` if Argo CD is not in the default namespace (the command does not fail in the wrong namespace). Treat the backup as containing secrets (gated: unconfirmed, source is paywalled or blocked).

## Velero
```bash
velero backup create argocd-$(date +%F) --include-namespaces argocd   # add --snapshot-volumes=false only after checking the Velero flag reference
velero restore create --from-backup argocd-2026-10-01
```
- Cluster-scoped resources (such as CRDs) need `--include-cluster-resources`; check the Velero backup reference for how it interacts with the include/exclude flags.
- Velero supports excluding single items with the `velero.io/exclude-from-backup=true` label.
- Restore flow, redis handling and token re-sync were not confirmed (gated: unconfirmed, source is paywalled or blocked).

## Recommended model
1. Install Argo CD itself from Git (Helm/Kustomize, "Argo manages Argo").
2. Applications/Projects declared in Git (app-of-apps or ApplicationSets).
3. Secrets from an external store (ESO/Vault), so nothing unique lives only in the cluster.
4. Keep `argocd admin export` as a belt-and-braces nightly snapshot.

## Restore pitfalls
- Restoring Applications before cluster secrets: apps show "cluster not found". Restore secrets first.
- Restored apps with auto-sync + prune against a partially restored cluster can delete resources;
  pause auto-sync (sync windows) during restore.

## Verify
- [ ] Quarterly drill: fresh cluster, restore, all apps Synced within the RTO.

## Checked

2026-11-02. Confirmed from the Argo CD disaster recovery page: argocd admin export/import via the argocd image of the server version, -n namespace note; from the Velero backup reference: --include-namespaces, --include-cluster-resources and the velero.io/exclude-from-backup label. Removed: the CronJob/SA claim, the redis exclusion advice and the --snapshot-volumes flag from the example (not stated in the pages read). Gated: redis as cache, secrets in the export, and the Velero restore behaviour.

Method: documentation only; no commands were run.
