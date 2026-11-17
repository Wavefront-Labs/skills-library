---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-disable-reconcilers-and-scope-install
name: external-secrets-operator-disable-reconcilers-and-scope-install
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [security, scopedrbac, reconcilers, crds]
level: advanced
status: docs-checked
description: "Shrink ESO's attack surface by disabling reconcilers and CRDs, or scoping the whole install to one namespace."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/guides/security-best-practices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Reconciliation of `ClusterSecretStore`, `ClusterExternalSecret`, `SecretStore` and `PushSecret` can be turned off in the Helm chart (`processClusterExternalSecret`, `processClusterStore`, `processPushSecret`, `processSecretStore` all `false`) or on the controller with `--enable-cluster-external-secret-reconciler=false`, `--enable-cluster-store-reconciler=false`, `--enable-secret-store-reconciler=false`, `--enable-push-secret-reconciler=false`.

CRD installation is separate: `crds.createClusterExternalSecret`, `createClusterSecretStore`, `createSecretStore`, `createPushSecret`. Disabling a CRD does not disable its reconciler, and the controller logs errors if the CRD is missing but reconciliation is still on. Disabling the SecretStore CRD prevents ExternalSecrets from using namespaced stores, so only do it when you use ClusterSecretStore exclusively.

Namespace-scoped installation:

```yaml
scopedRBAC: true
scopedNamespace: my-namespace
```

creates scoped roles and implicitly disables cluster stores and cluster external secrets.

## Checked

2026-11-03. Claims were read against guides/security-best-practices.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
