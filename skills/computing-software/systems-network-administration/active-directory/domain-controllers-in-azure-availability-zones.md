---
id: computing-software.systems-network-administration.active-directory.domain-controllers-in-azure-availability-zones
name: domain-controllers-in-azure-availability-zones
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, azure, azure-dc-availability-zones, availability-sets, domain-controllers-on-azure]
level: practitioner
status: docs-checked
description: "Place Azure domain controller VMs across availability zones or an availability set, with static IPs, data disks without caching and per-region redundancy."
sources:
  - https://learn.microsoft.com/en-us/azure/architecture/example-scenario/identity/adds-extend-domain
  - https://learn.microsoft.com/en-us/azure/reliability/availability-zones-overview
  - https://learn.microsoft.com/en-us/cli/azure/vm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure DC availability zones and sets

## Placement
- Two or more DC VMs per region, each in a **different availability zone** (zone 1, 2, 3) where the region
  supports zones. Otherwise put them in one **availability set** (separate fault and update domains).
- One AD site per region (see azure-regions-as-ad-sites); DCs in every region your workloads run in.

```bash
az vm create -g rg-identity -n azdc01 --image <WINDOWS_SERVER_IMAGE> --zone 1 --size Standard_D2s_v5 \
  --vnet-name vnet-hub --subnet snet-identity --private-ip-address 10.10.1.4 --public-ip-address ""
az vm create -g rg-identity -n azdc02 --image <WINDOWS_SERVER_IMAGE> --zone 2 ... --private-ip-address 10.10.1.5
```

## Must-dos for any Azure DC
- Static private IP on the NIC (Azure side) rather than relying on DHCP; do not edit network settings inside the guest.
- NTDS/SYSVOL on a separate **data disk with host caching = None**.
- No public IP; use Azure Bastion for administrative access. Use persistent managed OS disks, not ephemeral ones.
- VNet DNS servers set to the DC IPs (plus an on-premises DC if needed); renew DHCP leases on VMs to pick up changes.
- Back up DCs with a supported system state backup (see the DC backup strategy skill).

## Gotchas
- Zones are not available in every region and not for every VM size; check before deployment.

## Verify
- [ ] `az vm show -d --query "{n:name,zone:zones}"` shows DCs in different zones.
- [ ] Each DC's data disk caching is None and `dcdiag` passes.

## Checked
2026-10-27, against the Learn page "Extend on-premises Active Directory to Azure" (architecture center), the `az vm` reference and the availability zones overview. Confirmed: at least two DC VMs in different zones, else an availability set; static private IP on the NIC; NTDS.dit, logs and SYSVOL on a separate data disk with Host Cache Preference None; persistent OS disks; no public IP and Azure Bastion; custom DNS at VNet level; `az vm create` options --zone, --private-ip-address, --public-ip-address, --vnet-name, --subnet and Standard_D2s_v5. Removed as unconfirmed: the SLA percentages, the Win2025Datacenter image alias, the Azure Backup VM-GenerationID claim, and the redeploy and resize notes.

Method: documentation only; no commands were run.
