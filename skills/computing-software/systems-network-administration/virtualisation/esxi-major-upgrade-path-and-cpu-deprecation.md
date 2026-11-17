---
id: computing-software.systems-network-administration.virtualisation.esxi-major-upgrade-path-and-cpu-deprecation
name: esxi-major-upgrade-path-and-cpu-deprecation
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [esxi-major-upgrade, esxi-upgrade, cpu-deprecation, vmware, vsphere]
level: advanced
status: draft
description: "Plan an ESXi major version upgrade: supported paths, CPU and driver deprecations, boot media, order of operations and dry-run checks."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=82794
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/esxi-upgrade-8-0.html
  - https://interopmatrix.broadcom.com/Upgrade
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ESXi major upgrade path and CPU deprecation

**Goal:** move hosts to the next major release (for example 7.0 to 8.0) without stranding hardware or breaking clusters.

## Check before committing
1. **Upgrade path** in the Broadcom interoperability matrix (Upgrade tab): ESXi 8.0 accepts direct upgrades from 6.7 and 7.0. Older hosts need an intermediate hop or a fresh install.
2. **CPU support**: KB 82794 lists CPUs that are deprecated (warning) and discontinued (installer blocks). The installer reports `CPU_SUPPORT` errors. `allowLegacyCPU=true` at boot (Shift+O) bypasses the block but the result is unsupported.
3. **Drivers**: every NIC/HBA must have a native driver for the target release (vmklinux drivers were removed in 7.0). Check the VCG by PCI IDs from `esxcli hardware pci list`.
4. **Boot device**: SD/USB-only boot is deprecated; move OSDATA to durable local storage before or during the upgrade.
5. **vCenter version** must be equal or newer than target ESXi; upgrade vCenter first.

## Order of operations
vCenter -> (backup integrations, NSX, vSAN witness as required) -> ESXi hosts one cluster at a time -> VMware Tools -> VM hardware (optional) -> vDS version -> vSAN on-disk format.

## Methods
- **vLCM image**: set the cluster image to the new base image + vendor add-on, run compliance and remediation.
- **esxcli** (per host, maintenance mode):
```bash
esxcli software sources profile list -d /vmfs/volumes/ds01/VMware-ESXi-8.0U3-depot.zip
esxcli software profile update -d /vmfs/volumes/ds01/VMware-ESXi-8.0U3-depot.zip -p ESXi-8.0U3-standard --dry-run
esxcli software profile update -d /vmfs/volumes/ds01/VMware-ESXi-8.0U3-depot.zip -p ESXi-8.0U3-standard
```
Use `update`, not `install`; `install` overwrites third-party VIBs.
- **ISO**: boot the vendor custom ISO and choose *Upgrade ESXi, preserve VMFS datastore*.

## Gotchas
- EVC: a cluster's maximum EVC mode may change; check before mixing versions.
- Third-party VIBs absent from the target image (old vendor agents) block the upgrade; remove them or add the vendor add-on.
- Keep one host on the old version only briefly; HA and vMotion work across versions but feature parity does not.
- Fallback: Shift+R at boot reverts to the previous bootbank image right after an upgrade.

## Verify
`esxcli system version get` shows the new build; `esxcli software vib list` has no missing drivers; the host reconnects and VMs vMotion back.
