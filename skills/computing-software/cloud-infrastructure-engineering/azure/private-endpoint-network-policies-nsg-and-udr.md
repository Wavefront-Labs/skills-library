---
id: computing-software.cloud-infrastructure-engineering.azure.private-endpoint-network-policies-nsg-and-udr
name: private-endpoint-network-policies-nsg-and-udr
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, private-link, private-endpoint-network-policies, pe-nsg, udr, firewall-inspection, route-tables]
level: advanced
status: gated
description: "Enable private endpoint network policies so NSGs and UDRs apply to PE traffic: settings, /32 route behaviour, firewall inspection with SNAT, and ASGs on PEs."
sources: ["https://learn.microsoft.com/azure/private-link/disable-private-endpoint-network-policy", "https://learn.microsoft.com/azure/private-link/inspect-traffic-with-azure-firewall", "https://learn.microsoft.com/azure/private-link/private-endpoint-overview#network-security-of-private-endpoints"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NSG and UDR on private endpoints (network policies)

**Goal:** private endpoint traffic obeys the same NSG and firewall-routing controls as everything
else in the spoke.

## Default behaviour
With network policies **disabled** (historic default): NSGs on the PE subnet don't filter
traffic to the PE, and each PE injects a **/32 system route** into the VNet and peered VNets
that overrides broader UDRs — traffic to PEs bypasses your firewall.

## Enable
```bash
az network vnet subnet update -g rg-app --vnet-name vnet-spoke -n snet-pe \
  --private-endpoint-network-policies Enabled        # or NetworkSecurityGroupEnabled / RouteTableEnabled
```
| Value | NSG applies | UDR can override /32 |
|---|---|---|
| Disabled | No | No |
| NetworkSecurityGroupEnabled | Yes | No |
| RouteTableEnabled | No | Yes |
| Enabled | Yes | Yes |
(The four values are documented; the per-value NSG/UDR split is inferred from the names (gated: unconfirmed, source is paywalled or blocked).)

## NSG on PE traffic
Inbound rules on the PE subnet NSG now filter clients → PE (e.g. allow 443 only from app subnets).
PEs can be members of **application security groups** (`--asg` on PE create / update ip config).

## Route PE traffic via the firewall
With RouteTableEnabled, the /32 routes still exist but a UDR with an equal or broader prefix
can override them **if** the UDR is on the client subnet: since the subnet-level setting
invalidates the /32 for UDR comparison, a route `10.20.5.0/24 → firewall` (PE subnet) on client
subnets wins.
- **SNAT on the firewall** for traffic to PEs is recommended (Azure Firewall always SNATs traffic matched by application rules, so prefer them for private endpoints; with network rules or an NVA, configure SNAT) to keep return traffic symmetric — SNAT keeps return traffic symmetric.
- Firewall processing is charged for every inspected flow; check the pricing page.

## Gotchas
- The setting is per subnet — PEs in subnets without it still bypass.

## Verify
- [ ] `az network vnet subnet show ... --query privateEndpointNetworkPolicies` = Enabled.
- [ ] Effective routes on a client NIC show the UDR to the firewall for the PE prefix (or /32 marked invalid).
- [ ] Firewall logs show client → PE flows; NSG deny test blocks a non-approved subnet.

## Checked
2026-10-28. Confirmed on the Learn network-policies, inspect-traffic and private endpoint overview pages: the `privateEndpointNetworkPolicies` values Disabled, NetworkSecurityGroupEnabled, RouteTableEnabled, Enabled; a route with prefix length equal or larger than the VNet prefix overrides the PE /32 route; Azure Firewall always SNATs application-rule traffic; SNAT is recommended for PE traffic; ASG support (up to 50 IP configurations per ASG). Gated: the per-value NSG/UDR table cells. Removed: SQL redirect port range, flow-log claim, return-path wording, cost wording.
Method: documentation only; no commands were run.
