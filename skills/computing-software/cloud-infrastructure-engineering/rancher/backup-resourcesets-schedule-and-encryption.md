---
id: computing-software.cloud-infrastructure-engineering.rancher.backup-resourcesets-schedule-and-encryption
name: backup-resourcesets-schedule-and-encryption
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [rancher-backup, resourceset, encryption, encryptionconfiguration, schedule, retention]
level: advanced
status: docs-checked
description: "Choose between rancher-resource-set-basic and full, set cron or descriptor schedules and retentionCount, and encrypt backups with an EncryptionConfiguration secret."
sources:
  - https://ranchermanager.docs.rancher.com/reference-guides/backup-restore-configuration/backup-configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Schedule and retention.** A backup is one-time or recurring. `schedule` accepts standard cron such as `"0 * * * *"` or descriptors such as `"@midnight"` and `"@every 1h30m"`. `retentionCount` is how many backup files to keep; older ones beyond the count are deleted, default 10.

**ResourceSets.** Two officially maintained sets are created by the operator, and you can write your own to back up custom applications. `rancher-resource-set-basic` includes **no secrets**, so you must record and redeploy secrets yourself. `rancher-resource-set-full` includes all essential secrets so Rancher keeps running after a restore or migration; the page strongly advises enabling encryption with a strong key, to avoid storing secrets in plain text. The field is `resourceSetName`.

**Encryption.** The operator reads resources through the kube-apiserver, which returns them decrypted. Even with Kubernetes encryption at rest, backup contents would be plaintext. To encrypt, reuse an `EncryptionConfiguration` file (the Kubernetes docs sample works). It must be saved as `encryption-provider-config.yaml` and turned into a secret in `cattle-resources-system`:

```bash
kubectl create secret generic encryptionconfig \
  --from-file=./encryption-provider-config.yaml \
  -n cattle-resources-system
```

The secret name can be anything, but the key must be exactly `encryption-provider-config.yaml`; the UI dropdown only lists secrets that have it. The directive is `encryptionConfigSecretName`. Because the operator does not store the file, keep it safe: a migration needs it to recreate the secret in the new cluster. Encrypted backup files carry a `.enc` suffix.

## Checked

2026-11-04. Checked against the Rancher Manager documentation pages: Backup Configuration. Nothing removed.

Method: documentation only; no commands were run.
