---
id: computing-software.cloud-infrastructure-engineering.kubernetes.decrypt-secrets-identity-provider
name: decrypt-secrets-identity-provider
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, secrets-encryption-at-rest, identity-provider, disable-encryption, encryptionconfiguration, etcd]
level: practitioner
status: docs-checked
description: "Turn encryption at rest off safely by moving the identity provider first, rewriting all Secrets to plaintext, and only then removing the old keys."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/decrypt-data/", "https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/#decrypting-all-data"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Decrypting back to plaintext

Reasons: moving to a different KMS, or recovering from a broken KMS plugin. The key rule: never
remove a provider while data encrypted with it remains in etcd, or those objects become unreadable.

## Steps
1. Put `identity` first, keep the old provider second so existing data can still be read:
   ```yaml
   apiVersion: apiserver.config.k8s.io/v1
   kind: EncryptionConfiguration
   resources:
   - resources: [secrets]
     providers:
     - identity: {}
     - aescbc:
         keys: [{name: key1, secret: <base64>}]
   ```
2. Apply the same file on every control-plane node, one API server at a time, and restart each
   kube-apiserver (or, with `--encryption-provider-config-automatic-reload=true`, wait for the
   file poll, which runs every minute).
3. Rewrite every Secret so it is stored with the first provider (plaintext):
   ```bash
   kubectl get secrets -A -o json | kubectl replace -f -
   ```
4. Check etcd. Once every encrypted resource has been rewritten, remove the encryption settings
   from kube-apiserver (`--encryption-provider-config` and, if set,
   `--encryption-provider-config-automatic-reload`) and restart each API server again, in turn.

## Check what etcd holds
```bash
ETCDCTL_API=3 etcdctl ... get /registry/secrets/default/my-secret | hexdump -C | head
```
Encrypted data starts with `k8s:enc:aescbc:v1:key1` (or `k8s:enc:kms:v2:<name>`); a decrypted
Secret has no `k8s:enc:` prefix and its field values are readable in the dump.

## Gotchas
- `kubectl replace` can fail on conflicting writes; the docs say to retry (the command is safe to repeat).
- If no provider can read stored data, the API server returns an error for that resource, so
  keep the old provider (or KMS) until the rewrite has finished; this procedure only works while
  the old provider still decrypts.
- Backups or etcd snapshots taken while data was encrypted still need the old key to be read.

## Checked

Checked 2026-10-26 against Kubernetes documentation v1.37 (kubernetes/website commit 2026-10-25, feature gate pages, KMS and encryption task pages) (`decrypt-data.md`, `encrypt-data.md`). Confirmed: put `identity` first and keep the old provider after it; deploy to each API server in turn with the same configuration; `kubectl get secrets --all-namespaces -o json | kubectl replace -f -` forces decryption and conflicts are retried; then remove `--encryption-provider-config` and `--encryption-provider-config-automatic-reload` and restart again; automatic reload polls every minute; the `k8s:enc:aescbc:v1:` prefix; an unreadable resource returns an error. Removed as unconfirmed: the description of plaintext bytes in the etcd dump.

Method: documentation only; no commands were run.
