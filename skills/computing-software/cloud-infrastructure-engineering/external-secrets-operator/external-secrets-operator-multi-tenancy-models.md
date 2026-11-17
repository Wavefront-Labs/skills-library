---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-multi-tenancy-models
name: external-secrets-operator-multi-tenancy-models
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [multi-tenancy, clustersecretstore, secretstore, rbac]
level: advanced
status: docs-checked
description: "Compare shared ClusterSecretStore and per-namespace SecretStore models for multi-tenant ESO deployments."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/guides/multi-tenancy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Start from your organisation: roles (developers, cluster admins), their responsibilities, how they map to Kubernetes RBAC, and how your external provider restricts access (by secret name such as `db/dev/*`, or only per bucket). Not every provider has fine-grained access control. The documented examples are illustrations, not best practice.

Shared ClusterSecretStore: a cluster administrator deploys one ClusterSecretStore with access to the provider; developers reference it from ExternalSecrets but cannot create stores. Every developer can then read every secret, and ESO has no built-in way to limit keys per namespace; use an admission webhook such as Kyverno or Open Policy Agent. Simple, suits one central bucket, but does not scale.

Managed SecretStore per namespace: administrators create one or more SecretStores per namespace, each using its own provider role limited to a few keys. Access is enforced by the external API; the cluster admin only wires it. Suits an external secret administrator who manages secret lifecycle.

## Checked

2026-11-03. Claims were read against guides/multi-tenancy.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
