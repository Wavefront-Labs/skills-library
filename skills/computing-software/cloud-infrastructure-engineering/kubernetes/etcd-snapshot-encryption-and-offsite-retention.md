---
id: computing-software.cloud-infrastructure-engineering.kubernetes.etcd-snapshot-encryption-and-offsite-retention
name: etcd-snapshot-encryption-and-offsite-retention
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, etcd, snapshot-encryption, snapshot-retention, etcd-backup, object-lock]
level: practitioner
status: docs-checked
description: "Encrypt etcd snapshots before they leave the node, copy them off-site with retention and immutability rules, and prove they can be decrypted and restored."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/", "https://etcd.io/docs/v3.6/op-guide/recovery/", "https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/", "https://github.com/FiloSottile/age", "https://github.com/aws/aws-cli/blob/develop/awscli/customizations/s3/subcommands.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encrypted off-site etcd snapshots

An etcd snapshot contains all Kubernetes API data, including Secrets (as ciphertext only if encryption at rest
is configured on the API server). Treat it like a cluster-admin credential.

## Snapshot, encrypt, upload
```bash
TS=$(date -u +%Y%m%dT%H%M%SZ)
ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key snapshot save /var/backups/etcd-$TS.db
etcdutl snapshot status /var/backups/etcd-$TS.db -w table
age -r age1<public-key> -o /var/backups/etcd-$TS.db.age /var/backups/etcd-$TS.db
sha256sum /var/backups/etcd-$TS.db.age > /var/backups/etcd-$TS.db.age.sha256
aws s3 cp /var/backups/etcd-$TS.db.age s3://<bucket>/<cluster>/ --sse aws:kms --sse-kms-key-id <key-arn>
rm /var/backups/etcd-$TS.db      # remove the plaintext copy once the encrypted copy is uploaded
```
Keep only the public key (age recipient) on nodes; the private identity file lives in a vault used during restores.
Also keep a secure copy of the API server's encryption key, or the Secrets in the snapshot cannot be read.

## Retention
- Lifecycle rule: keep hourly for 2 days, daily for 30 days (separate prefixes make this easy).
- Use your object store's immutability feature (object lock or retention policy) so ransomware or an
  attacker with node credentials cannot delete history.
- A different account or project for the bucket; the node role should be able to write only.

## Verify (monthly)
```bash
aws s3 cp s3://<bucket>/<cluster>/etcd-<ts>.db.age . && sha256sum -c etcd-<ts>.db.age.sha256
age -d -i key.txt -o restore.db etcd-<ts>.db.age
etcdutl snapshot status restore.db -w table
etcdutl snapshot restore restore.db --data-dir /tmp/etcd-test   # on a scratch VM
```
A backup you have never decrypted is not a backup.

## Checked

Date: 2026-10-26. Documentation release: etcd v3.6 docs (etcd-io/website, repository head 2026-10-23); Kubernetes website docs (kubernetes/website main, 2026-10-26); kubeadm source (kubernetes/kubernetes master).

Fixed: removed the claim that a snapshot holds service-account signing inputs (those keys are files on the control plane, not etcd data; unconfirmed). Confirmed: `etcdctl snapshot save` and `etcdutl snapshot status -w table`; Kubernetes docs advise encrypting snapshot files and keeping a secure backup of the API server encryption key; age options `-r` (recipient), `-o` (output), `-d` (decrypt) and `-i` (identity); AWS CLI `s3 cp` options `--sse aws:kms` and `--sse-kms-key-id`; `etcdutl snapshot restore` with `--data-dir`. Removed as unconfirmed: `shred`, the named object-lock modes, the GCS bucket lock reference and the AWS Object Lock page as a source. Retention periods and the separate-account advice are recommendations.

Method: documentation only; no commands were run.
