---
id: computing-software.cloud-infrastructure-engineering.cert-manager.backup-and-restore
name: backup-and-restore
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [backup, restore, velero, disaster-recovery, migration, owner-references]
level: advanced
status: docs-checked
description: "Back up and restore cert-manager resources: config-only kubectl backup, Secret ordering, what to exclude, and the Velero two-step restore."
sources:
  - https://cert-manager.io/docs/devops-tips/backup/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Config-only: `kubectl get --all-namespaces -ojson issuer,clusterissuer,cert > backup.json`. Certificate Secrets are not included, so restoring causes reissuance. When moving clusters also copy referenced Secrets: CA root (`issuer.spec.ca.secretName`), Vault (`auth.tokenSecretRef`, `auth.appRole.secretRef`), ACME (`privateKeySecretRef` plus DNS01 provider Secrets). Restore after installing cert-manager with a `jq` filter that strips `uid` and `resourceVersion` from top-level metadata, then `kubectl apply -f -`; `ownerReferences` UIDs are kept.

Full backup (DR or migration):
- Restore Secrets before Certificates, and before Ingresses when using ingress-shim, or you get needless reissuance.
- Exclude `Order`, `Challenge` and `CertificateRequest`: their status is not restored, so fulfilled requests look unfulfilled.
- Usually exclude ingress-shim Certificates: restored owner references point at old Ingress UIDs.
- Tested only with Velero v1.12.2 and cert-manager v1.13.2.

Velero backup: `velero backup create full-backup --include-namespaces cert-manager,default --include-cluster-resources=true --exclude-resources challenges.acme.cert-manager.io,orders.acme.cert-manager.io,certificaterequests.cert-manager.io`. Velero restores pods before RBAC, so the restore can hang on the webhook pod; restore cert-manager RBAC first or restart the deployments. Velero does not restore owner references, so restore in two steps: `velero restore create --from-backup full-backup --exclude-resources certificates.cert-manager.io`, wait for auto-generated Certificates, then run the restore again without the exclusion.

CertificateRequests are not worth backing up. Since v1.3.0 a webhook sets immutable identity fields from the creator, so restored ones are likely wrong. Without a CertificateRequest some Certificate spec changes may not trigger reissuance.

## Checked

2026-11-03: Confirmed against the Backup and Restore page: the `kubectl get ... issuer,clusterissuer,cert` backup, Secrets to copy per issuer type, the `jq` restore filter and kept `ownerReferences`, restore ordering, excluding Orders, Challenges and CertificateRequests, ingress-shim owner reference caveat, Velero v1.12.2 / cert-manager v1.13.2 test note, the Velero backup and two-step restore commands, the RBAC-before-pods hang, and the v1.3.0 identity fields. Nothing removed.

Method: documentation only; no commands were run.
