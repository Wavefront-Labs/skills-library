---
id: computing-software.cloud-infrastructure-engineering.terraform.azurerm-oidc-authentication
name: azurerm-oidc-authentication
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, azure-oidc, use-oidc, azurerm, workload-identity-federation, github-actions, provider-authentication]
level: practitioner
status: docs-checked
description: "Authenticate azurerm (provider and backend) from CI with OIDC workload identity federation: app/federated credential setup, use_oidc, ARM_* env vars, and errors."
sources: ["https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/service_principal_oidc", "https://developer.hashicorp.com/terraform/language/backend/azurerm", "https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# azurerm with OIDC (no client secrets)

## Azure side
1. App registration (or user-assigned managed identity) for the pipeline.
2. Federated credential: issuer `https://token.actions.githubusercontent.com`,
   a subject that matches the token your workflow presents (entra matches issuer,
   subject and audience case-sensitively), audience `api://AzureADTokenExchange`.
3. Role assignments on the subscription/resource group (e.g. Contributor) and
   **Storage Blob Data Contributor** on the state storage account.

## Pipeline (GitHub Actions)
```yaml
permissions: { id-token: write, contents: read }
env:
  ARM_USE_OIDC: "true"
  ARM_CLIENT_ID: ${{ vars.AZURE_CLIENT_ID }}
  ARM_TENANT_ID: ${{ vars.AZURE_TENANT_ID }}
  ARM_SUBSCRIPTION_ID: ${{ vars.AZURE_SUBSCRIPTION_ID }}
steps:
  - run: terraform init && terraform plan
```
The provider detects `ACTIONS_ID_TOKEN_REQUEST_URL` and `ACTIONS_ID_TOKEN_REQUEST_TOKEN`
itself to fetch the JWT (the workflow needs `id-token: write`).
Azure DevOps: `ARM_USE_OIDC=true`, `ARM_ADO_PIPELINE_SERVICE_CONNECTION_ID`,
`SYSTEM_ACCESSTOKEN` and `SYSTEM_OIDCREQUESTURI` (the provider uses the latter two when
`ARM_OIDC_REQUEST_TOKEN` / `ARM_OIDC_REQUEST_URL` are absent; the backend takes
`oidc_azure_service_connection_id` / `ARM_OIDC_AZURE_SERVICE_CONNECTION_ID`). Other CI:
`ARM_OIDC_TOKEN` or `ARM_OIDC_TOKEN_FILE_PATH`.

## Config
```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "tfstate"
    storage_account_name = "acmetfstate"
    container_name       = "tfstate"
    key                  = "prod/network.tfstate"
    use_oidc             = true
    use_azuread_auth     = true     # data-plane RBAC instead of storage account keys
  }
}
provider "azurerm" {
  features {}
  use_oidc = true                   # or ARM_USE_OIDC
}
```
Leave IDs out of code; env vars keep it portable.

## Common errors
- Token rejected by Entra → the federated credential's issuer, subject or audience does not
  match the token (compare case-sensitively; branch, environment and PR runs have different subjects).
- State access denied → check the **Storage Blob Data Contributor** assignment on the
  container and that `use_azuread_auth` is set.

## Verify
- [ ] No `ARM_CLIENT_SECRET` anywhere in pipelines.
- [ ] `terraform init` and `plan` succeed in CI.

## Checked
- 2026-10-28. Confirmed against the azurerm provider guide "Authenticating using a Service Principal and OpenID Connect" (audience `api://AzureADTokenExchange`, GitHub issuer, `ACTIONS_ID_TOKEN_REQUEST_*`, `id-token: write`, `ARM_OIDC_TOKEN`, `ARM_ADO_PIPELINE_SERVICE_CONNECTION_ID`, `SYSTEM_ACCESSTOKEN`, `SYSTEM_OIDCREQUESTURI`, Contributor example), the Terraform azurerm backend page (`use_oidc`, `use_azuread_auth`, Storage Blob Data Contributor, `ARM_USE_OIDC`, `ARM_OIDC_TOKEN_FILE_PATH`, `oidc_azure_service_connection_id`) and the Microsoft Entra workload identity federation page (case-sensitive issuer, subject and audience match).
- Removed: the AADSTS70021 and AuthorizationPermissionMismatch error codes, the token-refresh-on-long-applies claim, the sign-in-log check, and the example subject strings (not in the fetched docs).
Method: documentation only; no commands were run.
