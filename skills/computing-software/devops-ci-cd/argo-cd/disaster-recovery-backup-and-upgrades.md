---
id: computing-software.devops-ci-cd.argo-cd.disaster-recovery-backup-and-upgrades
name: disaster-recovery-backup-and-upgrades
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, argocd, argocd-backup, argocd-restore, argocd-admin-export, argocd-admin-import, disaster-recovery, argocd-upgrade, upgrade-notes, crd-upgrade, helm-chart-upgrade, argocd-secret, argocd-cm, redis-cache-rebuild, finalizers-cascade, argo-manages-argo, bootstrap-from-git, cluster-rebuild, rto, rpo, version-skew, downgrade, gitops, kubernetes]
level: practitioner
status: docs-checked
description: "Recover and upgrade Argo CD: what state lives in the namespace, argocd admin export/import, finalizer caution, semver upgrade rules and server-side apply."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/disaster_recovery/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/upgrading/overview/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/upgrading/2.7-2.8/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disaster recovery, backup and upgrades

**Goal:** rebuild Argo CD on a fresh cluster with apps, projects, clusters and settings intact, and take upgrades without surprises.

## 1. What is state
Everything is declarative in the Argo CD namespace (by default `argocd`; Application and AppProject resources must live there). The declarative-setup page lists the single supported names:
- ConfigMaps: `argocd-cm`, `argocd-cmd-params-cm`, `argocd-rbac-cm`, `argocd-tls-certs-cm`, `argocd-ssh-known-hosts-cm`. ConfigMaps need the label `app.kubernetes.io/part-of: argocd` or Argo CD cannot use them.
- Secret `argocd-secret`: user passwords, certificates (deprecated), the signing key, Dex secrets and webhook secrets.
- Secrets labelled `argocd.argoproj.io/secret-type` with value `repository`, `repo-creds` or `cluster` for repositories, credential templates and clusters.
- `Application`, `ApplicationSet` and `AppProject` resources.
If these live in Git and Argo CD applies them (Argo managing itself), the backup problem reduces to the secrets plus a bootstrap step.

## 2. Backup and restore with argocd admin
The disaster-recovery page uses `argocd admin` to export and import all Argo CD data. Point `~/.kube/config` at the Argo CD cluster, find the server version (`argocd version`), and run the CLI from the matching image:
```
docker run -v <KUBE_DIR>:<CONTAINER_KUBE_DIR> --rm quay.io/argoproj/argocd:$VERSION argocd admin export > backup.yaml
docker run -i -v <KUBE_DIR>:<CONTAINER_KUBE_DIR> --rm quay.io/argoproj/argocd:$VERSION argocd admin import - < backup.yaml
```
(`<KUBE_DIR>` is your local kube config directory, mounted at the path the page gives for the `argocd` user's `.kube` directory.)
If Argo CD runs in a namespace other than the default, pass `-n <namespace>`; `argocd admin export` does not fail in the wrong namespace, so a silent empty backup is possible. The page describes it as all Argo CD data, so treat the file as sensitive.

Cautions when restoring:
- Applications carrying the finalizer `resources-finalizer.argocd.argoproj.io` cascade-delete their resources when deleted; without it, deleting an Application does not delete what it manages. Check which behaviour you have before deleting restored Applications.
- Decide whether you are recovering only the control plane before importing: Applications with automated sync can start syncing as soon as they exist, so check sync policies after import.
- Restore the signing key and other keys in `argocd-secret` from your secret store; they are part of that Secret.

## 3. Upgrading
The upgrading overview defines the rules:
- Patch releases have no breaking changes.
- Minor releases may introduce minor changes with a workaround; when skipping versions, read the notes for every minor you cross (for example v1.3 to v1.5 means both v1.3-v1.4 and v1.4-v1.5).
- Major releases introduce backward-incompatible behaviour; back up your settings with the disaster-recovery procedure first.
The documented upgrade command applies the full manifest set for the target version, non-HA or HA:
```
kubectl apply -n argocd --server-side --force-conflicts -f https://raw.githubusercontent.com/argoproj/argo-cd/<version>/manifests/install.yaml
kubectl apply -n argocd --server-side --force-conflicts -f https://raw.githubusercontent.com/argoproj/argo-cd/<version>/manifests/ha/install.yaml
```
`--server-side --force-conflicts` is required because some CRDs exceed the client-side apply size limit. Apply the whole manifest set even when only the image changes, since manifests may carry parameter changes.

Example of a version-specific note (2.7 to 2.8): Config Management Plugins configured in `argocd-cm` stop working in 2.8 and must be migrated; the containers drop `entrypoint.sh` for `tini`, so deployment manifests must be updated together with the images or pods fail to start; and new RBAC actions (create a Job from a CronJob, a Workflow from a CronWorkflow or WorkflowTemplate) are granted automatically to policies using `*` actions on applications.

## Verify
- [ ] A recent export exists, taken from the correct namespace and not empty.
- [ ] The notes for each minor crossed were read before the upgrade.
- [ ] A restore drill on a scratch cluster reproduced the applications, projects and clusters.

## Checked
2026-11-09. Confirmed against the Argo CD disaster-recovery page (export/import commands, namespace note), upgrading overview (semver rules, server-side apply command, whole-manifest advice, backup before major), the 2.7-2.8 notes (plugin removal, tini, new RBAC actions) and the declarative-setup page (resource names, `part-of` label, secret-type values, finalizer behaviour). Removed: `server.secretkey` and project-token claims, the Redis cache and refresh-storm remarks, the Helm chart upgrade procedure, downgrade rules, version-skew and Kubernetes support claims, `--prune` import behaviour, the CronJob backup design, bootstrap root-app steps, the Argo-managing-itself sync-option advice, and the pinned CRD version.
Method: documentation only; no commands were run.
