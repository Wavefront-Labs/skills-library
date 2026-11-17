---
id: computing-software.cloud-infrastructure-engineering.azure.cross-tenant-and-cross-subscription-vnet-peering
name: cross-tenant-and-cross-subscription-vnet-peering
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vnet-peering, cross-tenant-peering, cross-subscription, least-privilege]
level: advanced
status: docs-checked
description: "Peer VNets across subscriptions and Entra tenants: required permissions on both sides, guest identities, the auxiliary token header and peering states."
sources: ["https://learn.microsoft.com/azure/virtual-network/create-peering-different-subscriptions", "https://learn.microsoft.com/azure/virtual-network/virtual-network-manage-peering#permissions", "https://learn.microsoft.com/azure/azure-resource-manager/management/authenticate-multi-tenant"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-tenant and cross-subscription peering

**Goal:** connect a VNet owned by another team, subscription or company without handing out broad rights.

## Permissions
The account needs the Network Contributor role, or a custom role with these actions:

| Action | Purpose |
|---|---|
| `Microsoft.Network/virtualNetworks/virtualNetworkPeerings/write` | create a peering from VNet A to VNet B |
| `Microsoft.Network/virtualNetworks/virtualNetworkPeerings/read` | read a peering |
| `Microsoft.Network/virtualNetworks/virtualNetworkPeerings/delete` | delete a peering |

To remove the remote VNet's peering you need Network Contributor, or the `read` and `delete` actions, on the remote VNet.
Check the Learn permissions section for any additional action before building a minimal custom role, and test it.

## Peering states
A peering must be configured on each VNet. The first one is **Initiated**; once the second exists both become
**Connected**, and the peering is only established when both are Connected.

## Same tenant, different subscriptions
Use the full remote resource ID:
```bash
az network vnet peering create -g rg-a --vnet-name vnet-a -n a-to-b --allow-vnet-access \
  --remote-vnet /subscriptions/<subB>/resourceGroups/rg-b/providers/Microsoft.Network/virtualNetworks/vnet-b
```

## Different tenants
- Add the user from each tenant as a **guest** in the opposite tenant and assign Network Contributor on the VNet; each
  user must accept the guest invitation. To keep network management separate per tenant, assign each user the role on
  their own tenant's VNet only, and each side creates its peering.
- Multi-tenant apps: Azure Resource Manager accepts auxiliary tokens in the `x-ms-authorization-auxiliary` header (up
  to three); the user or application must be invited as a guest to the other tenants, and an expired token gives a 401.

## Before you peer
- Address spaces must not overlap.
- Peerings are not transitive.
- NSGs and firewalls still apply on both sides.

## Verify
- [ ] Both peerings show `Connected`; test flows only on the agreed ports.

## Checked
2026-10-31. Confirmed against Learn "Create, change, or delete a virtual network peering", "Create a virtual network
peering - different subscriptions" and "Authenticate requests across tenants": permissions table, Network Contributor,
Initiated/Connected states, guest and invitation steps, auxiliary header and 3-token limit, non-overlap, non-transitive.
Removed: the `peer/action` custom role, `AssignableScopes` example, `az login` steps, Terraform `auxiliary_tenant_ids`,
the `Disconnected` and `FullyInSync` states, gateway-transit defaults and the policy example (not on the pages read).
Method: documentation only; no commands were run.
