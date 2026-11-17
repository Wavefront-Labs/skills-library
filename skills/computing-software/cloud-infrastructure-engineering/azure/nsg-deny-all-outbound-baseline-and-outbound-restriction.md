---
id: computing-software.cloud-infrastructure-engineering.azure.nsg-deny-all-outbound-baseline-and-outbound-restriction
name: nsg-deny-all-outbound-baseline-and-outbound-restriction
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, nsg, deny-all-outbound, outbound-restriction, service-tags, egress-control]
level: practitioner
status: docs-checked
description: "Restrict VM outbound traffic with NSGs: why default rules allow internet, a deny-internet baseline with service-tag allows, VirtualNetwork tag breadth and what breaks."
sources: ["https://learn.microsoft.com/azure/virtual-network/network-security-groups-overview#default-security-rules", "https://learn.microsoft.com/azure/virtual-network/service-tags-overview", "https://learn.microsoft.com/azure/virtual-network/what-is-ip-address-168-63-129-16"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NSG outbound restriction baseline

**Goal:** workloads can reach only the Azure services and destinations they need, even before a firewall is in path.

## Default outbound rules (can't delete, can override)
| Priority | Name | Effect |
|---|---|---|
| 65000 | AllowVnetOutBound | VirtualNetwork -> VirtualNetwork |
| 65001 | AllowInternetOutBound | Any -> Internet |
| 65500 | DenyAllOutBound | Deny everything else |

## Baseline pattern
```bash
NSG=nsg-app
az network nsg rule create -g rg --nsg-name $NSG -n allow-azuremonitor-out --priority 200 --direction Outbound \
  --access Allow --protocol Tcp --destination-address-prefixes AzureMonitor --destination-port-ranges 443
az network nsg rule create -g rg --nsg-name $NSG -n allow-entra-out --priority 210 --direction Outbound \
  --access Allow --protocol Tcp --destination-address-prefixes AzureActiveDirectory --destination-port-ranges 443
az network nsg rule create -g rg --nsg-name $NSG -n allow-storage-weu-out --priority 220 --direction Outbound \
  --access Allow --protocol Tcp --destination-address-prefixes Storage.WestEurope --destination-port-ranges 443
az network nsg rule create -g rg --nsg-name $NSG -n deny-internet-out --priority 4000 --direction Outbound \
  --access Deny --protocol '*' --destination-address-prefixes Internet --destination-port-ranges '*'
```
Use regional service tags where a tag supports them (the page's example form is `Storage.WestUS`; Storage and AzureCloud can be regional, AzureMonitor and AzureActiveDirectory can't).

## Know what you're allowing
- `VirtualNetwork` tag = VNet address space + connected on-premises ranges + peered VNets + VNets connected to a gateway + the host virtual IP + address prefixes used on UDRs - broad.
  For east-west restriction, use explicit prefixes/ASGs and a deny for VirtualNetwork above 65000.
- NSG rules match on source, source port, destination, destination port and protocol, not FQDN - use Azure Firewall for FQDN-based egress.

## What commonly breaks
- Windows licensing (KMS) sends an outbound request on TCP port 1688 - make sure it still gets out.
- OS updates/package repos, AV signature updates, monitoring agents and extension downloads - inventory with VNet flow logs before enforcing (NSG flow logs retire on 30 September 2027).
- The host virtual IPs 168.63.129.16 and 169.254.169.254 (DHCP, DNS, IMDS, health monitoring) are by default not subject to NSG rules; don't deny them with the AzurePlatformDNS, AzurePlatformIMDS or AzurePlatformLKM service tags unless you mean to.

## Gotchas
- Rules are stateful: return traffic for allowed inbound flows is permitted.
- New or updated rules apply only to new connections; existing flows continue.

## Verify
- [ ] Flow logs show only allowed destinations; `curl https://example.com` fails from a VM; agents and updates still work.

## Checked

2026-10-31. Confirmed against the Learn NSG overview (default rules and priorities 65000, 65001, 65500, priority range 100-4096, stateful flows, platform considerations for 168.63.129.16, KMS port 1688 and flow log retirement) and the service tags overview (VirtualNetwork tag contents, regional tags, AzureMonitor and AzureActiveDirectory tags). Removed: the azkms hostname, the NIC-before-subnet outbound ordering claim and the AzureCloud endpoints remark (none confirmed). Commands were checked with check_commands.py.

Method: documentation only; no commands were run.
