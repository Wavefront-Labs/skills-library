---
id: computing-software.systems-network-administration.virtualisation.vds-health-check-vlan-mtu-teaming
name: vds-health-check-vlan-mtu-teaming
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vds-health-check, vds, mtu, vlan, nic-teaming, vmware, vsphere]
level: practitioner
status: docs-checked
description: "Enable the vDS health check to find VLAN trunk, MTU and teaming mismatches against the physical switch, read the Monitor tab results, and know its MAC-table impact."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=2032878
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# vDS health check (VLAN, MTU, teaming)

**Goal:** find physical-switch versus vDS mismatches before a VLAN, MTU or teaming change
causes an outage.

## What it checks
It monitors three parameters at a regular interval:
- **VLAN:** whether the vDS VLAN settings match the trunk port configuration on the adjacent
  physical switch ports.
- **MTU:** whether the physical access switch port MTU, per VLAN, matches the vDS MTU.
- **Network adapter teaming:** whether the physical switch ports' EtherChannel setting
  matches the port group's IP Hash teaming policy.

The default interval is one minute. It sends layer 2 Ethernet probe packets across the
vDS uplinks; if the connected device drops the REQ and ACK packets, that indicates a
configuration issue and a warning is shown in the vSphere Client.

## Requirements
- VLAN and MTU check: at least two physical uplinks connected to the vDS.
- Teaming check: at least two active uplinks in the team and at least two hosts in the vDS.

## Enable or disable
1. Browse to the vDS, open the Configure tab, then Settings > Health Check.
2. Click Edit and choose the options from the dropdowns: VLAN and MTU, and Teaming and
   Failover. Click OK. The same Edit dialog turns the check off.

## View results
Browse to the vDS, open Monitor > Health, and in Health Status Details choose the VLAN, MTU
or Teaming and Failover tab.

## Impact
The check generates a significant number of MAC addresses and extra network traffic. The
article's example: a vDS with 2 uplinks, 35 VLANs and 60 hosts gives 2 x 35 x 60 = 4200 MAC
table entries on the upstream physical switch. Make sure the count stays below the physical
switch MAC table size, or the switches can run out of memory and connectivity can fail.
After you disable the check, the generated MAC addresses age out per your network policy.
The check uses registered ethertype 0x8922.

## Checked
Date: 2026-11-07. Read the whole Broadcom KB article "Enabling vSphere Distributed Switch
health check in the vSphere Web Client" (the attached pcap was not opened; the
"vDS Health Check reports unsupported VLANs for MTU and VLAN" limitations article was not
opened). Removed as not on the page: the PowerCLI health-check snippet, the sample result
strings and their meanings, the "Unknown" status for single-uplink hosts, the MAC flap/CAM
remark, the "wait 2 intervals" advice and the "Normal" verify wording.
Method: documentation only; no commands were run.
