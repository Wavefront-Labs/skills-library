---
id: computing-software.cloud-infrastructure-engineering.kubernetes.etcd-snapshot-security
name: etcd-snapshot-security
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, etcd-security, snapshot-security, etcd-backup, encryption-at-rest]
level: practitioner
status: docs-checked
description: "Protect etcd snapshots, which contain every Secret: encryption of backups, storage access controls, separating the encryption key, retention and access auditing."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/", "https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/", "https://github.com/FiloSottile/age"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Securing etcd snapshots

An etcd snapshot is the whole cluster state: every Secret, RBAC object and configuration object.
Possessing it is close to cluster-admin (Kubernetes docs: access to etcd is equivalent to root in the cluster).

## Encryption layers
1. **Secrets encryption at rest** in the apiserver (aescbc/KMS): Secret values are encrypted in
   the snapshot. Other objects (ConfigMaps, CRs) remain plaintext unless included.
2. **Encrypt the snapshot file** before it leaves the node:
   ```bash
   etcdctl ... snapshot save /var/backups/etcd-$(date +%F).db
   age -r age1... -o etcd-$(date +%F).db.age /var/backups/etcd-$(date +%F).db && rm /var/backups/etcd-*.db
   ```
   or use object storage server-side encryption with a customer-managed KMS key.
3. **Store the apiserver EncryptionConfiguration key separately** from snapshots. Same bucket =
   no protection; different account/KMS = an attacker needs both.

## Access control
- Dedicated bucket with write-only credentials for the backup job (no read/delete), object lock
  or versioning for ransomware resistance.
- Restore role separate and audited; access logging on the bucket.
- Local snapshot directories readable by root only and not on shared volumes.

## Retention
Short retention for frequent snapshots; longer for daily/weekly. Old snapshots contain old
credentials that may still be valid (long-lived tokens, unrotated passwords).

## Verify
- Attempt to read a snapshot with the backup job's credentials: must fail.
- Restore drill uses the separately stored key and succeeds.
- On a restored scratch copy, read a Secret key with `etcdctl get` and check the stored value starts with
  `k8s:enc:aescbc:v1:` (the prefix the Kubernetes docs say marks aescbc-encrypted data).

## Checked

Date: 2026-10-26. Documentation release: etcd v3.6 docs (etcd-io/website, repository head 2026-10-23); Kubernetes website docs (kubernetes/website main, 2026-10-26); kubeadm source (kubernetes/kubernetes master).

Confirmed: the Kubernetes etcd page says to encrypt snapshot files because they hold all Kubernetes state; the encryption-at-rest page lists the aescbc and KMS providers, says other resources (not only Secrets) can be added, that a lost key means encrypted resources cannot be recovered, and that stored values carry the prefix `k8s:enc:aescbc:v1:` (checked with `etcdctl get ... | hexdump -C`); age usage. Removed as unconfirmed: the claim that a snapshot holds ServiceAccount signing data, `shred`, the `strings | grep` check, and the specific permission bits. The retention and bucket access advice are recommendations.

Method: documentation only; no commands were run.
