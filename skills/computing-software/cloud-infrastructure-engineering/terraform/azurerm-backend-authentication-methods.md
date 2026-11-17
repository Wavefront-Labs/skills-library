---
id: computing-software.cloud-infrastructure-engineering.terraform.azurerm-backend-authentication-methods
name: azurerm-backend-authentication-methods
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, use-azuread-auth, azurerm-backend-oidc, azurerm-backend, azure-storage-backend]
level: practitioner
status: docs-checked
description: "Authenticate the azurerm state backend without storage keys: use_azuread_auth with OIDC, managed identity or Azure CLI, and the RBAC roles each needs."
sources: ["https://developer.hashicorp.com/terraform/language/backend/azurerm", "https://learn.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# azurerm backend authentication

## Prefer Entra ID (Azure AD) over access keys
```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "rg-tfstate"
    storage_account_name = "sttfstateprod01"
    container_name       = "tfstate"
    key                  = "payments/prod.tfstate"
    use_azuread_auth     = true      # data-plane auth with Entra ID, no keys
  }
}
```
With `use_azuread_auth = true` the identity needs **Storage Blob Data Contributor**
on the storage account container (HashiCorp's recommended least-privilege data-plane
role). The data plane URI is normally inferred from `storage_account_name` and
`container_name`, so no management-plane access is needed. The management plane is
used only when you set `lookup_blob_endpoint = true` (required for the Azure DNS zone
endpoints feature): then you also need `resource_group_name`, `subscription_id` and the
**Reader** role on the storage account.

## Identity options
| Method | Settings |
|---|---|
| OIDC from CI (GitHub, Azure DevOps, GitLab) | `use_oidc = true`, `client_id`, `tenant_id` (or `ARM_USE_OIDC`, `ARM_CLIENT_ID`, `ARM_TENANT_ID`); GitHub provides the token automatically with `id-token: write` |
| Managed identity (self-hosted agent VM) | `use_msi = true`, optional `client_id` for user-assigned |
| Azure CLI (laptops) | `use_cli = true` / `ARM_USE_CLI`; `az login` first |
| Service principal + secret | `client_secret` / `ARM_CLIENT_SECRET` (avoid) |
| Access key / SAS | `access_key` / `ARM_ACCESS_KEY`, `sas_token` (avoid) |

The backend can take every setting above from `ARM_*` environment variables
(`ARM_USE_OIDC`, `ARM_USE_AZUREAD`, `ARM_CLIENT_ID`, `ARM_TENANT_ID`, `ARM_USE_MSI`,
`ARM_USE_CLI`, `ARM_ACCESS_KEY`, `ARM_SAS_TOKEN`, `ARM_CLIENT_SECRET`), so CI can
configure it without editing HCL.

## Hardening the account
- Microsoft's Terraform state guide advises restricting the storage account with a
  storage firewall, service endpoint or private endpoint, and warns that its access-key
  example is not a production choice; CI runners must still reach the blob endpoint.
- Enable blob versioning for recovery (see Microsoft Learn, "Enable and manage blob
  versioning").

## Gotchas
- A blob authorization failure usually means the Storage Blob Data Contributor assignment
  is missing, or `use_azuread_auth` is not set.
- An OIDC federated credential's issuer, subject and audience must match the run's token
  case-sensitively (branch, environment and PR runs differ).

## Verify
- [ ] `terraform init -reconfigure` works with no `ARM_ACCESS_KEY` set.
- [ ] No `access_key` or `sas_token` appears in the backend block or CI variables.

## Checked
- 2026-10-28. Confirmed against the Terraform azurerm backend page (`use_azuread_auth`, `use_oidc`, `use_msi`, `use_cli`, `client_secret`, `access_key`, `sas_token` and their `ARM_*` variables; `client_id` optional for system-assigned identity; Storage Blob Data Contributor; Reader and `resource_group_name` only with `lookup_blob_endpoint`), Microsoft Learn "Store Terraform state in Azure Storage" (firewall, service endpoint, private endpoint advice) and the Entra workload identity federation page (case-sensitive issuer, subject, audience match).
- Removed: the `shared_access_key_enabled` argument, soft delete, the `AuthorizationPermissionMismatch` and `KeyBasedAuthenticationNotPermitted` error names, the 5-minute propagation claim and the old-versus-new backend version split (not in the fetched docs).
Method: documentation only; no commands were run.
