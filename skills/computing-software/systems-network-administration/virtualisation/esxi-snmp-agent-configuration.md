---
id: computing-software.systems-network-administration.virtualisation.esxi-snmp-agent-configuration
name: esxi-snmp-agent-configuration
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [esxi-snmp, snmpv3, vsphere-monitoring, esxcli, hardware-alerts, vmware, vsphere]
level: practitioner
status: docs-checked
description: "Configure the ESXi SNMP agent for polling and traps with v3 users, communities, targets, hardware event sources, firewall, and test traps from esxcli."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-monitoring-and-performance/snmp-and-vsphere/configure-snmp-for-esx-esxi.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-monitoring-and-performance/snmp-and-vsphere/configure-snmp-for-esx-esxi/configure-esxi-for-snmp-v3.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-monitoring-and-performance/snmp-and-vsphere/configure-snmp-for-esx-esxi/configure-esxi-for-snmp-v3/configure-snmp-users.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESXi SNMP agent

ESXi has its own SNMP agent (disabled by default). Use it for hardware/link traps into an
NMS that can't use the vSphere API. vCenter alarms can also send SNMP traps separately
(see Configure SNMP Settings in the vCenter Server Configuration guide).

## SNMPv3 (preferred)
```sh
esxcli system snmp hash --auth-hash <authpass> --priv-hash <privpass> --raw-secret
#   -> returns hashed keys
esxcli system snmp set --users=nms/<authhash>/<privhash>/priv
esxcli system snmp set --enable=true
```
Set the engine ID, authentication/privacy protocols and v3 trap targets as described in
the Configure ESXi for SNMP v3 section of the monitoring guide.
SNMPv1/v2c (lab only): set communities and trap targets with `esxcli system snmp set`
(see Configure ESXi for SNMPv1 and SNMPv2c).

## Hardware event sources
The agent can take hardware events from CIM indications or IPMI sensors; see Configure
the Source of Hardware Events Received by the SNMP Agent. With vendor CIM providers
(Dell/HPE), indications give richer hardware traps.

## Filter noisy traps
`esxcli system snmp set --notraps <oid list>` suppresses specific traps (comma-separated
OIDs; `--notraps reset` clears the filter).

## Test
```sh
esxcli system snmp test          # sends a test trap to targets
esxcli system snmp get           # shows the full config
```
From NMS: `snmpwalk -v3 -u nms -l authPriv -a SHA -A ... -x AES -X ... esx01 1.3.6.1.2.1.1`.

## Gotchas
- Configure via host profiles for fleets; per-host engine IDs must be unique or v3 traps
  get confused at the receiver.
- SNMP polling of VM-level metrics is very limited; use the API for performance.
- Load the VMware MIBs into the NMS to decode traps.

## Verify
NMS receives the test trap from each host; a link-down on a test vmnic produces a trap.

## Checked
2026-10-31: `esxcli system snmp set --communities`, `esxcli system snmp hash --auth-hash/--priv-hash/--raw-secret`, the users configuration, `esxcli system snmp test` and `esxcli system snmp set --notraps <oid list>` (plus `--notraps reset`) confirmed on the Configure SNMP Communities, Configure SNMP Users and Configure the SNMP Agent to Filter Notifications pages; the engine ID, authentication/privacy, v3 targets, hardware-event source and VMware MIB topics confirmed in the SNMP section structure. Removed unconfirmed specifics: `--engineid`/`--v3targets`/`--hwsrc` flag forms, the firewall ruleset example, `Get-EsxCli -V2` and the warmStart trap name.
Method: documentation only; no commands were run.
