---
id: computing-software.cloud-infrastructure-engineering.azure.bidirectional-vnet-peering-in-bicep-and-terraform
name: bidirectional-vnet-peering-in-bicep-and-terraform
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vnet-peering, peering-bicep, bidirectional-peering, terraform, hub-spoke, iac]
level: practitioner
status: gated
description: "Create both sides of a hub-spoke VNet peering in one deployment: Bicep cross-scope modules, Terraform provider aliases, gateway transit ordering and safe updates."
sources: ["https://learn.microsoft.com/azure/templates/microsoft.network/virtualnetworks/virtualnetworkpeerings", "https://learn.microsoft.com/azure/azure-resource-manager/bicep/deploy-to-resource-group#deploy-to-target-resource-group", "https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/virtual_network_peering"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bidirectional peering in Bicep and Terraform

**Goal:** one spoke deployment creates both peerings (spoke->hub and hub->spoke) correctly, even across subscriptions.

## Bicep: module per side
```bicep
// peering.bicep (deployed at the RG of the local VNet)
param localVnetName string
param remoteVnetId string
param allowGatewayTransit bool = false
param useRemoteGateways bool = false

resource peer 'Microsoft.Network/virtualNetworks/virtualNetworkPeerings@2023-02-01' = {
  name: '${localVnetName}/to-${last(split(remoteVnetId, '/'))}'
  properties: {
    remoteVirtualNetwork: { id: remoteVnetId }
    allowVirtualNetworkAccess: true
    allowForwardedTraffic: true
    allowGatewayTransit: allowGatewayTransit
    useRemoteGateways: useRemoteGateways
  }
}
```
```bicep
// spoke main.bicep
module hubToSpoke 'peering.bicep' = {
  name: 'hub-to-${spokeVnet.name}'
  scope: resourceGroup(hubSubscriptionId, hubResourceGroup)
  params: { localVnetName: hubVnetName, remoteVnetId: spokeVnet.id, allowGatewayTransit: true }
}
module spokeToHub 'peering.bicep' = {
  name: 'spoke-to-hub'
  params: { localVnetName: spokeVnet.name, remoteVnetId: hubVnetId, useRemoteGateways: true }
  dependsOn: [ hubToSpoke ]   // useRemoteGateways requires the hub side with gateway transit first
}
```
The deploying identity needs peering rights on the hub VNet (custom role) as well as the spoke.

## Terraform: two providers
```hcl
provider "azurerm" {
  alias           = "hub"
  subscription_id = var.hub_subscription_id
  features {}
}
resource "azurerm_virtual_network_peering" "hub_to_spoke" {
  provider                  = azurerm.hub
  name                      = "hub-to-${azurerm_virtual_network.spoke.name}"
  resource_group_name       = var.hub_rg
  virtual_network_name      = var.hub_vnet_name
  remote_virtual_network_id = azurerm_virtual_network.spoke.id
  allow_forwarded_traffic   = true
  allow_gateway_transit     = true
}
resource "azurerm_virtual_network_peering" "spoke_to_hub" {
  name                      = "spoke-to-hub"
  resource_group_name       = azurerm_resource_group.spoke.name
  virtual_network_name      = azurerm_virtual_network.spoke.name
  remote_virtual_network_id = var.hub_vnet_id
  allow_forwarded_traffic   = true
  use_remote_gateways       = true
  depends_on                = [azurerm_virtual_network_peering.hub_to_spoke]
}
```

## Gotchas
- `useRemoteGateways` only takes effect when `allowGatewayTransit` is also true on the remote peering (ARM reference), so create the hub side first.
- The peering resource exposes `peeringSyncLevel` (FullyInSync, LocalNotInSync, RemoteNotInSync, LocalAndRemoteNotInSync): check it after address-space changes instead of assuming IaC resynced.
- Terraform argument names above follow the azurerm registry page, which could not be read here (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] Both peerings Connected after one pipeline run; re-run is a no-op.

## Checked
2026-10-28. Confirmed (Learn ARM reference for virtualNetworkPeerings, Bicep deploy-to-resource-group): property names
`remoteVirtualNetwork`, `allowVirtualNetworkAccess`, `allowForwardedTraffic`, `allowGatewayTransit`, `useRemoteGateways`,
`peeringSyncLevel` and its values, `scope: resourceGroup(...)` for cross-scope modules. Changed: apiVersion 2024-01-01 (not
seen on the page) to 2023-02-01 (in the page's samples). Removed: "fails if the hub has no gateway", the inline-subnet
churn note and the AVNM suggestion (unconfirmed). Gated: the azurerm Terraform arguments (registry page returned empty).
Method: documentation only; no commands were run.
