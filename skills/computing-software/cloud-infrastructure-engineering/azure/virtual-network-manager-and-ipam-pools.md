---
id: computing-software.cloud-infrastructure-engineering.azure.virtual-network-manager-and-ipam-pools
name: virtual-network-manager-and-ipam-pools
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vnet, virtual-network-manager, avnm, ipam-pools, ipam, network-groups, address-space]
level: advanced
status: docs-checked
description: "Deploy Azure Virtual Network Manager: scope, network groups with Policy-driven membership, IPAM pools for non-overlapping address allocation, and goal-state deployments."
sources: ["https://learn.microsoft.com/azure/virtual-network-manager/overview", "https://learn.microsoft.com/azure/virtual-network-manager/concept-ip-address-management", "https://learn.microsoft.com/azure/virtual-network-manager/how-to-manage-ip-addresses-network-manager", "https://learn.microsoft.com/azure/virtual-network-manager/concept-network-groups"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Virtual Network Manager and IPAM pools

**Goal:** central control of VNets across subscriptions: no overlapping address spaces, and
network groups that connectivity and security configurations target automatically.

## Create the manager
```bash
az network manager create -g rg-netmgmt -n avnm-contoso -l westeurope \
  --scope-accesses Connectivity SecurityAdmin \
  --network-manager-scopes management-groups="/providers/Microsoft.Management/managementGroups/mg-contoso"
```
The manager's scope is a set of management groups and/or subscriptions; its network groups can only hold VNets inside that scope. The CLI reference lists `SecurityAdmin` and `Connectivity` as scope-access values.

## Network groups
- **Static** membership: add VNets explicitly.
- **Dynamic** membership via Azure Policy (`Microsoft.Network.Data` mode) — e.g. all VNets tagged `env=prod`:
```json
{ "if": { "allOf": [ { "field": "type", "equals": "Microsoft.Network/virtualNetworks" },
                      { "field": "tags['env']", "equals": "prod" } ] },
  "then": { "effect": "addToNetworkGroup", "details": { "networkGroupId": "<ng-id>" } } }
```
`networkGroupId` must be the full resource ID of the network group and can't be parameterised in the policy definition; the definition also needs `policyType` `Custom` when created outside the AVNM dashboard. A network group is a global container for VNets from any region, a VNet can be in several groups, and Azure Policy membership currently covers virtual networks only (not cross-tenant ones).

## IPAM pools
```bash
az network manager ipam-pool create -g rg-netmgmt --network-manager-name avnm-contoso -n pool-weu \
  --address-prefixes 10.0.0.0/12 --display-name "West Europe"
az network manager ipam-pool create ... -n pool-weu-prod --parent-pool-name pool-weu --address-prefixes 10.0.0.0/14
```
VNet creation from a pool (allocate next free block):
```bicep
resource vnet 'Microsoft.Network/virtualNetworks@2024-01-01' = {
  name: 'vnet-orders-prd'
  location: location
  properties: { addressSpace: { ipamPoolPrefixAllocations: [ { pool: { id: poolId }, numberOfIpAddresses: '1024' } ] } }
}
```
Pools form a hierarchy (a root pool plus child pools, up to seven layers). Pool usage statistics show the total number of IPs and the percentage allocated. Allocate on-premises or other unmanaged ranges to the pool as **static CIDRs** so they're never handed out.
Users need the *IPAM Pool User* role on the pool to allocate; if they can't see pools or VNets, also grant *Network Manager Read* at the network manager scope.

## Deployment model
Configurations (connectivity, security admin, routing) are **committed/deployed per region**:
```bash
az network manager post-commit -g rg-netmgmt --network-manager-name avnm-contoso \
  --commit-type Connectivity --target-locations westeurope northeurope --configuration-ids <cfg-id>
```
Deployment is goal-state: a region gets exactly the configs in the latest commit — omitting a config removes it.

## Gotchas
- Policy-driven membership isn't instant: with fewer than 1,000 subscriptions in scope it takes a few minutes, above that Azure Policy notifies the network group within a 24-hour window; manual members update immediately.
- IPAM allocation is requested as a number of IP addresses (`numberOfIpAddresses`) and the system picks a non-overlapping CIDR from the pool.
- Only one security admin configuration and one routing configuration can be deployed from a manager to a region at a time (use several rule collections); several connectivity configurations can coexist.

## Verify
- [ ] Network group members list includes all tagged VNets.
- [ ] Pool usage statistics show the expected allocation, and a VNet created from the pool gets a CIDR that doesn't overlap the others.

## Checked

2026-10-31. Confirmed against the Learn pages on Virtual Network Manager (scope), network groups, Azure Policy network groups (addToNetworkGroup effect, Microsoft.Network.Data mode, full networkGroupId, membership timing), IPAM concepts and how-to (pools, seven layers, static CIDRs, IPAM Pool User and Network Manager Read, ipamPoolPrefixAllocations and numberOfIpAddresses), configuration deployments (goal state, per-region commit) and the az network manager CLI reference. Removed: the subnet-group claim, the multi-manager conflict note, the power-of-two and cannot-shrink claims, the remove-deployments-first claim, the usage-view wording and the Routing scope-access value (the CLI reference lists only SecurityAdmin and Connectivity). The Bicep API version now matches the Learn template.

Method: documentation only; no commands were run.
