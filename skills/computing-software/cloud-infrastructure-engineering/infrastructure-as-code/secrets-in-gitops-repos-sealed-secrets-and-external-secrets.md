---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.secrets-in-gitops-repos-sealed-secrets-and-external-secrets
name: secrets-in-gitops-repos-sealed-secrets-and-external-secrets
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, gitops, secrets-in-iac, sealed-secrets, external-secrets, eso, kubeseal, sops]
level: practitioner
status: docs-checked
description: "Keep Kubernetes secrets out of Git in plain text: encrypt with Sealed Secrets (kubeseal) or reference a secret store with External Secrets Operator, and know when to choose each."
sources: ["https://github.com/bitnami-labs/sealed-secrets", "https://external-secrets.io/latest/api/externalsecret/", "https://external-secrets.io/latest/provider/aws-secrets-manager/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secrets in GitOps repos: Sealed Secrets and External Secrets

## Option 1: Sealed Secrets (encrypted in Git)
A controller in the cluster holds a private key; you encrypt with its public key.
```bash
echo -n 'S3cr3t' | kubectl create secret generic db-creds -n orders \
  --dry-run=client --from-file=password=/dev/stdin -o json \
| kubeseal --controller-namespace kube-system > apps/overlays/prod/orders/db-creds.sealed.json
git add apps/overlays/prod/orders/db-creds.sealed.json
```
The `SealedSecret` is safe to commit; the controller decrypts it into a normal `Secret`.
- Scope: default `strict` binds to name+namespace (renaming breaks decryption); `--scope namespace-wide` or `cluster-wide` loosens it.
- Offline sealing: `kubeseal --fetch-cert >mycert.pem`, then `kubeseal --cert mycert.pem`.
- **Back up the controller's key** (`kubectl get secret -n kube-system -l sealedsecrets.bitnami.com/sealed-secrets-key -o yaml`) into your vault — losing it means re-sealing every secret. Sealing keys are renewed every 30 days by default (a new key is appended; older ones still unseal).

## Option 2: External Secrets Operator (reference in Git, value in a store)
```yaml
apiVersion: external-secrets.io/v1
kind: ClusterSecretStore
metadata: {name: aws-sm}
spec:
  provider:
    aws:
      service: SecretsManager
      region: eu-west-1
      # auth: add the block from the ESO AWS provider page for your cluster
---
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata: {name: db-creds, namespace: orders}
spec:
  refreshInterval: 1h
  secretStoreRef: {kind: ClusterSecretStore, name: aws-sm}
  target: {name: db-creds}
  data:
    - secretKey: password
      remoteRef: {key: prod/orders/db, property: password}
```
Providers: AWS Secrets Manager/Parameter Store, Vault, Azure Key Vault, GCP Secret Manager, 1Password, etc.
Rotation in the store propagates at `refreshInterval` (pods still need a restart or a reloader).
Match the `apiVersion` to what your installed ESO release serves.

## Choosing
| | Sealed Secrets | External Secrets | SOPS (Flux) |
|---|---|---|---|
| Source of truth | Git (ciphertext) | external store | Git (ciphertext) |
| Rotation | re-seal + commit | in the store | re-encrypt + commit |
| Needs a store | no | yes | KMS/age key |
| Audit of reads | no | store's audit log | KMS log |

Organisations with a central secret store → ESO. Small/air-gapped clusters → Sealed Secrets or SOPS+age.

## Gotchas
- Never `kubectl create secret` then commit `-o yaml` output — base64 is not encryption.
- ESO needs IAM permissions scoped to the needed paths only, per namespace store if possible.
- Pre-commit secret scanning (gitleaks) still matters — catches plain secrets before they land.

## Verify
- [ ] The Git repo contains no `kind: Secret` with `data:` (scan in CI).

## Checked
2026-11-01. Confirmed in the Sealed Secrets README: `strict` default scope and name+namespace binding, `--scope` with `namespace-wide`/`cluster-wide`, `--controller-namespace`, `--fetch-cert` and `--cert`, the key label `sealedsecrets.bitnami.com/sealed-secrets-key`, 30-day key renewal. Confirmed in the ESO ExternalSecret and AWS Secrets Manager pages: `external-secrets.io/v1`, `refreshInterval`, store/`remoteRef` layout. Removed: `kubeseal --format yaml`, the `jwt`/`serviceAccountRef` auth block, the `v1beta1` remark and the `kubectl get secret` check.
Method: documentation only; no commands were run.
