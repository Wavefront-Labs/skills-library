---
id: computing-software.systems-network-administration.backup-and-recovery.dr-failover-re-ip-and-dns-cutover
name: dr-failover-re-ip-and-dns-cutover
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [site-recovery, re-ip, failover, failback, disaster-recovery]
level: advanced
status: docs-checked
description: "Handle IP addressing in DR failover to Azure: retain IPs by failing over the subnet or assign new IPs, with the trade-offs Site Recovery documents."
sources:
  - https://learn.microsoft.com/en-us/azure/site-recovery/concepts-on-premises-to-azure-networking
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# DR failover networking: retain IPs or re-IP

**Goal:** after failover, users and systems reach the recovered servers at the DR site quickly and predictably. The facts below come from Azure Site Recovery (ASR) failover to Azure.

## Two options for the internal IP
- **Retain the same IP address** on the Azure VM as on-premises. This avoids potential network issues after failover but adds complexity.
- **Use a different IP address** on the Azure VM.

## Retaining IPs
- If the target Azure VM uses the same address or subnet as on-premises, you cannot connect the two with a site-to-site VPN or ExpressRoute, because the addresses overlap; subnets must be unique.
- Azure does not support stretched VLANs, so to keep addresses you take the IP space to Azure by failing over the entire subnet along with the machines.
- Subnet failover ensures a subnet is not available on-premises and in Azure at the same time.
- Manage subnets as part of the DR process: an Azure VNet matching the on-premises network, and route changes after failover to show the subnet has moved to Azure.
- Set the target network and IP in the Compute and Network properties of the replicated item before failover.
- Microsoft's example: apps with hard-coded IP addresses keep the same addresses by mirroring the subnet in a recovery VNet, and the production Azure network connects to it through VNet peering with transit connectivity enabled.

## Public addresses
You cannot reuse the on-premises public IP on an Azure VM. Assign a public IP manually, assign one during failover through a script or Azure automation runbook in a recovery plan, or use DNS-level routing with Azure Traffic Manager.

## Preparing guests
Configure Windows settings on the machine: remove static persistent routes and any WinHTTP proxy, and set the disk SAN policy to OnlineAll.

## Verify
In each DR test, measure the time from failover start to "users can connect by name or address", and note any hard-coded address that failed.

## Checked

2026-11-09. Confirmed against the Azure Site Recovery "networking" page (retain or new IPs, overlap and stretched VLAN limits, subnet failover, public IP options, Windows settings, example). Partial read; examples summarised. Removed: NIST SP 800-34 source (landing page, not relied on), stretched L2/VXLAN/EVPN/OTV and BGP route advertisement, Veeam, SRM and Zerto re-IP, DNS TTL values and DNS server advice, GSLB, the hard-coded IP hunt list and failback steps (not on the cited page).

Method: documentation only; no commands were run.
