---
id: computing-software.cloud-infrastructure-engineering.terraform.azure-managed-identity-and-service-principal-auth
name: azure-managed-identity-and-service-principal-auth
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, managed-identity, service-principal, azurerm-provider, provider-authentication, use-msi]
level: practitioner
status: docs-checked
description: "Authenticate the azurerm and azuread providers with managed identity on self-hosted agents, or service principals with certificates or secrets, and the ARM_ variables each uses."
sources: ["https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/managed_service_identity", "https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/service_principal_client_certificate", "https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/service_principal_client_secret"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure managed identity and service principals

## Managed identity (agent VM, AKS pod, Container Apps job)
```hcl
provider "azurerm" {
  features {}
  use_msi         = true
  client_id       = var.uami_client_id     # only for user-assigned identity
  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id
}
```
Env equivalent: `ARM_USE_MSI=true`, `ARM_CLIENT_ID`, `ARM_SUBSCRIPTION_ID`, `ARM_TENANT_ID`.
- System-assigned: omit `client_id` (the default). User-assigned: set `client_id` (or `ARM_CLIENT_ID`).
- Grant the identity RBAC on the target scope (the provider guide's example grants
  Contributor) plus data-plane roles where needed (for example Storage Blob Data
  Contributor for the azurerm state backend).
- To create an identity and assign a role you need the Owner role, or Contributor plus
  User Access Administrator.
- AKS: the provider has a separate guide, "Authenticating to Azure using AKS Workload Identity".
- Running somewhere with a non-default endpoint (for example Azure Function Apps)?
  set `ARM_MSI_ENDPOINT`.

## Service principal with certificate (preferred over secrets)
```bash
export ARM_CLIENT_ID=... ARM_TENANT_ID=... ARM_SUBSCRIPTION_ID=...
export ARM_CLIENT_CERTIFICATE_PATH=/secure/sp.pfx
export ARM_CLIENT_CERTIFICATE_PASSWORD=...
```

## Service principal with secret (avoid; rotate)
`ARM_CLIENT_SECRET=...`. Secrets expire; track expiry or move to OIDC or managed identity.

## Choosing
| Runner | Use |
|---|---|
| GitHub/GitLab/Azure DevOps hosted | OIDC (`use_oidc`) |
| Self-hosted VM/VMSS in Azure | managed identity |
| On-prem/non-Azure runner without OIDC | certificate SP |
| Laptop | Azure CLI (`az login`); HashiCorp recommends it for local runs |

## Provider since v4
`subscription_id` is **required** in azurerm 4.0 and later (provider block property or
`ARM_SUBSCRIPTION_ID`).

## Gotchas
- `use_msi` only works where the managed identity endpoint exists (an Azure resource with
  a managed identity); do not set `ARM_USE_MSI` globally for laptops.

## Verify
- [ ] `terraform plan` works with only the identity (no secrets) on the runner.

## Checked
- 2026-10-28. Confirmed against the azurerm provider guides (managed service identity: `use_msi` / `ARM_USE_MSI`, `ARM_CLIENT_ID` for user-assigned, `ARM_MSI_ENDPOINT`, Contributor example, Owner or Contributor plus User Access Administrator; service principal with client certificate: `ARM_CLIENT_CERTIFICATE_PATH`, `ARM_CLIENT_CERTIFICATE_PASSWORD`; with client secret: `ARM_CLIENT_SECRET`; AKS workload identity guide) and the azurerm 4.0 upgrade guide (`subscription_id` required), plus the Terraform azurerm backend page (Storage Blob Data Contributor).
- Removed: the Key Vault role, the azuread provider statement, IMDS laptop error, role propagation time and the claim that the CLI is the implicit default.
Method: documentation only; no commands were run.
