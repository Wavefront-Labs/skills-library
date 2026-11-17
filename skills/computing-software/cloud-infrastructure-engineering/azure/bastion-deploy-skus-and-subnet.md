---
id: computing-software.cloud-infrastructure-engineering.azure.bastion-deploy-skus-and-subnet
name: bastion-deploy-skus-and-subnet
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, bastion, bastion-deploy, bastion-sku, azurebastionsubnet, developer-sku, bastion-premium, bastion-nsg]
level: practitioner
status: docs-checked
description: "Deploy Azure Bastion: pick Developer/Basic/Standard/Premium SKU, size AzureBastionSubnet, apply the required NSG rules, zones and scale units."
sources: ["https://learn.microsoft.com/azure/bastion/configuration-settings", "https://learn.microsoft.com/azure/bastion/tutorial-create-host-portal", "https://learn.microsoft.com/azure/bastion/bastion-nsg", "https://learn.microsoft.com/azure/bastion/quickstart-developer-sku"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploy Bastion: SKUs, subnet and NSG

**Goal:** browser and native-client RDP/SSH to private VMs without public IPs on VMs, sized and
secured correctly first time.

## SKU choice
| SKU | Key features | Notes |
|---|---|---|
| Developer | Free, shared infra, one VM at a time, portal only | No subnet needed, dev/test only, limited regions |
| Basic | Portal RDP/SSH, 2 fixed instances, peered VNets | No native client, no IP-based connect, no scaling |
| Standard | Native client, IP-based connect, shareable links, file transfer, 2–50 scale units, custom ports | Production default |
| Premium | Standard + session recording, private-only Bastion (no public IP) | Compliance scenarios |
Upgrade Basic→Standard→Premium in place; downgrade requires delete/recreate.

## Subnet
- Name exactly **AzureBastionSubnet**, **/26 or larger** (needed for Standard scale units).
- Bastion needs outbound 443 to `AzureCloud` and 80 to `Internet` (see the NSG section), so check those requirements before sending the subnet's traffic through a firewall.
- Basic and higher reach VMs in peered VNets; Developer does not.

## Deploy
```bash
az network vnet subnet create -g rg-hub --vnet-name vnet-hub -n AzureBastionSubnet --address-prefixes 10.0.1.0/26
az network public-ip create -g rg-hub -n pip-bastion --sku Standard --zone 1 2 3
az network bastion create -g rg-hub -n bas-hub --vnet-name vnet-hub --public-ip-address pip-bastion \
  --sku Standard --scale-units 2 --enable-tunneling true --enable-ip-connect true --zones 1 2 3
```
Each instance (scale unit) supports up to 20 concurrent RDP and 40 SSH sessions; Basic has 2 fixed instances (40 RDP / 80 SSH).

## NSG on AzureBastionSubnet (optional but if present, must include)
Inbound: 443 from `Internet`; 443 from `GatewayManager`; 443 from `AzureLoadBalancer`; 8080, 5701 from `VirtualNetwork` to `VirtualNetwork`.
Outbound: 22, 3389 to `VirtualNetwork`; 443 to `AzureCloud`; 8080, 5701 `VirtualNetwork`→`VirtualNetwork`; 80 to `Internet` (session/cert validation).
Target VM NSGs: allow 3389/22 **from the AzureBastionSubnet prefix**, not from Internet.

## Gotchas
- A missing required NSG rule makes Bastion fail or misbehave; compare against the Bastion NSG page.
- Billing is hourly by SKU plus outbound data transfer (Developer is free); see the Bastion pricing page.
- Private-only (Premium) requires ExpressRoute/VPN reachability for users.

## Verify
- [ ] `az network bastion show -g rg-hub -n bas-hub` reports the expected SKU, scale units, tunneling and a succeeded provisioning state.
- [ ] Portal Connect → Bastion to a spoke VM with no public IP works.

## Checked

- 2026-10-27. Confirmed on Microsoft Learn (Bastion SKU comparison, configuration settings, Bastion NSG, private-only deployment, CLI reference for `az network bastion` and `public-ip`, limits page): the four SKUs and their feature split, AzureBastionSubnet name and /26 minimum, 2-50 instances for Standard/Premium, 20 RDP and 40 SSH sessions per instance, upgrade-only SKU path, NSG rule list, `--sku`, `--scale-units`, `--enable-tunneling`, `--enable-ip-connect`, `--zones` flags.
- Removed: the claims about forced tunnelling, one Bastion per VNet, subnet delegation, UDR restrictions and the 10-minute deployment time (not confirmed; the 10 minutes in the docs refers to upgrades), and the pricing wording.

Method: documentation only; no commands were run.
