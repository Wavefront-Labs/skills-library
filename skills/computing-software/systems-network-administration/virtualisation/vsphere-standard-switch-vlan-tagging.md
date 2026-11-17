---
id: computing-software.systems-network-administration.virtualisation.vsphere-standard-switch-vlan-tagging
name: vsphere-standard-switch-vlan-tagging
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vsphere-networking, standard-switch, vss-port-group, vst-vgt-est, vlan-4095, virtual-guest-tagging, port-group, esxcli, vmware, esxi, vsphere]
level: practitioner
status: draft
description: "Build vSphere standard switch port groups and pick VLAN tagging mode (EST, VST, VGT with 4095), with esxcli commands and the mismatches that black-hole traffic."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-networking-8-0.html
  - https://knowledge.broadcom.com/external/article?legacyId=1003806
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# vSphere standard switch port groups and VLAN tagging

**Goal:** VM and VMkernel traffic lands on the right VLAN, and every host in a cluster has
byte-identical port group names so vMotion and HA restarts work.

## Tagging modes
| Mode | Port group VLAN ID | Physical switch port | Who tags |
|---|---|---|---|
| EST (external switch tagging) | 0 / none | access port | physical switch |
| VST (virtual switch tagging) | 1-4094 | trunk with those VLANs allowed | vSwitch |
| VGT (virtual guest tagging) | 4095 | trunk | the guest OS (802.1Q inside the VM) |
VST is the normal choice. VGT is for appliances that need many VLANs (firewalls, nested
ESXi); on a vDS use a "VLAN trunking" range instead of 4095.

## Create with esxcli (repeat identically on every host, or script it)
```sh
esxcli network vswitch standard add -v vSwitch1
esxcli network vswitch standard uplink add -v vSwitch1 -u vmnic2
esxcli network vswitch standard uplink add -v vSwitch1 -u vmnic3
esxcli network vswitch standard portgroup add -v vSwitch1 -p "VM-App-120"
esxcli network vswitch standard portgroup set -p "VM-App-120" -v 120
esxcli network vswitch standard set -v vSwitch1 -m 9000        # only if the fabric is jumbo end to end
esxcli network vswitch standard portgroup list
```
PowerCLI for many hosts: `Get-Cluster <cl> | Get-VMHost | Get-VirtualSwitch -Name vSwitch1 |
New-VirtualPortGroup -Name VM-App-120 -VLanId 120`.

## Security policy (per vSwitch or port group)
Promiscuous mode, MAC address changes and forged transmits default to Reject on new
vSwitches in recent versions. Nested ESXi and some load balancers need MAC changes/forged
transmits Accept (or the MAC Learning policy on vDS 6.7+); grant it on a dedicated port
group only.

## Failure modes
- **Native VLAN mismatch:** VST port group with VLAN 10 while the switch sends VLAN 10
  untagged as native: frames arrive untagged and the port group drops them.
- **Port group name typo** on one host: vMotion fails with "network not accessible" and
  HA cannot restart VMs there.
- **VLAN not allowed on trunk** on one uplink only: intermittent loss depending on which
  uplink the VM's port hashes to. Test each uplink.

## Verify
On each host `esxcli network vswitch standard portgroup list` matches; from a test VM on
the port group ping the gateway, then disable each uplink in turn and ping again.
