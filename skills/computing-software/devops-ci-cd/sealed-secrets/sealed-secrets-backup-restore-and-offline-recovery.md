---
id: computing-software.devops-ci-cd.sealed-secrets.sealed-secrets-backup-restore-and-offline-recovery
name: sealed-secrets-backup-restore-and-offline-recovery
category: computing-software
field: devops-ci-cd
product: sealed-secrets
tags: [sealed-secrets, backup, restore, disaster-recovery, recovery-unseal, private-key, kubectl]
level: advanced
status: docs-checked
description: "Back up Sealed Secrets sealing keys, restore them after a disaster, and decrypt files offline with kubeseal --recovery-unseal."
sources: ["https://github.com/bitnami/sealed-secrets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sealed secrets backup restore and offline recovery

Without the sealing private key no SealedSecret can be decrypted; there are no backdoors. If both the key Secrets and the live unsealed Secrets are lost, you must create new passwords and reseal everything.

Backup from an account with suitable access:

```bash
kubectl get secret -n kube-system -l sealedsecrets.bitnami.com/sealed-secrets-key -o yaml >main.key
echo "---" >> main.key
kubectl get secret -n kube-system sealed-secrets-key -o yaml >>main.key
```

The second command is only needed if you ever ran a version older than 0.9.x. The file contains public and private keys and must be guarded accordingly. Recreate the backup after each key renewal, otherwise it cannot decrypt secrets sealed with newer keys.

Restore: put the Secrets back before starting the controller, or, if it is already running, replace the freshly created ones and restart it.
- Helm deployment: `kubectl apply -f main.key` then `kubectl delete pod -n kube-system -l app.kubernetes.io/name=sealed-secrets`
- Manifest deployment: same apply, then delete pods with `-l name=sealed-secrets-controller`

Offline decryption, for when the cluster is down and restoring into a new controller is impractical (the README does not recommend using sealed secrets as long-term secret storage):

```bash
kubeseal --recovery-unseal --recovery-private-key file1.key,file2.key
```

It takes a sealed secrets file and the comma-separated backup key files.

## Checked
Date: 2026-11-04. Documentation: bitnami-labs/sealed-secrets README (raw markdown, main branch), FAQ sections on backup, cluster loss and offline decryption.
Confirmed: backup commands, 0.9.x note, renewal note, both restore variants and labels, `--recovery-unseal --recovery-private-key`.
Removed: nothing.
Method: documentation only; no commands were run.
