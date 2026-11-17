---
id: computing-software.cloud-infrastructure-engineering.keda.authentication-azure-key-vault
name: authentication-azure-key-vault
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [azure-key-vault, azurekeyvault, vaulturi, azure-workload, azure-clouds]
level: advanced
status: docs-checked
description: "Read scaler secrets from Azure Key Vault using pod identity or an Azure AD application, including sovereign and private cloud settings."
sources:
  - https://keda.sh/docs/2.17/concepts/authentication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Values pulled from the vault are merged with any other sources in the same TriggerAuthentication, so Key Vault can be combined with env or secretTargetRef parameters.
Use the `azureKeyVault` key in a TriggerAuthentication or ClusterTriggerAuthentication.

Required: `vaultUri` and a `secrets` list mapping each Key Vault secret `name` (optional `version`) to an authentication `parameter`.

Two ways to authenticate to the vault:
1. Pod identity: `podIdentity.provider` set to `azure-workload` (the page also mentions `azure`). The identity binding must be applied in the KEDA namespace. Optional `identityId`.
2. An Azure AD application: provide `credentials.clientId`, `credentials.tenantId` and `credentials.clientSecret.valueFrom.secretKeyRef` naming a Kubernetes Secret and key. That secret must be in the same namespace as the authentication resource.

Either way, grant "read secret" permission to the managed identity or application on the Key Vault.

Cloud selection: the optional `cloud.type` is `AzurePublicCloud`, `AzureUSGovernmentCloud`, `AzureChinaCloud`, `AzureGermanCloud` or `Private`. For `Private` (Azure Stack Hub or air-gapped clouds) you must also set `keyVaultResourceURL` and `activeDirectoryEndpoint`.

```yaml
azureKeyVault:
  vaultUri: {key-vault-address}
  secrets:
  - parameter: {param-name-used-for-auth}
    name: {key-vault-secret-name}
```

## Checked

2026-11-03. Confirmed on the 2.17 Authentication page: azureKeyVault fields, pod identity providers, clientId/tenantId/clientSecret, cloud types and the Private-cloud fields.

Method: documentation only; no commands were run.
