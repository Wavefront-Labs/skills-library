---
id: computing-software.cloud-infrastructure-engineering.kubernetes.external-secrets-operator-patterns
name: external-secrets-operator-patterns
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, external-secrets-operator, eso, secretstore, clustersecretstore, externalsecret, pushsecret, refreshinterval, gitops, secret-management, vault, aws-secrets-manager, azure-key-vault, gcp-secret-manager, deletion-policy, templating]
level: practitioner
status: docs-checked
description: "Sync secrets into Kubernetes with External Secrets Operator: SecretStore vs ClusterSecretStore scope, ExternalSecret refresh/templating, deletionPolicy, and when ESO beats sealed-secrets."
sources: ["https://external-secrets.io/latest/api/externalsecret/", "https://external-secrets.io/latest/api/clustersecretstore/", "https://external-secrets.io/latest/api/pushsecret/", "https://external-secrets.io/latest/provider/aws-access/", "https://external-secrets.io/latest/introduction/stability-support/", "https://github.com/external-secrets/external-secrets/blob/main/apis/externalsecrets/v1/externalsecret_types.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# External Secrets Operator — the live-sync answer to GitOps secrets

**Model, contrasted with Sealed Secrets:** nothing secret is ever committed to git at
all — an `ExternalSecret` CR in git is just a *pointer* ("fetch key `prod/db/password`
from this backend, materialize it as Secret `db-creds`"); the actual value lives only
in the external store (Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret
Manager, 1Password, etc.) and in the resulting in-cluster `Secret`. Rotating the
credential in the backend propagates automatically on the next refresh — no reseal,
no recommit. Trade-off: it requires running and trusting a real secret store, where
Sealed Secrets requires nothing but the cluster itself.

## 1. Core objects
```yaml
apiVersion: external-secrets.io/v1
kind: ClusterSecretStore           # or SecretStore (namespace-scoped)
metadata: {name: aws-backend}
spec:
  provider:
    aws: {service: SecretsManager, region: us-east-1, auth: {jwt: {serviceAccountRef: {name: eso-irsa, namespace: external-secrets}}}}   # namespace is required in a ClusterSecretStore
---
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata: {name: db-creds, namespace: payments}
spec:
  refreshInterval: 1h
  secretStoreRef: {name: aws-backend, kind: ClusterSecretStore}
  target: {name: db-creds, creationPolicy: Owner}
  data:
    - secretKey: password
      remoteRef: {key: prod/db, property: password}
```
- **`SecretStore`** is namespace-scoped (a team's own store config); **`ClusterSecretStore`**
  is cluster-scoped and can be referenced by `ExternalSecret`s in any namespace (set
  `kind: ClusterSecretStore` in `secretStoreRef`) —
  default to `SecretStore` per-namespace unless you deliberately want one shared
  backend config for the whole cluster (simpler ops, but every namespace that can
  create an `ExternalSecret` referencing it can potentially reach everything that
  store's auth allows — scope the store's own IAM/Vault-policy tightly, don't rely
  on Kubernetes RBAC alone to limit blast radius).
- `auth` should use workload identity (IRSA on AWS, Workload Identity on GCP, Vault
  Kubernetes auth) — a long-lived static credential for ESO itself defeats the
  point of pulling secrets from a managed store in the first place.

## 2. Refresh, templating, and multi-value secrets
- `refreshInterval` governs polling; `0` creates the Secret once and never updates it (used
  for values that genuinely never rotate, rare for real secrets); `refreshPolicy` can also be
  `CreatedOnce` or `OnChange`. A credential
  rotated in the backend won't reach the cluster faster than this interval — size it
  against your rotation SLA, not just "small number, more API calls."
- `dataFrom: [{extract: {key: prod/db}}]` pulls an entire JSON secret's keys at once
  instead of enumerating each field under `data:` — less repetition, but a new key
  appearing in the backend secret appears automatically in the K8s Secret too; make
  sure anything consuming it doesn't assume a fixed key set.
- `target.template` renders the final Secret's data through Go templates
  (combining multiple backend fields into one connection string, base64-decoding,
  etc.).

## 3. Ownership and deletion policy
- `target.creationPolicy: Owner` (default) means ESO owns the Secret lifecycle —
  deleting the `ExternalSecret` deletes the Secret too (owner reference). `Orphan` creates the
  Secret without an owner reference so it stays after the `ExternalSecret` is deleted. `Merge`,
  `CreateOrMerge` and `None` let an existing Secret be augmented or left alone,
  useful when another controller or a Helm chart also writes fields into the same
  Secret object, but then nobody fully owns it — avoid unless genuinely needed.
- `target.deletionPolicy` (`Retain` default, `Delete`, `Merge`) is a different setting: it
  says what happens to the Secret when all the provider secrets have been deleted. It does not
  control what happens when the `ExternalSecret` itself is deleted; for that, use
  `creationPolicy: Orphan`. Recreating an `ExternalSecret` (for example a GitOps prune and
  re-apply) re-syncs and overwrites the target keys; the docs say only `target.immutable: true`
  prevents an existing Secret's data being overwritten. Think through prune-driven deletion before
  enabling `prune: true` on the directory containing `ExternalSecret`s.

## 4. `PushSecret` — the reverse direction
`PushSecret` (a namespaced CRD) pushes an in-cluster Secret *out* to the backend store —
used for operator-generated credentials (e.g. a database operator's generated
password) that need to exist in Vault/AWS for other non-Kubernetes consumers, the
mirror image of the normal pull flow. Confirm availability/stability in your
installed ESO version before depending on it for anything critical.

## Gotchas
- Alert on the `ExternalSecret`'s `Ready` condition (and its refresh time) rather than only on
  the Secret existing, so a store that stops syncing is noticed.
- A `ClusterSecretStore` without namespace guardrails (`spec.conditions` with
  `namespaceSelector`, `namespaces` or a regex) means any namespace can request any secret
  the store's backend credentials can reach — this is the main operational risk specific to ESO vs. Sealed Secrets'
  purely local trust model.
- Two things syncing into the same Secret name (an `ExternalSecret` with
  `creationPolicy: Merge` and something else) produces a field-ownership fight
  similar to the drift patterns in
  `computing-software.cloud-infrastructure-engineering.kubernetes.drift-detection-and-reconciliation`.

## Verify
- [ ] Rotating the credential in the backend store propagates into the cluster
      Secret within one `refreshInterval`, verified end to end at least once.
- [ ] The `ExternalSecret`'s auth uses workload identity, not a static key checked
      into the store config.
- [ ] `deletionPolicy`/`creationPolicy` match intent — test what actually happens to
      the live Secret when the `ExternalSecret` is deleted.
- [ ] A `SecretStore`/`ClusterSecretStore`'s backend permissions are scoped to only
      the secrets that namespace/cluster actually needs, not a blanket read-all.

## Checked
2026-10-26. Checked against the External Secrets Operator docs and API types (repository external-secrets/external-secrets, last push 2026-10-23). Confirmed: `external-secrets.io/v1` apiVersion for ExternalSecret and stores; `refreshInterval` of zero creates the Secret once and never refreshes; `refreshPolicy` values CreatedOnce, Periodic and OnChange; `creationPolicy` values Owner, Orphan, Merge, None and CreateOrMerge; `deletionPolicy` values Delete, Merge and Retain (default Retain) which apply when the provider secrets are deleted, not when the ExternalSecret is deleted; ExternalSecret condition type `Ready`; ClusterSecretStore namespace restriction through `spec.conditions` (`namespaceSelector`, `namespaces`, regex); AWS `auth.jwt.serviceAccountRef` needs a `namespace` in a ClusterSecretStore; PushSecret is a namespaced CRD. Corrected: the meaning of `deletionPolicy`, the creationPolicy list, the `SecretSynced` condition name and the missing serviceAccount namespace in the example. Removed as unconfirmed: the claims about auth failures leaving stale Secrets and the Helm `tpl` comparison.
Method: documentation only; no commands were run.
