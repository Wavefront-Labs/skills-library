---
id: computing-software.cryptography-implementation.key-management.kubernetes-secrets-encryption-at-rest
name: kubernetes-secrets-encryption-at-rest
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, kubernetes-secrets-encryption, kubernetes, etcd, encryptionconfiguration, kms-v2, envelope-encryption, secrets-at-rest, key-rotation]
level: practitioner
status: docs-checked
description: "Encrypt Kubernetes Secrets in etcd with EncryptionConfiguration and KMS v2: provider order, rewriting existing secrets, verifying in etcd and rotating keys."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/", "https://kubernetes.io/docs/tasks/administer-cluster/kms-provider/", "https://kubernetes.io/docs/concepts/security/secrets-good-practices/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubernetes Secrets encryption at rest

By default Secrets are only base64 in etcd. Anyone with etcd or its backups reads them.

## Configuration
```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources: ["secrets"]
    providers:
      - kms:
          apiVersion: v2
          name: cloud-kms
          endpoint: unix:///var/run/kmsplugin/socket.sock
          timeout: 3s
      - identity: {}          # read old plaintext data during migration; remove later
```
kube-apiserver flags: `--encryption-provider-config=/etc/kubernetes/enc.yaml`
(`--encryption-provider-config-automatic-reload=true` to pick up changes without restart).

- The **first** provider encrypts new writes; all listed providers are tried for reads.
- KMS v2 (stable since 1.29) encrypts with DEKs derived from a secret seed, and the seed is rotated when the KEK is rotated. The page rates `aescbc` Weak and says `aesgcm` must be rotated every 200,000 writes; prefer KMS v2.

## Encrypt existing Secrets
```
kubectl get secrets --all-namespaces -o json | kubectl replace -f -
```
New writes go through the first provider; this rewrites every Secret.

## Verify in etcd
```
ETCDCTL_API=3 etcdctl get /registry/secrets/default/my-secret --print-value-only | head -c 32 | xxd
```
Encrypted values start with `k8s:enc:kms:v2:<name>:` (or `k8s:enc:aescbc:v1:` etc.). Plaintext shows readable YAML.

## Rotation
1. Rotate the key in the KMS (KMS v2 picks up the new key ID automatically) or add a new local key as the first
   entry.
2. Rewrite all Secrets (command above).
3. Remove the old key from the config only after the rewrite and after confirming backups are re-encrypted or expired.

## Gotchas
- Removing `identity` or an old key before rewriting makes existing Secrets unreadable.
- etcd backups taken before encryption still contain plaintext; rotate secrets that were in them.
- Extend `resources` to `configmaps` or custom resources that hold secrets if needed.

## Verify
- [ ] etcd shows the `k8s:enc:kms:v2` prefix for a sample of Secrets.
- [ ] apiserver metrics show no KMS errors; a KMS outage test confirms behaviour.

## Checked

2026-10-31. Confirmed against the Kubernetes encrypt-data and kms-provider pages: provider order, identity provider, 3s timeout default, automatic-reload flag, `k8s:enc:kms:v2:` prefix, KMS v2 stable since 1.29, aesgcm 200,000 writes. Removed: managed-cluster (EKS/GKE/AKS) claim and the claim that KMS is not called per write.
Method: documentation only; no commands were run.
