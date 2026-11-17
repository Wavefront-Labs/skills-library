---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-azure-keyvault-auth
name: external-secrets-operator-azure-keyvault-auth
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [azure-key-vault, authentication, workload-identity, service-principal]
level: practitioner
status: docs-checked
description: "Authenticate ESO to Azure Key Vault with a service principal, managed identity or workload identity and pick the right cloud environmentType."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/provider/azure-key-vault.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Supported clouds via `environmentType`: `PublicCloud`, `USGovernmentCloud`, `ChinaCloud`, `GermanCloud` and `AzureStackCloud`. Whatever the method, the identity needs Key Vault permissions (RBAC or access policies) matching the object types and operations used.

- Service principal: a Kubernetes Secret holding the client ID and either a client secret or a PEM client certificate, referenced from the store.
- Managed identity via AAD Pod Identity: deprecated; if several identities are assigned, choose with `spec.provider.azurekv.identityId`.
- Workload identity: the recommended method. Create a ServiceAccount and the federated credential (the docs use the `azwi` CLI), then either mount the service account into the controller pod with the label `azure.workload.identity/use: "true"`, which grants everyone able to use a store those permissions, or, usually recommended, run the controller without Azure rights and set `serviceAccountRef` in the SecretStore. When the client ID is not known at deploy time, `secretRef` can deliver `clientId` and `tenantId`.

## Checked

2026-11-03. Claims were read against provider/azure-key-vault.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
