---
id: computing-software.cloud-infrastructure-engineering.kubernetes.secrets-encryption-at-rest
name: secrets-encryption-at-rest
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, secrets, encryption-at-rest, encryptionconfiguration, kms-v2, envelope-encryption, etcd, key-rotation, aescbc, aesgcm, dek, kek, managed-kubernetes, eks, gke, aks, re-encrypt-secrets, verify-encryption]
level: advanced
status: docs-checked
description: "EncryptionConfiguration and KMS v2 envelope encryption for Secrets at rest, key-rotation mechanics, and the gap between enabling it and actually re-encrypting existing data."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/", "https://kubernetes.io/docs/tasks/administer-cluster/kms-provider/", "https://kubernetes.io/docs/reference/config-api/apiserver-config.v1/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Secrets encryption at rest — closing the "etcd is just base64" gap

**Goal:** make a raw etcd snapshot or disk read useless to an attacker, and know
that flipping on encryption does not retroactively encrypt what's already
stored. RBAC-level access control to Secrets and the operational advice to source
them from a vault are in
`computing-software.cloud-infrastructure-engineering.kubernetes.k8s-rbac-and-security`;
etcd's own access/TLS hardening is in
`computing-software.cloud-infrastructure-engineering.kubernetes.etcd-security-hardening`.

## 1. Without this, Secrets are not encrypted — only base64-encoded
`kubectl get secret -o jsonpath='{.data.password}' | base64 -d` recovers the
plaintext from the API; `etcdctl get /registry/secrets/... ` on the raw store
recovers it too, in cleartext base64, to anyone with etcd access (a backup file,
a volume snapshot, a compromised etcd node). Base64 is an encoding, not
encryption — EncryptionConfiguration is the only thing standing between an etcd
compromise and plaintext Secrets.

## 2. `EncryptionConfiguration` mechanics
```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
- resources: [secrets]        # can also list configmaps, or "*.<group>" (wildcards need v1.27+)
  providers:
  - kms: {apiVersion: v2, name: myprovider, endpoint: unix:///var/run/kmsplugin/socket.sock, timeout: 3s}
  - identity: {}               # fallback: NO encryption — order matters, see §3
```
Passed to `kube-apiserver` via `--encryption-provider-config`. With
`--encryption-provider-config-automatic-reload=true` the file is polled every minute and key
changes apply without an API server restart. Without `--encryption-provider-config` there is no
encryption at rest.

## 3. Provider order governs both write and read
- **Write path:** the apiserver encrypts new/updated objects with the **first**
  provider listed.
- **Read path:** on read, each provider that matches the stored data attempts to decrypt it in
  list order; if none can, an error is returned. This is how key rotation and migration work
  (add the new provider or key first so it is used for new writes, keep the old one later so
  existing ciphertext still decrypts). An `identity: {}` provider listed **first** means new
  writes are stored unencrypted (existing encrypted data is not rewritten automatically), while
  listed **last** it only lets unencrypted data keep being read until you re-encrypt and then
  remove it.

## 4. KMS v2 vs. the deprecated KMS v1 / static key providers
- **KMS v2** (stable since 1.29): envelope encryption. The API server derives a single-use data
  encryption key (DEK) for every write from a secret seed (a key derivation function), and the
  seed is protected by a key encryption key (KEK) in the remote KMS, reached through a KMS plugin
  over a gRPC UNIX socket on the control-plane host. The seed rotates when the KEK rotates.
  The docs say it has significantly better performance than v1, and KMS v2 does not support
  `cachesize`: unwrapped DEKs stay cached in the clear in the API server.
- **KMS v1** is deprecated since 1.28 and disabled by default since 1.29. The static providers
  (`aescbc`, `aesgcm`, `secretbox`) keep key material in the config file on the control-plane
  host; the docs rate `aescbc` as not recommended (padding-oracle weakness) and say `aesgcm`
  needs keys rotated every 200,000 writes. Prefer a KMS v2 plugin so the KEK never sits on the
  API server host.

## 5. Enabling it does NOT encrypt what's already there
This is the single most common gap: turning on `EncryptionConfiguration`
encrypts objects **only as they are next written**. Every existing Secret stays
in its previous (often plaintext) form in etcd until something writes it again.
```bash
kubectl get secrets --all-namespaces -o json | kubectl replace -f -
```
This is the documented sweep (run it as an administrator and retry on conflicting writes; it is
safe to repeat). Run it after rolling out encryption, and after any key rotation that makes a
new key first, because old objects are not re-encrypted until they are rewritten.

## 6. Verifying it actually took effect
```bash
ETCDCTL_API=3 etcdctl get /registry/secrets/default/my-secret \
  --cert=... --key=... --cacert=... | hexdump -C | head
```
Encrypted output starts with a provider-specific prefix (`k8s:enc:kms:v2:...`
for KMS v2); plaintext/base64 output means that Secret was never rewritten since
encryption was enabled — the sweep in §5 was skipped or missed it.

## Gotchas
- There is no fallback to plaintext for encrypted data: the `identity` provider only helps for
  data that was stored unencrypted. A DEK that is not in the API server's cache needs a call to
  the KMS to unwrap, while cached DEKs decrypt indefinitely without one. The API server polls
  the plugin's `Status` about every minute (every 10 seconds when it is unhealthy), and
  `/healthz/kms-providers` reports health; monitor the plugin.
- `cachesize` is a KMS v1 setting; KMS v2 does not support it.
- Backups/snapshots taken *before* encryption was enabled remain in their
  original (often plaintext) form forever — rotating a backup retention policy or
  re-running a fresh backup after the §5 sweep is the only fix.

## Verify
- [ ] `EncryptionConfiguration` lists an external KMS v2 provider first (not
      `identity`), confirmed via `kube-apiserver` flags or provider console.
- [ ] A raw `etcdctl get` on a Secret shows an encrypted prefix, not plaintext
      base64 — spot-check several, including old ones predating the last change.
- [ ] The full-Secret rewrite sweep ran after initial enablement **and** after
      every subsequent key rotation.
- [ ] KMS plugin/endpoint has its own availability monitoring independent of
      general apiserver health checks.
- [ ] Backup/snapshot retention accounts for pre-encryption snapshots that may
      still hold plaintext.

## Checked

Checked 2026-10-26 against Kubernetes documentation v1.37 (kubernetes/website commit 2026-10-25, feature gate pages, KMS and encryption task pages). Confirmed: `--encryption-provider-config` and `--encryption-provider-config-automatic-reload` (polled every minute); provider order for writes and reads; `identity` first stores new data unencrypted without rewriting old data; wildcards need v1.27+; KMS v2 stable since v1.29, KMS v1 deprecated since v1.28 and disabled by default since v1.29; single-use DEKs derived from a seed; KMS v2 does not support `cachesize`; the `kms` v2 provider fields `apiVersion`, `name`, `endpoint`, `timeout` (default 3s); the `kubectl get secrets ... | kubectl replace -f -` sweep; prefix `k8s:enc:kms:v2:`; provider table remarks on `aescbc` and `aesgcm`; plugin `Status` polling and `/healthz/kms-providers`. Wrong and fixed: the example KMS provider omitted `apiVersion: v2` (which defaults to the deprecated v1) and used `cachesize`, which KMS v2 rejects; DEKs are per encryption, not per resource. Removed as unconfirmed: the EKS and GKE remarks, the ConfigMap overhead figure, the `kubectl annotate` rewrite trick and the "reads fail while the plugin is down" claim.

Method: documentation only; no commands were run.
