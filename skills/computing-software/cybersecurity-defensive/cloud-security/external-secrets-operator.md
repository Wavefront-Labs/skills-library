---
id: computing-software.cybersecurity-defensive.cloud-security.external-secrets-operator
name: external-secrets-operator
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [external-secrets, external-secrets-operator, secrets-store-csi-driver, kubernetes-secrets, vault, aws-secrets-manager, cloud-workload-protection]
level: practitioner
status: docs-checked
description: "Deliver secrets to Kubernetes: External Secrets Operator vs Secrets Store CSI driver, plus Kubernetes guidance on etcd encryption, RBAC and Secret handling."
sources: ["https://external-secrets.io/latest/", "https://secrets-store-csi-driver.sigs.k8s.io/", "https://kubernetes.io/docs/concepts/security/secrets-good-practices/", "https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# External secrets operators and CSI secrets

Keep secrets in an external secret manager and bring them into the cluster, rather than in manifests or source control. Kubernetes guidance: base64 in a Secret manifest is not encryption, so do not share or commit such manifests.

## Options
| | External Secrets Operator (ESO) | Secrets Store CSI Driver |
|---|---|---|
| Mechanism | Operator reads external APIs and injects values into a Kubernetes `Secret`; CRDs `ExternalSecret`, `SecretStore`, `ClusterSecretStore` | Kubelet retrieves secrets via a CSI inline volume (`secrets-store.csi.k8s.io`) and mounts them into authorised pods; config via `SecretProviderClass` |
| Providers | AWS Secrets Manager, Vault, Google Secret Manager, Azure Key Vault and about 40 more | Akeyless, AWS, Azure, Conjur, GCP, OpenBao, Vault |
| Extras | Many consumers can use the resulting Secret | Optional sync to a Kubernetes Secret and auto rotation, both marked alpha |

Because ESO produces a normal Secret, it lands in etcd; the CSI mount alone does not (the Kubernetes page points to the CSI driver for keeping data outside the cluster).

## Illustrative ESO manifest (not taken from the pages, field names unverified here)
```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata: {name: db-creds, namespace: payments}
spec:
  refreshInterval: 1h
  secretStoreRef: {name: aws-sm, kind: SecretStore}
  target: {name: db-creds}
  data:
  - secretKey: password
    remoteRef: {key: prod/payments/db, property: password}
```
The ESO landing page does not document these fields or the SecretStore vs ClusterSecretStore difference; consult its API spec and security best-practices pages.

## Kubernetes hardening (from the Kubernetes pages)
- Secrets are stored unencrypted in etcd by default; configure encryption at rest. It is set via an `EncryptionConfiguration` (`--encryption-provider-config`); the first provider encrypts, all matching providers can decrypt, and `identity` first means no encryption. Existing objects stay unencrypted until rewritten. Encryption at rest does not cover data in mounted volumes.
- RBAC: restrict `get`, `watch`, `list` on Secrets; `list` implicitly lets the holder read contents; anyone who can create a Pod using a Secret can read it. Use short-lived Secrets, audit rules for one user reading many Secrets, and separate namespaces.
- Mount a Secret only in the container that needs it; do not log it. Use TLS between multiple etcd instances.

## Verify
- [ ] First provider in the encryption config is not `identity`; secrets re-written after enabling.
- [ ] No plaintext secrets in Git or Helm values.

## Checked
Method: 2026-11-08 read the ESO and Secrets Store CSI landing pages and the Kubernetes good-practices page; the encrypt-data page was only partly read (first ~100,000 characters via summary; KMS, re-encryption and key rotation sections not covered). Removed unsupported claims: workload-identity/IRSA auth, per-namespace IAM, rotation and Reloader advice, the pros/cons wording, and a SecretStore example. The remaining ExternalSecret manifest is unverified against the pages.
