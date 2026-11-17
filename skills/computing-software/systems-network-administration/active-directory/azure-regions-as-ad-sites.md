---
id: computing-software.systems-network-administration.active-directory.azure-regions-as-ad-sites
name: azure-regions-as-ad-sites
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-sites, azure-ad-site, azure-domain-controller, site-links]
level: practitioner
status: docs-checked
description: "Model Azure VNets and regions as AD sites: subnets per VNet, site links to on-premises, replication schedule and keeping clients on Azure DCs."
sources:
  - https://learn.microsoft.com/en-us/azure/architecture/example-scenario/identity/adds-extend-domain
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/creating-a-site-link-design
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/move-addirectoryserver
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/new-adreplicationsubnet
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure regions as AD sites

Without a site, Azure VMs authenticate against on-premises DCs over the VPN/ExpressRoute and the Azure DCs
replicate as if they were next door.

## Design
- Create an AD site for the Azure location and add every VNet address space it serves as a subnet, so clients map to it.
- Site link from each Azure site to the on-premises sites with a cost that reflects the WAN; the default replication
  interval is 180 minutes, so set a shorter one if Azure data must converge sooner.
- At least two DCs in different availability zones (or an availability set where zones are unavailable).

## Build it
```powershell
New-ADReplicationSite -Name AZ-UKSouth
New-ADReplicationSubnet -Name 10.20.0.0/16 -Site AZ-UKSouth -Location "Azure UK South hub"
New-ADReplicationSubnet -Name 10.21.0.0/16 -Site AZ-UKSouth -Location "Azure UK South spokes"
New-ADReplicationSiteLink -Name "HQ-AZUKSouth" -SitesIncluded HQ,AZ-UKSouth -Cost 200 -ReplicationFrequencyInMinutes 15
Move-ADDirectoryServer -Identity AZDC01 -Site AZ-UKSouth
```
Enable change notification on the link if the WAN is fast and you want near-immediate replication:
`Set-ADReplicationSiteLink HQ-AZUKSouth -Replace @{options=1}`.

## Keep clients local
- VNet custom DNS points at the region's DCs.
- Add new VNets as subnets the same day they are created (automation: hook into the VNet pipeline). Clients on
  unmapped subnets cause Netlogon warning event 5807 on DCs.

## Egress cost
Outbound traffic through a VPN gateway is charged (inbound is free). Intersite replication is compressed and follows the
site link schedule, intrasite replication is not compressed, another reason to model Azure as its own site.

## Verify
- [ ] `nltest /dsgetdc:<domain>` on an Azure VM returns an Azure DC.
- [ ] `repadmin /showrepl` on Azure DCs shows inbound from the hub bridgehead only.

## Checked
2026-10-27, against the Learn pages "Extend on-premises Active Directory to Azure" (architecture center), the intersite replication topology page, the Setting Site Link Properties and Determining the Interval pages, and the New-ADReplicationSite/Subnet, New-ADReplicationSiteLink, Set-ADReplicationSiteLink and Move-ADDirectoryServer cmdlet pages. Confirmed: create an AD site that includes the Azure subnets and a site link to on-premises; at least two DCs in different zones or an availability set; default interval 180 minutes; `options=1` change notification; New-ADReplicationSubnet -Site -Location; Move-ADDirectoryServer -Identity -Site; Netlogon 5807; VPN outbound charge; intersite compression. Removed as unconfirmed: one site per region rule, the 15 to 30 minute figure and nltest /dsgetsite.

Method: documentation only; no commands were run.
