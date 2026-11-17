---
id: computing-software.cloud-infrastructure-engineering.azure.public-ip-skus-and-basic-ip-retirement-upgrade
name: public-ip-skus-and-basic-ip-retirement-upgrade
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, public-ip-sku, basic-ip-retirement, public-ip-upgrade, standard-public-ip, public-ip-prefix]
level: practitioner
status: docs-checked
description: "Manage Azure public IPs: Standard vs Basic behaviour, finding and upgrading retired Basic IPs while keeping the address, zones, tiers and public IP prefixes."
sources: ["https://learn.microsoft.com/azure/virtual-network/ip-services/public-ip-basic-upgrade-guidance", "https://learn.microsoft.com/azure/virtual-network/ip-services/public-ip-upgrade-vm", "https://learn.microsoft.com/azure/virtual-network/ip-services/public-ip-addresses"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Public IP SKUs and Basic IP retirement

**Goal:** no Basic public IPs left (retired 30 September 2025), and Standard IPs designed for zones and security.

## Standard vs Basic
| | Standard | Basic (retired) |
|---|---|---|
| Inbound by default | **Closed** - needs NSG allow | Open |
| Allocation | Static only | Dynamic or static |
| Zones | Zone-redundant / zonal | None |
| Works with | Standard LB, NAT GW, AGW v2, Firewall, Bastion | Basic LB |

## Find leftovers
```kusto
resources
| where type == "microsoft.network/publicipaddresses" and sku.name == "Basic"
| project id, ip = properties.ipAddress, attachedTo = tostring(properties.ipConfiguration.id), allocation = properties.publicIPAllocationMethod
```

## Upgrade keeping the address
- Unattached IP: set static then upgrade.
```bash
az network public-ip update -g rg -n pip-legacy --allocation-method Static
az network public-ip update -g rg -n pip-legacy --sku Standard
```
- Attached to a VM NIC: use Microsoft's VM public IP upgrade PowerShell script (PowerShell Gallery) which dissociates,
  upgrades and re-associates, retaining the IP; or do the same steps manually in a window.
- Attached to a Basic load balancer: upgrade the LB with the Basic LB upgrade script, which handles its IPs.
- Add an **NSG** allowing required inbound before/at upgrade - Standard IPs are closed by default.

## Designing new IPs
- Standard IPs can be non-zonal, zonal or zone-redundant (zone-redundant needs a region with 3 availability zones live).
- Tier: Regional (default) or **Global** (for cross-region load balancer).
- Routing preference: Microsoft network vs Internet; see the pricing page for the cost difference.
- **Public IP prefixes** give contiguous, predictable ranges for allow-lists (check the allowed prefix lengths on the public IP prefix page):
```bash
az network public-ip prefix create -g rg-net -n ippre-egress --length 30 --zone 1 2 3
az network public-ip create -g rg-net -n pip-egress-1 --public-ip-prefix ippre-egress --sku Standard
```

## Gotchas
- Switch a Basic IP to static before upgrading so the address is retained.

## Verify
- [ ] ARG query returns no Basic SKU IPs; upgraded endpoints reachable with the same address and expected NSG rules.

## Checked
2026-10-28. Confirmed on the public IP Learn pages: Basic SKU public IPs were retired on 30 September 2025 (the skill said September 2025), Standard upgrade guidance. check_commands confirmed the az public-ip commands and flags. Removed: typical prefix length range, egress-cost claim, DDoS SKU claim, the dynamic-IP-lost claim. Also confirmed on the public IP addresses page: Standard closed by default with NSG required, Basic open by default, zone support only for Standard, Global tier for cross-region load balancers.
Method: documentation only; no commands were run.
