---
id: computing-software.systems-network-administration.virtualisation.vsphere-distributed-power-management
name: vsphere-distributed-power-management
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [distributed-power-management, dpm, ipmi, ilo, wake-on-lan, host-power-management, drs, resource-management, vmware, vsphere]
level: practitioner
status: draft
description: "Configure vSphere DPM to power off spare hosts at low load: IPMI/iLO or WoL wake-up tests, thresholds, host overrides, and the HA and vSAN conflicts to avoid."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-resource-management-8-0/using-drs-clusters-to-manage-resources/managing-power-resources.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# vSphere Distributed Power Management (DPM)

**Goal:** save power by putting under-used hosts into standby at night or weekends, and
be sure they wake when demand returns.

## Requirements
- DRS enabled. DPM consolidates VMs onto fewer hosts with vMotion, then puts emptied hosts
  in **standby** (powered off).
- Wake-up method per host: **IPMI** or **iLO** (BMC address, MAC and credentials entered
  under Host → Configure → System → Power Management), or **Wake-on-LAN** over the vMotion
  network (NIC must support it, switch ports must stay up when the host is off).
- **Test** each host: right-click → Power → Enter Standby Mode, then Power On. A host
  that fails to wake will be excluded, but only after it has failed once in production.

## Settings
- Automation: Off, Manual (recommendations), Automated.
- **DPM threshold** 1-5: how aggressively hosts are powered on/off (target utilisation
  band roughly 45-81% by default).
- **Host overrides:** set Disabled for hosts that must stay on (vSAN witness-hosting, hosts
  with local-only VMs, hosts with passthrough devices).

## Conflicts
- **HA admission control** keeps enough hosts powered on to honour the failover
  capacity; DPM respects it, so savings on small clusters are tiny.
- **vSAN** clusters: powering off hosts removes their storage; DPM is not supported
  with vSAN.
- Monitoring systems will alarm on standby hosts; suppress host-down alerts for hosts in
  standby state.
- Long boot times (large memory servers with full POST) mean slow reaction to sudden load.

## Alternative
Scheduled tasks ("Change cluster power settings") enable DPM only out of hours, keeping
all hosts up during business days.

## Verify
Every host shows a successful last exit from standby; Cluster → Monitor → DRS history
shows standby/power-on operations at expected times; no capacity alarms during wake-up.
