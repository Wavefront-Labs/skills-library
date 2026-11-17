---
id: computing-software.devops-ci-cd.secrets-management.external-secrets-operator-secretstore-and-externalsecret
name: external-secrets-operator-secretstore-and-externalsecret
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, external-secrets-operator, eso, externalsecret, secretstore, clustersecretstore, aws-secrets-manager, vault, gcp-secret-manager, azure-key-vault, irsa, workload-identity, refreshinterval, datafrom, gitops-secrets]
level: practitioner
status: docs-checked
description: "Sync cloud secret managers into Kubernetes with External Secrets Operator: SecretStore vs ClusterSecretStore, ExternalSecret mapping, refresh policies, templates."
sources: ["https://external-secrets.io/latest/introduction/overview/", "https://external-secrets.io/latest/api/externalsecret/", "https://external-secrets.io/latest/provider/aws-secrets-manager/", "https://external-secrets.io/latest/guides/templating/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# External Secrets Operator: SecretStore and ExternalSecret

The controller fetches secrets from an external API (AWS Secrets Manager, Azure Key Vault, and others) and creates Kubernetes `Secret` objects, reconciling them when the source changes. The cluster manifests hold references, not values.

## Resource model
- **SecretStore** (namespaced) says how to access the provider and separates authentication and access from what workloads need. It holds references to Secrets containing credentials for the external API.
- **ClusterSecretStore** is a global, cluster-wide SecretStore referenced from all namespaces, a central gateway to the provider.
- **ExternalSecret** says what to fetch: `spec.secretStoreRef` names the store, `spec.data` syncs individual keys (`secretKey` plus `remoteRef` with `key`, `property`, `version`), `spec.dataFrom` (for example `extract`) pulls all values, and `spec.target` shapes the resulting Secret.
- Reconcile flow: find the store (and skip if missing or if `spec.controller` does not match), build a client from the store's credentials, fetch and decode, create the Secret from `spec.target.template`, and keep it in sync.
- ESO does not manage the lifecycle (rotation) of secrets; that is out of scope.

```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: example
spec:
  refreshInterval: 1h0m0s
  secretStoreRef:
    name: secretstore-sample
    kind: SecretStore
  target:
    name: secret-to-be-created
    creationPolicy: Owner
  data:
    - secretKey: secret-key-to-be-managed
      remoteRef:
        key: provider-key
        property: provider-key-property
```

## Refresh and target behaviour
- `refreshPolicy`: `Periodic` (default) updates every `refreshInterval` (zero means create once); `OnChange` updates only when the ExternalSecret's metadata or spec changes; `CreatedOnce` syncs once per ExternalSecret object. Recreating the ExternalSecret re-syncs and overwrites the target Secret under every `creationPolicy`; only `spec.target.immutable: true` prevents an existing Secret's data being overwritten, so combine it with `CreatedOnce` for generate-once credentials.
- Manual refresh where the policy supports it: annotate the ExternalSecret with `force-sync` set to a changing value.
- `creationPolicy`: `Owner` (default; Secret deleted with the ExternalSecret), `Merge` (merge into an existing Secret), `Orphan` (no owner reference), `None`.
- `deletionPolicy` (when provider data disappears): `Retain` (default), `Delete`, `Merge`.
- Status condition `Ready` with reason `SecretSynced` shows a successful sync.
- Templates: each data value in `spec.target.template` is a Go template; referencing a missing key is an error. Keys containing dashes need `index`. When installing via Helm the template must be escaped. `templateFrom` reads templates from ConfigMaps.

## Access control
- ESO runs with elevated privileges, creating and reading Secrets in all namespaces, so give its provider credentials least privilege. Design stores carefully so developers can read only certain keys in shared environments; admission control (such as OPA or Kyverno) can add fine-grained control.
- AWS provider: use a role (`spec.provider.aws.role`) with fine-grained access to individual secrets. `dataFrom` with a `path` prefix or tag-only filter uses the batch `BatchGetSecretValue` API; searching by name alone falls back to `ListSecrets` plus per-secret fetches, which costs more. For a `ClusterSecretStore` using static credentials, give the namespace in the secret references. The documented IAM example grants `GetSecretValue`, `DescribeSecret`, `ListSecretVersionIds` and `GetResourcePolicy` on a secret ARN pattern.
- AWS secret versions: `version` is a version stage (such as `AWSCURRENT`, `AWSPREVIOUS`) unless prefixed `uuid/`, which means a version ID.

## Verify
- [ ] The ExternalSecret shows Ready with reason `SecretSynced`.
- [ ] Changing the value in the provider and forcing a sync updates the Secret.

## Checked
Method: docs-checked 2026-11-09 against the External Secrets overview, ExternalSecret API, AWS Secrets Manager provider and Advanced Templating pages (templating page read to its opening and first examples).
Removed as unconfirmed: Helm install commands, workload identity (IRSA, Pod Identity) auth example and the `jwt.serviceAccountRef` YAML, ClusterSecretStore `conditions[].namespaceSelector`, the claim that pods using environment variables need restarts and the Reloader annotation, specific AccessDenied and kms:Decrypt gotchas, the 1h refresh recommendation, Argo CD and etcd encryption advice, and the `ClusterExternalSecret` statement.
