---
id: computing-software.systems-network-administration.virtualisation.esxi-fibre-channel-hba-zoning-lun-masking
name: esxi-fibre-channel-hba-zoning-lun-masking
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [fc-hba, lun-masking, fc-zoning, wwpn, fibre-channel, vmware, esxi, vsphere]
level: advanced
status: draft
description: "Connect ESXi hosts to Fibre Channel storage: find HBA WWPNs, single-initiator zoning, array host groups and LUN masking, rescans, and path checks."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-storage-8-0/using-esxi-with-fibre-channel-san.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fibre Channel HBAs, zoning and LUN masking

**Goal:** each host sees exactly the LUNs it should, on all expected paths, with a consistent LUN ID.

## Get WWPNs
```sh
esxcli storage san fc list            # Adapter, Port Name (WWPN), Node Name, Port State, Speed
esxcli storage core adapter list      # vmhba numbers and drivers
```
PowerCLI: `Get-VMHostHba -Type FibreChannel | Select VMHost, Device, @{n='WWPN';e={'{0:X}' -f $_.PortWorldWideName}}`.

## Zoning (switch)
- **Single-initiator, single-target** (or single-initiator, multi-target) zones using WWPN aliases. Never put two hosts' HBAs in one zone.
- Two fabrics (A/B), each HBA port to one fabric, each array controller in both.
- Brocade example: `alicreate esx01_hba0,"21:00:..."; zonecreate z_esx01_hba0_arrA,"esx01_hba0;arrA_ct0p0"; cfgadd prod_cfg,z_...; cfgenable prod_cfg`.

## Array side (masking)
- One host object per ESXi host with its WWPNs, grouped into a host group per cluster.
- Present each LUN to the host group with **the same LUN ID on every host**. Different IDs break RDMs and make troubleshooting painful.
- Host persona/type "VMware ESXi" (sets ALUA mode).

## ESXi side
```sh
esxcli storage core adapter rescan --all
esxcli storage core device list | grep -E '^naa|Display Name|Size'
esxcli storage nmp path list -d naa.<id>     # expect 4+ paths, ALUA Active/Optimised and Non-optimised
```
ESXi-side masking (rare) uses `esxcli storage core claimrule add -P MASK_PATH`, mainly to hide a LUN during decommissioning.

## Gotchas
- Port state *Link Down* on an HBA = cabling/SFP or switch port disabled.
- Datastore shows as *snapshot* after a LUN copy or new ID: do not resignature blindly (see datastore resignature procedures).
- Boot from SAN hosts need the boot LUN masked only to their own HBAs.

## Verify
Every host shows identical LUN IDs and the same path count; `esxcli storage core path list` has no dead paths.
