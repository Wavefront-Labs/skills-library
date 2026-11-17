---
id: computing-software.systems-network-administration.virtualisation.vlcm-hardware-support-manager-firmware
name: vlcm-hardware-support-manager-firmware
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vlcm, hardware-support-manager, hsm, firmware-updates, omivv, hpe-oneview, xclarity, firmware-and-drivers-addon, vmware, vsphere]
level: advanced
status: draft
description: "Patch server firmware with ESXi through vLCM hardware support managers (Dell OMIVV, HPE OneView/iLO Amplifier, Lenovo XClarity): setup, firmware add-on and remediation."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vLCM firmware updates via hardware support managers

**Goal:** BIOS, BMC, NIC and storage controller firmware move in lockstep with the ESXi
image and its drivers, in one remediation, so driver/firmware combinations stay on the HCL.

## Pieces
- **Hardware support manager (HSM):** a vendor appliance/plugin registered with vCenter
  that exposes firmware packages: Dell OpenManage Integration for VMware vCenter (OMIVV),
  HPE OneView for VMware vCenter / iLO Amplifier, Lenovo XClarity Integrator, Cisco
  Intersight.
- **Firmware and drivers add-on:** selected in the cluster image (Image → Edit → Firmware
  and Drivers Addon), tied to a vendor catalogue/baseline.

## Setup outline
1. Deploy the vendor appliance, register it with vCenter, give it BMC credentials
   (cluster profile in OMIVV, server profile in OneView).
2. Point it at a firmware repository (vendor online catalogue or an internal share for
   air-gapped sites).
3. In the cluster image choose the HSM and firmware add-on version that the vendor
   pairs with your ESXi add-on.
4. Check compliance: firmware drift now appears alongside software drift.

## Remediation
vLCM puts the host in maintenance mode, the HSM stages firmware through the BMC, ESXi
reboots (no Quick Boot when firmware changes), firmware applies during POST, host returns.
Expect 20-45 minutes per host; plan windows accordingly.

## Gotchas
- vSAN clusters: storage controller firmware/driver mismatches are the most common HCL
  failure; let the HSM handle both.
- HSM appliance outage stops firmware compliance but not ESXi patching; monitor it.
- BMC credentials rotating without updating the HSM silently breaks firmware jobs.
- Vendor catalogues lag new ESXi releases; do not upgrade ESXi ahead of the firmware
  add-on's support for it.

## Verify
Cluster image compliance shows firmware compliant for all hosts; BMC inventory (iDRAC/iLO)
shows the expected versions; vSAN HCL check is green.
