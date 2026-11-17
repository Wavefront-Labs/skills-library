---
id: computing-software.cloud-infrastructure-engineering.azure.terraform-and-tools-authenticating-to-azure-via-oidc
name: terraform-and-tools-authenticating-to-azure-via-oidc
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, workload-identity-federation, terraform-oidc, oidc-terraform, azurerm-oidc, terraform-backend-oidc, use-oidc]
level: practitioner
status: draft
description: "Authenticate Terraform azurerm/azapi providers and the azurerm state backend with OIDC from GitHub Actions, Azure DevOps, GitLab and Terraform Cloud — no client secrets."
sources: ["https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/service_principal_oidc", "https://developer.hashicorp.com/terraform/language/backend/azurerm", "https://developer.hashicorp.com/terraform/cloud-docs/workspaces/dynamic-provider-credentials/azure-configuration", "https://learn.microsoft.com/azure/developer/terraform/authenticate-to-azure"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Terraform and other tools authenticating via OIDC

**Goal:** `terraform plan/apply` in CI authenticates to both the state backend and Azure APIs with
federated tokens.

## Provider + backend config
```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "rg-tfstate"
    storage_account_name = "sttfstateprod"
    container_name       = "tfstate"
    key                  = "orders/prod.tfstate"
    use_oidc             = true
    use_azuread_auth     = true    # data-plane RBAC, not storage keys
  }
}
provider "azurerm" {
  features {}
  use_oidc = true
  # client_id / tenant_id / subscription_id via ARM_* env vars
}
```
Identity needs **Storage Blob Data Contributor** on the state container plus its deployment roles.

## GitHub Actions
```yaml
permissions: { id-token: write, contents: read }
env:
  ARM_CLIENT_ID: ${{ vars.AZURE_CLIENT_ID }}
  ARM_TENANT_ID: ${{ vars.AZURE_TENANT_ID }}
  ARM_SUBSCRIPTION_ID: ${{ vars.AZURE_SUBSCRIPTION_ID }}
  ARM_USE_OIDC: "true"
steps:
  - uses: hashicorp/setup-terraform@v3
  - run: terraform init && terraform plan -out tfplan
```
The provider requests the GitHub token itself (via `ACTIONS_ID_TOKEN_REQUEST_*`) and refreshes
it for long applies — better than `azure/login` + CLI auth.

## Azure DevOps
```yaml
- task: AzureCLI@2
  inputs:
    azureSubscription: sc-orders-prod      # WIF service connection
    addSpnToEnvironment: true
    scriptType: bash
    scriptLocation: inlineScript
    inlineScript: |
      export ARM_CLIENT_ID=$servicePrincipalId ARM_TENANT_ID=$tenantId ARM_OIDC_TOKEN=$idToken ARM_USE_OIDC=true
      export ARM_SUBSCRIPTION_ID=$(az account show --query id -o tsv)
      terraform init && terraform apply -auto-approve tfplan
```
Newer azurerm (≥3.x late / 4.x) supports `ARM_OIDC_AZURE_SERVICE_CONNECTION_ID` + `SYSTEM_ACCESSTOKEN` to refresh tokens for runs > 1 h.

## GitLab / Terraform Cloud
- GitLab: `id_tokens: { AZURE_TOKEN: { aud: api://AzureADTokenExchange } }`, then `ARM_OIDC_TOKEN=$AZURE_TOKEN`; subject `project_path:group/proj:ref_type:branch:ref:main`.
- HCP Terraform: workspace env vars `TFC_AZURE_PROVIDER_AUTH=true`, `TFC_AZURE_RUN_CLIENT_ID`; subjects `organization:<org>:project:<p>:workspace:<w>:run_phase:plan|apply` — separate identities for plan (Reader) and apply.

## Gotchas
- `use_azuread_auth` missing → backend falls back to listing storage keys and fails without `listKeys` permission.
- ADO `$idToken` expires in ~10 min-1 h; long applies need the service-connection refresh method.
- Separate plan and apply identities: plan with Reader+state read on PRs, apply with Contributor on main only.

## Verify
- [ ] `terraform init` log shows "Using OIDC" / no `ARM_CLIENT_SECRET` in pipeline env.
- [ ] Storage account `allowSharedKeyAccess=false` and state still works.
