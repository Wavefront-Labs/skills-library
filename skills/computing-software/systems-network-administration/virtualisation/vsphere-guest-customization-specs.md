---
id: computing-software.systems-network-administration.virtualisation.vsphere-guest-customization-specs
name: vsphere-guest-customization-specs
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [guest-customization, customization-spec, sysprep, cloud-init, vm-template, domain-join, vsphere-vm-administration, vmware, vsphere]
level: practitioner
status: draft
description: "Create vSphere guest OS customisation specs for Windows (sysprep, domain join) and Linux (perl/cloud-init), with NIC mappings, scripts, and how to debug failed customisations."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=59557
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vSphere guest customisation specifications

**Goal:** clones come up with unique names, IPs, SIDs and domain membership without manual
console work.

## Windows
- Spec runs **sysprep** inside the clone (template must not already be sysprepped with
  OOBE, or keep it generalised and let the spec drive it; do not do both inconsistently).
- Settings: computer name (use VM name, or a prefix plus number), product key, admin
  password, time zone, run-once commands, network (DHCP or prompt for static IP), and
  **domain join** with a join-only service account.
- Windows sysprep can only rearm a limited number of times: always build from the
  template, not a clone of a clone.

## Linux
- Two engines: traditional **perl**-based (needs `open-vm-tools` and perl in the
  template) or **cloud-init** (vSphere 7U3+ with VMware datasource, spec type cloud-init
  where you pass metadata and userdata).
- Hostname, domain, time zone, NIC config (writes netplan/NetworkManager/ifcfg depending
  on distro), and a custom script with `precustomization`/`postcustomization` arguments.
- Custom scripts are disabled by default in recent open-vm-tools:
  `vmware-toolbox-cmd config set deployPkg enable-custom-scripts true` in the template.

## Apply
At clone/deploy select the spec (or "customize the operating system" and override per
VM). PowerCLI: `New-VM -Template t -OSCustomizationSpec spec -Name app03` plus
`Get-OSCustomizationNicMapping | Set-OSCustomizationNicMapping -IpMode UseStaticIP -IpAddress ...`
on a cloned non-persistent spec for static IPs.

## Debugging
- Windows: `%WINDIR%\Temp\vmware-imc\guestcust.log`, `%WINDIR%\Panther\setupact.log`.
- Linux: `/var/log/vmware-imc/toolsDeployPkg.log`, `/var/log/cloud-init.log`.
- vCenter events: "Customization started/succeeded/failed".
- Common causes: old VMware Tools in template, wrong guest OS type in VM settings,
  NIC count mismatch between spec and VM, domain account lacking join rights.

## Verify
Deploy a test VM per OS template monthly after template patching; confirm hostname,
IP, domain membership and that the "Customization succeeded" event appears.
