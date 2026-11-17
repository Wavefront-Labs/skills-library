---
id: computing-software.systems-network-administration.virtualisation.esxi-raw-device-mappings
name: esxi-raw-device-mappings
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [rdm, raw-device-mapping, vsphere-storage, wsfc, physical-compatibility, vmkfstools, vmware, vsphere]
level: practitioner
status: docs-checked
description: "Use raw device mappings correctly: physical vs virtual compatibility mode, WSFC shared disks, snapshot and vMotion limits, perennial reservation, and creating with vmkfstools."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-storage/raw-device-mapping-in-vsphere/characteristics-of-raw-device-mapping-in-vsphere/rdm-virtual-and-physical-compatibility-modes.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-storage/using-vmkfstools-in-vsphere/virtual-disk-options-of-vsphere-vmkfstools-command/creating-a-physical-compatibility-mode-raw-device-mapping.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Raw device mappings (RDM)

An RDM is a VMFS mapping file that points a VM disk at a whole LUN. Use only when needed:
WSFC/Oracle RAC shared disks with SCSI-3 persistent reservations (if vVols or clustered
VMDK are not options), array-based snapshot/replication tools inside the guest, or P2V of
a SAN boot disk.

## Modes
| | Virtual (vRDM, `-r`) | Physical (pRDM, `-z`) |
|---|---|---|
| SCSI commands | virtualised (only READ/WRITE pass) | all passed except REPORT LUNs |
| VM snapshots | yes | **no** |
| Storage vMotion | can convert to VMDK | mapping file only, data stays |
| WSFC across hosts | no | **yes** (SCSI-3 PR) |

## Create
UI: Add New Device → RDM Disk → choose LUN → compatibility mode; put a pRDM on a separate
SCSI controller with **Bus sharing: Physical** for WSFC.
```sh
vmkfstools -z /vmfs/devices/disks/naa.600xxxx /vmfs/volumes/DS01/sql01/sql01-quorum-rdmp.vmdk
vmkfstools -q /vmfs/volumes/DS01/sql01/sql01-quorum-rdmp.vmdk     # shows mapped device
```

## WSFC: perennially reserved
Hosts take minutes to boot or rescan when cluster LUNs are reserved by another node. Mark
them on every host:
```sh
esxcli storage core device setconfig -d naa.600xxxx --perennially-reserved=true
esxcli storage core device list -d naa.600xxxx | grep -i perennially
```

## Gotchas
- LUN must be presented with the **same LUN ID** to all hosts that run the VM.
- pRDM blocks VM-level backup (VADP cannot snapshot it); back up inside the guest.
- vMotion of a VM with bus-sharing pRDMs is supported only in vSphere 7+ with specific
  WSFC configurations; read the WSFC guide for your version.
- Deleting the RDM disk from the VM with "delete from disk" deletes the mapping file,
  not the LUN data.

## Verify
`vmkfstools -q` shows correct NAA; in guest, cluster validation storage tests pass; host
boot time normal after perennial reservation.

## Checked
2026-10-31: Confirmed virtual vs physical compatibility mode behaviour (READ/WRITE-only
virtualisation vs all-but-REPORT-LUNs passthrough, VMFS snapshots in virtual mode,
virtual-to-physical clustering) and >2 TB RDM support on VMFS5/6 against the vSphere 8.0
"RDM Virtual and Physical Compatibility Modes" page; the `vmkfstools -z` physical-mode
mapping syntax against the "Creating a Physical Compatibility Mode Raw Device Mapping"
page. Removed the 62/64 TB max-size row (not stated on the fetched pages).
Method: documentation only; no commands were run.
