---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-namespace-isolation-and-store-conditions
name: external-secrets-operator-namespace-isolation-and-store-conditions
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [security, namespace-isolation, clustersecretstore, conditions]
level: practitioner
status: docs-checked
description: "Keep ESO namespaced resources isolated and restrict a ClusterSecretStore to specific namespaces with conditions."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/guides/security-best-practices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ESO forbids cross-namespace references: an `ExternalSecret` must not reference a `SecretStore` or `Secret` in another namespace, and a `SecretStore` must not reference Secrets elsewhere. Cluster-wide `ClusterSecretStore` and `ClusterExternalSecret` can reach Secrets in all namespaces, so minimise RBAC on them and disable them if they are not needed.

Limit a ClusterSecretStore to certain namespaces with `spec.conditions`, either by label or by explicit list:

```yaml
apiVersion: external-secrets.io/v1
kind: ClusterSecretStore
metadata:
  name: fake
spec:
  conditions:
    - namespaceSelector:
        matchLabels:
          app: frontend
```

Use `namespaces` for a fixed list. Without conditions any namespace may reference the store.

## Checked

2026-11-03. Claims were read against guides/security-best-practices.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
