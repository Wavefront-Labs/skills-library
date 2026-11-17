---
id: computing-software.cloud-infrastructure-engineering.azure.bastion-developer-sku-and-private-only-bastion
name: bastion-developer-sku-and-private-only-bastion
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, bastion, bastion-developer, private-only-bastion, bastion-premium, dev-test]
level: practitioner
status: docs-checked
description: "Pick the edge Bastion options: free Developer SKU for dev/test VMs (limits and setup) and Premium private-only Bastion with no public IP for ExpressRoute-only access."
sources: ["https://learn.microsoft.com/azure/bastion/quickstart-developer", "https://learn.microsoft.com/azure/bastion/private-only-deployment", "https://learn.microsoft.com/azure/bastion/bastion-sku-comparison"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bastion Developer SKU and private-only Bastion

**Goal:** cheapest secure access for dev boxes, and Bastion with zero internet exposure for regulated estates.

## Developer SKU
- Free, shared Microsoft-managed resource; **no AzureBastionSubnet and no public IP** needed.
- Limits (SKU comparison page): one VM connection at a time, no concurrent connections, no native client, no IP-Connect, no shareable links, no session recording, no connecting to VMs in peered virtual networks; availability zones only in select regions.
- Good for: sandbox and dev/test VMs; not for production admin access.
```bash
az network bastion create -g rg-dev -n bas-dev --vnet-name vnet-dev --sku Developer -l <supported-region>
```

## Private-only Bastion (Premium)
- Bastion with **no public IP**: reachable only from private networks (on-prem via ExpressRoute private peering
  or VPN), so admin traffic never touches the internet.
Deploy it as private-only at creation time (see the private-only deployment page); no `az network bastion create` flag for this appears in the CLI reference.
- For end-to-end private connectivity use the native client instead of the portal; an on-premises client also needs ExpressRoute or VPN and IP-based connection enabled on the Bastion resource.
- Must be decided at deployment (can't convert an existing public Bastion).
- Combine with session recording (Premium) for audited admin access.

## SKU choice recap
| Need | SKU |
|---|---|
| Dev/test, single VNet, free | Developer |
| Basic RDP/SSH from portal | Basic |
| Native client, IP connect, scale units, shareable links | Standard |
| Session recording, private-only | Premium |

## Gotchas
- Check the SKU comparison page for Developer SKU feature and region support.
- Private-only Bastion needs DNS/connectivity planning for clients; there's no fallback internet path.

## Verify
- [ ] Dev VM reachable via Developer SKU with no Bastion subnet; private-only Bastion unreachable from the internet and reachable from corp.

## Checked
2026-10-28. Confirmed on the SKU comparison, Developer quickstart, private-only deployment pages and `az network bastion` reference: free Developer SKU on a shared resource, no AzureBastionSubnet or public IP, one VM connection at a time, no concurrent connections, native client, IP-Connect, shareable link, peered VNet reach and session recording not in Developer, private-only needs Premium and is chosen at deployment (cannot convert), native client for end-to-end private use, `--sku {Basic, Developer, Premium, Standard}`.
Fixed: `--enable-private-only-bastion` does not exist in the CLI reference. Removed: the portal-blade and per-VNet deployment claims.

Method: documentation only; no commands were run.
