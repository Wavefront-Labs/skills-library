---
id: computing-software.systems-network-administration.virtualisation.vsan-hcl-database-and-firmware-compliance
name: vsan-hcl-database-and-firmware-compliance
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vsan-hcl-database, vsan-hcl, vsan-health, driver-firmware, vsan, vmware, vsphere]
level: practitioner
status: draft
description: "Keep the vSAN HCL database current (online or offline JSON), clear controller driver and firmware compliance warnings, and fix them through vLCM."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=2145116
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vSAN HCL database and driver/firmware compliance

**Goal:** vSAN health checks compare controllers, drivers and firmware against a current compatibility list, and the cluster stays supported.

## Update the HCL database
- Online: Cluster -> Monitor -> vSAN -> Skyline Health -> *Hardware compatibility* -> Update from internet (vCenter needs internet or proxy).
- Offline: download `all.json` from `https://partnerweb.vmware.com/service/vsan/all.json` (or the current Broadcom location in KB 2145116) and upload it in the same place.
- Health warns *vSAN HCL DB up-to-date* when older than 90 days.

## Checks that use it
- *SCSI controller is VMware certified*
- *Controller driver is VMware certified* (driver name and version)
- *Controller firmware is VMware certified*
- *Controller disk group mode is VMware certified* (RAID0 vs passthrough/HBA mode)
- For ESA, *NVMe device is VMware certified*.

## Find what you have
```sh
esxcli storage core adapter list
esxcli software vib list | grep -Ei 'lsi|smartpqi|nvme|mpi3'
esxcli vsan debug controller list
```

## Fix through vLCM
Put the right driver in the cluster image (vendor add-on or component) and firmware through the Hardware Support Manager (Dell OMEVV, HPE iLO Amplifier/OneView, Lenovo XClarity). vLCM can show the *recommended* image that is vSAN HCL compliant. Remediate host by host (vSAN maintenance mode, *ensure accessibility*).

## Gotchas
- A driver newer than the certified one also triggers a warning; newer is not automatically better.
- Controller in RAID mode instead of HBA/passthrough is unsupported for vSAN on most controllers.
- Silencing the check hides real risk; only silence for documented exceptions.

## Verify
All *Hardware compatibility* checks green with a DB timestamp under 90 days.
