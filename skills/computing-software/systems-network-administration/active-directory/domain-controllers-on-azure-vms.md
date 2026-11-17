---
id: computing-software.systems-network-administration.active-directory.domain-controllers-on-azure-vms
name: domain-controllers-on-azure-vms
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, azure-domain-controller, azure-vm-domain-controller, ntds-data-disk, virtualized-domain-controller, hybrid, vnet-dns, availability-zones, azure-site, host-caching]
level: practitioner
status: docs-checked
description: "Run AD DCs on Azure VMs: NTDS on an uncached data disk, static private IP, VNet DNS, availability zones, an AD site for the VNet, and what not to do."
sources:
  - https://learn.microsoft.com/en-us/azure/architecture/example-scenario/identity/adds-extend-domain
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/virtual-dc/adds-on-azure-vm
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/introduction-to-active-directory-domain-services-ad-ds-virtualization-level-100
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Domain controllers on Azure VMs

**Goal:** extend an on-premises AD into Azure (or run it there) so Azure workloads
authenticate locally and survive a site link failure.

## Build
1. **Network:** hybrid connectivity (VPN or ExpressRoute). Put the DCs in their own subnet protected by an NSG, close all
   ports except those AD needs, and give each DC NIC a **static private IP** in Azure (the install prerequisite check
   warns about no static IP on the guest adapter; Microsoft says to ignore it because the address is assigned in the
   virtual network). Never give a DC a public IP; use Azure Bastion for admin access.
2. **Disks:** add a data disk and put the AD DS database, logs and SYSVOL on it, not on the OS disk. Set **Host Cache
   Preference to None** on that disk: the ESE database engine manages its own write ordering and caching would
   interfere with consistency.
3. **Availability:** at least two DC VMs in different availability zones, or an availability set where zones are not
   available. Consider assigning standby operations master roles.
4. **Promote** as an additional DC (see add-domain-controller skill) with
   `-DatabasePath <DATA_DRIVE>:\NTDS -LogPath <DATA_DRIVE>:\NTDS -SysvolPath <DATA_DRIVE>:\SYSVOL`.
5. **AD site:** create a site for the Azure subnets, then a site link to your on-premises sites; AD DS then handles
   replication.
6. **VNet DNS:** after the DCs are promoted, set the virtual network DNS servers to the Azure DCs as primary and
   secondary, with any on-premises DNS servers as tertiary and beyond. VMs keep their current DNS settings until they
   restart.

## Do not
- Do not shut a DC down from the Azure portal: that deallocates the VM. Shut down and restart the guest OS instead.
  Deallocating has side effects when the DC restarts (listed in the Azure Architecture Center article).
- Do not use snapshots or a rolled-back disk image as an AD backup: rolling a DC back outside its awareness causes USN
  rollback.
- Do not expose AD ports to the internet through a public IP or NSG rule.

## Verify
- [ ] Data disk Host caching = None (Portal > VM > Disks) and the NTDS database, logs and SYSVOL on it.
- [ ] Azure VMs resolve the Azure AD site with `nltest /dsgetsite`.
- [ ] `repadmin /replsummary` clean across the hybrid link.

## Checked

Date: 2026-10-27. Documentation: Azure Architecture Center "Deploy AD DS in an Azure virtual network" (adds-extend-domain),
the AD DS on Azure VM deployment article, and AD DS virtualization overview (Microsoft Learn pages read on
2026-10-27).
Confirmed: host cache None and its reason, static private IP and the prerequisite warning, NSG and public-IP guidance,
two VMs across availability zones or an availability set, AD site and site link, VNet DNS ordering and restart
behaviour, portal shutdown deallocation warning, USN rollback definition, `nltest /dsgetsite`.
Removed unconfirmed claims: the Azure-provided DNS `168.63.129.16` forwarder, Private Resolver forwarding, Azure Backup
being DC-aware, the OS-disk write-caching wording, the sysprep warning and the `restore VM` advice.

Method: documentation only; no commands were run.
