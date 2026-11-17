---
id: computing-software.cloud-infrastructure-engineering.azure.private-endpoint-create-for-paas-services
name: private-endpoint-create-for-paas-services
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, private-link, private-endpoint-create, private-endpoint-setup, group-id, sub-resource, public-network-access]
level: practitioner
status: docs-checked
description: "Create private endpoints for PaaS services: pick the right group ID (sub-resource), subnet and static IP options, DNS zone group, then disable public network access safely."
sources: ["https://learn.microsoft.com/azure/private-link/create-private-endpoint-cli", "https://learn.microsoft.com/azure/private-link/private-endpoint-overview", "https://learn.microsoft.com/azure/private-link/availability"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create private endpoints for PaaS

**Goal:** an Azure service is reachable on a private IP from the VNet (and on-prem), with DNS
resolving correctly, and its public endpoint closed.

## Group IDs (sub-resources) — one PE per group
| Service | Group IDs |
|---|---|
| Storage | `blob`, `file`, `queue`, `table`, `web`, `dfs` (each separate) |
| Key Vault | `vault` |
| SQL | `sqlServer`; SQL MI `managedInstance` |
| Cosmos DB | `Sql`, `SqlDedicated`, `MongoDB`, `Cassandra`, `Gremlin`, `Table`, `Analytical` |
| App Service / Functions | `sites` |
| ACR | `registry` |
| Service Bus / Event Hubs | `namespace` |
| Azure Monitor (AMPLS) | `azuremonitor` |
```bash
az network private-link-resource list --id <resource-id> -o table   # discover groupIds and required DNS zones
```

## Create
```bash
az network private-endpoint create -g rg-app -n pe-stdata-blob -l westeurope \
  --vnet-name vnet-spoke --subnet snet-pe \
  --private-connection-resource-id <storage-id> --group-id blob --connection-name stdata-blob \
  --nic-name nic-pe-stdata-blob \
  --ip-config name=ipcfg group-id=blob member-name=blob private-ip-address=10.20.5.10    # optional static IP
az network private-endpoint dns-zone-group create -g rg-app --endpoint-name pe-stdata-blob -n default \
  --private-dns-zone <privatelink.blob.core.windows.net zone id> --zone-name blob
```
- The private endpoint must be in the same region and subscription as its VNet; the target resource can be in another region. A dedicated `snet-pe` per spoke keeps NSG/UDR policy simple (private endpoints support network policies for NSG, UDR and ASG).
- `--nic-name` sets a custom NIC name; `--ip-config` sets a static IP.

## Close the public endpoint (after testing)
Disable public network access on the target service (each service has its own setting; see its networking docs).
Check dependencies first: admin access from outside the VNet and any client or CI agent still using the public endpoint.

## Gotchas
- Each sub-resource (`blob`, `dfs`, `file`, ...) needs its own private endpoint.
- Cross-region PEs are allowed (resource in region A, PE in region B) — useful for DR clients.

## Verify
- [ ] From a VM in the VNet: `nslookup stdata.blob.core.windows.net` → 10.20.5.10 via `stdata.privatelink.blob.core.windows.net`.
- [ ] From the internet: access to the service's public endpoint is refused.
- [ ] `az network private-endpoint show -g rg-app -n pe-stdata-blob --query "privateLinkServiceConnections[0].privateLinkServiceConnectionState.status"` = Approved.

## Checked

- 2026-10-27. Confirmed on Microsoft Learn (private endpoint overview, availability, CLI reference for `network private-endpoint`, `dns-zone-group` and `private-link-resource`): group IDs for Storage, Key Vault, SQL Database, SQL Managed Instance, Cosmos DB, App Service, Container Registry (Premium), Service Bus, Event Hubs and Azure Monitor private link scope, same-region/subscription rule for the endpoint, cross-region target resources, network policy support, `--group-id`, `--ip-config`, `--nic-name`, `--connection-name`, `dns-zone-group create/add` with `--private-dns-zone` and `--zone-name`, `private-link-resource list --id`.
- Removed: the `az storage` and `az keyvault` public-access commands (not in the fetched pages), the `sites-<slot>` form, the PE NIC immutability and per-region FQDN gotchas, the ADLS both-endpoints claim, the 403 error name, and the list of Azure services that use public endpoints.

Method: documentation only; no commands were run.
