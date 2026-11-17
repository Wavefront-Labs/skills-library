---
id: computing-software.cloud-infrastructure-engineering.azure.data-factory-managed-identity-and-private-endpoints
name: data-factory-managed-identity-and-private-endpoints
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, data-integration, adf-managed-identity, adf-private-endpoint, managed-virtual-network, self-hosted-ir]
level: advanced
status: docs-checked
description: "Secure Azure Data Factory with managed identity linked services, managed VNet integration runtime with managed private endpoints, and private access to the factory itself."
sources: ["https://learn.microsoft.com/azure/data-factory/data-factory-service-identity", "https://learn.microsoft.com/azure/data-factory/managed-virtual-network-private-endpoint", "https://learn.microsoft.com/azure/data-factory/data-factory-private-link", "https://learn.microsoft.com/azure/data-factory/store-credentials-in-key-vault"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Data Factory managed identity and private endpoints

**Goal:** no secrets in linked services and no public network paths for data movement.

## Identity
- A factory can use a **system-assigned managed identity**, or a **user-assigned** identity created as a standalone resource and assigned to one or more factories. Trusted bypass works only with system-assigned identities (Azure Storage and Key Vault).
- Linked service with MI, for example ADLS Gen2: authentication type *System Assigned Managed Identity*, and grant that identity a suitable data-plane role on the account/container.
- Anything needing secrets (on-prem SQL logins, SaaS keys): **Key Vault linked service** + secret references; grant the factory `Key Vault Secrets User`.

## Network
| Need | Mechanism |
|---|---|
| Reach PaaS stores privately from Azure IR | **Managed virtual network** Azure IR + **managed private endpoints** (create in ADF, approve on the target resource) |
| Reach on-premises / IaaS in your VNet | Self-hosted IR on a VM in the VNet or on-prem |
| Lock down factory authoring and runtime control plane | Private endpoints on the factory: target sub-resource `datafactory` (self-hosted IR command traffic) and `portal` (authoring and monitoring); disable public network access (this applies only to the self-hosted IR, not to Azure IR or SSIS IR) |
| SHIR to ADF control plane privately | Private endpoint for sub-resource `datafactory`; the SHIR resolves it via private DNS zone `privatelink.datafactory.azure.net` (`portal` uses `privatelink.adf.azure.com`) |

Managed private endpoint creation:
```bash
az datafactory managed-private-endpoint create -g rg --factory-name adf1 --managed-virtual-network-name default \
  -n mpe-adls --group-id dfs --private-link-resource-id <storageId>
az network private-endpoint-connection approve --id <connectionIdOnStorage> --description "ADF"
```
Set the target storage/SQL firewall to deny public access once managed PEs are approved.

## Gotchas
- Managed VNet IR has a cold start unless you set a time to live (TTL) on the IR for copy/pipeline/external compute; TTL is not available on the default auto-resolve Azure IR.
- Interactive authoring (test connection, browse folders and tables, get schema, preview data) can be enabled on an Azure IR in the managed VNet; it preallocates compute, otherwise each interactive operation waits for allocation.
- Pipeline and external compute TTL cannot be disabled; Copy TTL can.

## Verify
- [ ] Linked service *Test connection* succeeds via managed VNet IR; target store has public access disabled.
- [ ] No linked service contains inline secrets (`az datafactory linked-service list` reviewed).

## Checked
Date: 2026-10-31. Checked against Microsoft Learn: Managed identity for Data Factory, Managed virtual network and managed private endpoints, Azure Private Link for Data Factory, Store credentials in Azure Key Vault; CLI flags checked against `az datafactory`.
- Confirmed: system- and user-assigned identities, trusted bypass limit, Key Vault Secrets User role, `datafactory` and `portal` sub-resources and their private DNS zones, public-access setting scope, TTL types and the default auto-resolve IR limit, interactive authoring.
- Removed as unconfirmed: identity naming and credential-object claim, Azure SQL grant statement, storage role name, Git-publish and silent public-endpoint gotchas.
Method: documentation only; no commands were run.
