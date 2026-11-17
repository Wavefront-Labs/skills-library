---
id: computing-software.cloud-infrastructure-engineering.azure.spoke-to-spoke-routing-via-hub-firewall
name: spoke-to-spoke-routing-via-hub-firewall
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, hub-and-spoke, spoke-to-spoke, transitive-routing, azure-firewall, udr, vnet-peering]
level: practitioner
status: docs-checked
description: "Enable spoke-to-spoke traffic in hub-and-spoke via the hub firewall: UDRs on both spokes, firewall network rules, forwarded-traffic flags, and alternatives (AVNM mesh, vWAN)."
sources: ["https://learn.microsoft.com/azure/architecture/networking/architecture/hub-spoke", "https://learn.microsoft.com/azure/architecture/networking/guide/spoke-to-spoke-networking", "https://learn.microsoft.com/azure/firewall/rule-processing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spoke-to-spoke via hub firewall

**Goal:** spokes talk to each other only through an inspected, logged path in the hub.

## Why it doesn't work by default
Peering is non-transitive: spoke1 ↔ hub ↔ spoke2 gives spoke1 no route to spoke2.

## Configure
1. Peerings hub↔spoke with **allowForwardedTraffic = true** on both sides of each peering (the firewall forwards traffic that didn't originate in the hub).
2. Route tables on every spoke subnet:
```bash
az network route-table route create -g rg-spoke1 --route-table-name rt-spoke1 -n to-spokes \
  --address-prefix 10.20.0.0/14 --next-hop-type VirtualAppliance --next-hop-ip-address 10.0.0.4
```
   Use a summary covering all spokes (contiguous IP plan pays off). The spoke's own address space system route is more specific, so intra-spoke traffic stays local.
3. Firewall network rules (rule collection group *spoke-to-spoke*):
```bash
az network firewall policy rule-collection-group collection add-filter-collection -g rg-hub --policy-name afwp-hub \
  --rcg-name rcg-east-west --name allow-app-to-db --collection-priority 200 --action Allow \
  --rule-type NetworkRule --rule-name app1-to-sql --source-addresses 10.20.1.0/24 --destination-addresses 10.21.2.0/24 \
  --destination-ports 1433 --ip-protocols TCP
```
   By default Azure Firewall doesn't SNAT network-rule traffic to RFC 1918 or RFC 6598 destinations (application rules always SNAT) — return traffic follows the destination spoke's UDR back through the firewall (symmetric).

## Alternatives
| Option | When |
|---|---|
| AVNM connectivity config (hub-spoke with **direct connectivity** within groups) | Trusted spokes needing low-latency without inspection |
| Direct spoke-to-spoke peering | Few high-volume pairs (e.g. app ↔ data platform) |
| Virtual WAN (Microsoft-managed hub router) | Many spokes and regions, managed routing |
| Private Link Service/private endpoints | Expose one service rather than full network reach |

## Gotchas
- East-west traffic is bounded by the firewall's bandwidth limits and adds a hop — big data flows (backup, replication) may justify direct peering or AVNM direct connectivity.
- Forgetting the UDR in one spoke = asymmetric flow, firewall drops return packets.
- Private endpoints add a /32 route that beats broader UDRs; enable network policies for user-defined routes on the PE subnet and use a UDR prefix at least as specific as the VNet address space, or traffic to them bypasses the firewall.

## Verify
- [ ] Next hop from spoke1 VM to spoke2 IP = VirtualAppliance 10.0.0.4 (and vice versa).
- [ ] Azure Firewall network rule logs show the allowed flow spoke1→spoke2 and denies for non-allowed ports.

## Checked

2026-10-31. Confirmed against the Learn pages on the hub-spoke architecture (non-transitive peering, Allow forwarded traffic, firewall or NVA in the hub), spoke-to-spoke networking (AVNM direct connectivity, direct peering for high-bandwidth pairs, Virtual WAN, Private Link), Azure Firewall SNAT private ranges and private endpoint network policies; the firewall policy commands were checked against the az CLI reference with check_commands.py. Removed: the routing-intent wording, the per-GB processing cost remark and the AZFWNetworkRule table name (not in the fetched docs).

Method: documentation only; no commands were run.
