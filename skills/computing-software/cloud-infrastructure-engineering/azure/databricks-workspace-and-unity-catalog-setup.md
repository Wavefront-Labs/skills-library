---
id: computing-software.cloud-infrastructure-engineering.azure.databricks-workspace-and-unity-catalog-setup
name: databricks-workspace-and-unity-catalog-setup
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, databricks, databricks-workspace, unity-catalog, vnet-injection, secure-cluster-connectivity, private-link, access-connector, metastore, external-locations, storage-credentials, cluster-policies]
level: advanced
status: docs-checked
description: "Deploy Azure Databricks properly: Premium workspace with VNet injection, no public IP and Private Link, Unity Catalog metastore, access connector, external locations and grants."
sources: ["https://learn.microsoft.com/en-us/azure/databricks/security/network/classic/vnet-inject", "https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/get-started", "https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/azure-managed-identities", "https://learn.microsoft.com/en-us/azure/databricks/security/network/classic/private-link"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Databricks workspace and Unity Catalog

**Goal:** a workspace whose compute runs in your VNet with no public IPs, whose data access is
governed centrally by Unity Catalog through a managed identity — no storage keys in notebooks.

## 1. Workspace with VNet injection
```bash
# two dedicated subnets (host/"public" and container/"private"), each delegated to Microsoft.Databricks/workspaces, same NSG
az network vnet subnet create -g rg-dbx --vnet-name vnet-dbx -n snet-host      --address-prefixes 10.30.0.0/26 --delegations Microsoft.Databricks/workspaces --network-security-group nsg-dbx
az network vnet subnet create -g rg-dbx --vnet-name vnet-dbx -n snet-container --address-prefixes 10.30.1.0/26 --delegations Microsoft.Databricks/workspaces --network-security-group nsg-dbx
az databricks workspace create -g rg-dbx -n dbw-prod -l uksouth --sku premium \
  --vnet <vnet-id> --public-subnet snet-host --private-subnet snet-container \
  --enable-no-public-ip true --public-network-access Disabled --required-nsg-rules NoAzureDatabricksRules
```
- Private Link on the classic compute plane needs the Premium plan (and VNet injection plus secure cluster connectivity for back-end and end-to-end modes). `--required-nsg-rules` is `AllRules` for front-end only and `NoAzureDatabricksRules` for back-end and end-to-end.
- Subnet sizing: the VNet takes a CIDR block between /16 and /24; each of the two subnets should be at least /26 (smaller than /26 is not recommended). Subnet CIDR ranges cannot be changed after deployment.
- **Private Link** endpoints: `databricks_ui_api` (workspace UI and REST API; front-end and back-end) plus `browser_authentication` for SSO over a private connection. Only one `browser_authentication` endpoint can exist per Azure region and private DNS zone. Private endpoints are region-specific.

## 2. Unity Catalog
1. **Access connector** (`Microsoft.Databricks/accessConnectors`): a first-party Azure resource with a system-assigned managed identity (a user-assigned one is optional). Grant its identity *Storage Blob Data Contributor* on the ADLS Gen2 account (or *Storage Blob Delegator* on the account plus *Storage Blob Data Contributor* on one container for a narrower grant).
2. Use the access connector's resource ID when creating the Unity Catalog metastore or storage credential, then create external locations and grant privileges to groups, never users. Co-locate the connector, workspaces, metastore and storage in one region.
3. Storage firewall: add the access connector as a resource instance (`Microsoft.Databricks/accessConnectors`) if the account is network-restricted.
- Any access connector in the same tenant can reach a storage account that allows it, so scope role assignments tightly.

## Gotchas
- Databricks creates and manages the NSG rules on the delegated subnets; do not modify or delete them, and use a unique NSG per workspace.

## Verify
- [ ] Workspace shows *No Public IP: Enabled*, VNet-injected; UI reachable only via Private Link if required.
- [ ] Workspace assigned to a metastore; the external location validates via the access connector.
- [ ] An analyst group can query governed tables but cannot read the storage path directly.

## Checked
2026-10-31. Confirmed against the Azure Databricks VNet injection, Private Link, Unity Catalog managed identity pages:
VNet /16 to /24 and subnet at least /26 guidance, subnets not resizable after deployment, delegation to
`Microsoft.Databricks/workspaces`, managed NSG rules, `AllRules`/`NoAzureDatabricksRules`, Premium plan prerequisite,
`databricks_ui_api` and `browser_authentication` endpoints, access connector and Storage Blob Data Contributor /
Delegator roles. `az network vnet subnet` and `az databricks workspace` flags checked against the CLI reference.
Removed as unconfirmed: "/24 = 250 nodes", metastore-per-region rule, DNS zone name, SQL examples, cluster policy
and compute governance guidance, and the legacy hive_metastore and mount gotchas.
Method: documentation only; no commands were run.
