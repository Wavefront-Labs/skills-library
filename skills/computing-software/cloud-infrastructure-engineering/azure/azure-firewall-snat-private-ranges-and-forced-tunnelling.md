---
id: computing-software.cloud-infrastructure-engineering.azure.azure-firewall-snat-private-ranges-and-forced-tunnelling
name: azure-firewall-snat-private-ranges-and-forced-tunnelling
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-firewall, snat-private-ranges, management-nic, forced-tunneling, azurefirewallmanagementsubnet]
level: advanced
status: docs-checked
description: "Control Azure Firewall SNAT (private ranges, always/never SNAT) and send internet traffic on-prem with forced tunnelling using the management NIC and its subnet."
sources: ["https://learn.microsoft.com/azure/firewall/snat-private-range", "https://learn.microsoft.com/azure/firewall/forced-tunneling", "https://learn.microsoft.com/azure/firewall/management-nic"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firewall SNAT private ranges and forced tunnelling

**Goal:** predictable source IPs through the firewall, and the option to route internet egress via on-prem security stacks.

## SNAT behaviour
- **Network rules**: Azure Firewall SNATs to its public IP only when the destination is **not** in the private
  ranges list. Default private ranges = IANA RFC 1918 + RFC 6598 (100.64.0.0/10).
- **Application rules**: always SNAT (to a firewall instance's private IP for private destinations).
- If your organisation uses registered (non-RFC 1918 / RFC 6598) IP space internally, add it to the private ranges or network-rule flows to it are SNATed to one of the firewall's private IPs in AzureFirewallSubnet (and may break).
```bash
az network firewall policy update -g rg-hub -n fwpol-hub --private-ranges IANAPrivateRanges 203.0.113.0/24
# always SNAT:  --private-ranges 255.255.255.255/32
# never SNAT:   --private-ranges 0.0.0.0/0
```
Auto-learn SNAT ranges requires the firewall to be associated with Azure Route Server (for VNet deployments, Route Server must be in the same VNet as the firewall).

## Forced tunnelling
Send 0.0.0.0/0 from the firewall to on-prem or an NVA instead of the internet:
1. The firewall needs a **management NIC**: subnet `AzureFirewallManagementSubnet` (/26) with its own public
   IP (or no public IP when the management NIC is deployed without one); the platform uses it for management traffic (its route table must keep 0.0.0.0/0 -> Internet).
2. Route table on `AzureFirewallSubnet`: 0.0.0.0/0 -> next hop VirtualAppliance (on-prem path via NVA) or learn the
   default route via BGP from the VPN/ExpressRoute gateway.
```bash
az network firewall create -g rg-hub -n fw-hub --sku AZFW_VNet --tier Premium --vnet-name vnet-hub \
  --conf-name fw-ipconfig --public-ip pip-fw --m-conf-name fw-mgmt --m-public-ip pip-fw-mgmt
```
The management NIC can be enabled at creation or on an existing firewall (see "Enable the management NIC on existing firewalls" on the management NIC page).

## Gotchas
- Without SNAT, the next hop (on-prem) must route return traffic back to Azure via the firewall.

## Verify
- [ ] Flows to internal "public" ranges keep original source IPs (check destination logs); `curl ifconfig.me` from a spoke shows the on-prem egress IP when forced tunnelling is on.

## Checked

- 2026-10-27. Confirmed on Microsoft Learn (Azure Firewall SNAT private IP address ranges, management NIC, forced tunneling, CLI reference for `az network firewall` and `firewall policy`): network rules do not SNAT to private ranges by default (IANA RFC 1918 and RFC 6598), application rules always SNAT, `255.255.255.255/32` = always SNAT, `0.0.0.0/0` = never SNAT, `--private-ranges` flag, AzureFirewallManagementSubnet minimum /26, default route to Internet only on the management subnet, `--m-conf-name` and `--m-public-ip` flags, `--sku AZFW_VNet`, `--tier Premium`, auto-learn needs Route Server.
- Corrected: SNAT target for non-private public ranges (private IP in AzureFirewallSubnet, not the public IP); management NIC can be enabled on existing firewalls. Removed: the DNAT-with-forced-tunnelling note and the policy-wide impact claim (not confirmed).

Method: documentation only; no commands were run.
