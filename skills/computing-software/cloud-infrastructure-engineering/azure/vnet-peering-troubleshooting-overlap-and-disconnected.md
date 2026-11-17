---
id: computing-software.cloud-infrastructure-engineering.azure.vnet-peering-troubleshooting-overlap-and-disconnected
name: vnet-peering-troubleshooting-overlap-and-disconnected
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vnet-peering, peering-troubleshooting, address-overlap, peering-disconnected, effective-routes]
level: practitioner
status: docs-checked
description: "Troubleshoot VNet peering: overlapping address spaces, Disconnected/Initiated states, address-space sync, NSG/UDR blocks, gateway transit and DNS across peers."
sources: ["https://learn.microsoft.com/troubleshoot/azure/virtual-network/virtual-network-troubleshoot-peering-issues", "https://learn.microsoft.com/azure/virtual-network/virtual-network-manage-peering", "https://learn.microsoft.com/azure/network-watcher/connection-troubleshoot-overview", "https://learn.microsoft.com/en-us/cli/azure/network/watcher", "https://learn.microsoft.com/en-us/cli/azure/network/vnet/peering"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# VNet peering troubleshooting

**Goal:** find why VMs across a peering can't talk, using state, routes, NSGs and DNS in order.

## 1. Peering state
Check both sides (portal: virtual network > Peering > Status; CLI per virtual network):
```bash
az network vnet peering show -g rg --vnet-name vnet-a -n <peering-name> --query "{state:peeringState, remoteAddressSpace:remoteAddressSpace.addressPrefixes}"
```
| State | Meaning and fix |
|---|---|
| Initiated | Only the first link exists: create the peering from the second virtual network |
| Connected | Both links exist and traffic can flow |
| Disconnected | One link was deleted: delete the remaining link on both virtual networks, then re-create both |

Causes of Disconnected listed on the page: deleting a link from one side, an address-space change without a sync, moving a virtual network to another subscription or tenant, and Azure Policy removing or blocking peering. You can't re-create a peering while one side is Disconnected; delete both first, then re-create with the correct Allow forwarded traffic, Allow gateway transit and Use remote gateways settings on each side.
After you change a peered virtual network's address space, sync the peering for each remote peer:
```bash
az network vnet peering sync -g rg --vnet-name vnet-a -n <peering-name>
```
Run the sync after every resize rather than batching them; address-space sync isn't supported when the peer is a classic virtual network.

## 2. Overlap
Peered virtual networks must have nonoverlapping address spaces; creating a peering with overlapping CIDR ranges fails (for example 10.0.0.0/16 and 10.0.1.0/24 overlap). Compare ranges with
`az network vnet show -g rg -n vnet-a --query "addressSpace.addressPrefixes"`.
Fixes on the page: remove or change the overlapping range on one virtual network (first make sure no subnets or resources use that range, then sync the peering); in Azure Virtual Network Manager set `ConnectedGroupAddressOverlap` to `Disallowed` to prevent overlap in mesh topologies; plan address space across all virtual networks before peering.

## 3. Routes
```bash
az network nic show-effective-route-table -g rg-a -n nic-vm1 -o table   # expect next hop type Virtual network peering for the remote prefix
az network watcher show-next-hop -g rg-a --vm vm1 --source-ip 10.1.0.4 --dest-ip 10.2.0.4
```
Peering adds system routes with next hop type Virtual network peering. A UDR with the same prefix overrides it, which sends traffic to an NVA or drops it. Peering system routes take precedence over BGP routes. In hub-and-spoke designs with an NVA, test both directions: if the return path doesn't pass through the same NVA, the asymmetric route can break connections, and a stateful firewall that sees only one direction may drop the traffic.

## 4. NSGs and the network path
```bash
az network watcher test-ip-flow -g rg-a --vm vm1 --direction Outbound --protocol TCP --local 10.1.0.4:50000 --remote 10.2.0.4:443
```
Use Connection troubleshoot and IP flow verify from the source VM to the destination VM to find an NSG or UDR interfering. `--local` and `--remote` take `X.X.X.X:PORT`. If a firewall or NVA is involved, you can temporarily remove the UDR that points to it and test directly (record the UDR first). If the peering is Connected and packets reach the destination VM, check the VM firewall and the listening application.
Connection troubleshoot reports peering-related issue types including `VnetAccessNotAllowed` (the peering link has AllowVNetAccess false), `AllowGatewayTransitNotEnabled`, `UseRemoteGatewaysNotEnabled`, `IPForwardingNotEnabled` (the NVA's NIC) and `BasicILBNotSupportedWithGlobalPeering`.
With "Allow the peered virtual network to access" selected, the `VirtualNetwork` service tag in NSG rules includes the peered virtual network.

## 5. DNS
Default Azure name resolution does not resolve names across peered virtual networks. Use Azure Private DNS or a custom DNS server.

## 6. Gateway transit specifics
- Site-to-site or ExpressRoute from on-premises to a spoke: the troubleshooting page says to verify Allow forwarded traffic on the virtual network that has the gateway and Use remote gateway on the one that doesn't, and to have your network admin add the remote virtual network address space on the on-premises devices. The peering settings page adds that Use remote gateways needs the gateway side to enable "Allow gateway or route server ... to forward traffic".
- You can't use remote gateways if the spoke already has a gateway. Use remote gateways can be enabled in only one of the peerings.
- Point-to-site clients must download and reinstall the client package after peering is set up or changed so they get the new routes.
- If the remote virtual network is in another tenant, the portal can't check for its gateway and the "remote virtual network lacks a gateway" error can appear: re-create the peering selecting Use Remote Gateways, or enable it with PowerShell or CLI.

## Gotchas
- Global peering: resources can't reach the frontend IP of a Basic Load Balancer in a globally peered virtual network; Basic Load Balancer was retired on 30 September 2025 and resources using Basic internal load balancer SKUs don't work over global peering. Use Standard.
- Peering is not transitive: A-B and B-C peerings give no A-C connectivity without another peering or an NVA in the hub.
- You can't move a virtual network while it's part of a peering.

## Verify
- [ ] Both peerings show Connected, and the effective routes on a NIC list the remote address space.
- [ ] `az network watcher test-connectivity --source-resource vm1 --dest-address 10.2.0.4 --dest-port 443` returns `ConnectionStatus` Reachable (this command is marked Preview in the CLI reference).

## Checked

2026-11-07. Read in full: Troubleshoot virtual network peering problems, Create, change, or delete virtual network peering (portal, PowerShell and CLI tabs, requirements and permissions), and Connection troubleshoot overview (response properties and the full error and fault tables). The `az network watcher` and `az network vnet peering` CLI references are large; I searched them for the flags and `X.X.X.X:PORT` format used, not read end to end.
Corrected: the state query now uses documented properties (`peeringState`, `remoteAddressSpace.addressPrefixes`) instead of unconfirmed `peeringSyncLevel` and `remoteVirtualNetwork.id`. Removed: "Private Link Service / NAT via NVA" as an overlap fix, the on-premises "longest prefix/most recent wins" claim, the "link each private DNS zone to both VNets" DNS claim, the `UseRemoteGateways` error cause list, and "deny on VirtualNetwork inbound" wording. Added: documented Disconnected causes, sync rules, Virtual Network Manager setting and Connection troubleshoot issue types.

Method: documentation only; no commands were run.
