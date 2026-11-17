---
id: computing-software.systems-network-administration.virtualisation.esxi-hardware-health-cim-ipmi-sensors
name: esxi-hardware-health-cim-ipmi-sensors
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [ipmi-sensors, hardware-health, cim, esxi, vmware, vsphere]
level: practitioner
status: draft
description: "Monitor ESXi host hardware health through CIM providers and IPMI sensors, read the SEL with esxcli, reset sensors and alarm on failures."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-monitoring-and-performance-8-0/monitoring-host-health-status.html
  - https://developer.broadcom.com/xapis/esxcli-command-reference/latest/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Host hardware health via CIM and IPMI sensors

**Goal:** see failed fans, PSUs, DIMMs and disks in vCenter and get alerted.

## Where
Host -> **Monitor** -> *Hardware Health*: Sensors, Storage Sensors, Alerts and Warnings, System Event Log. Data comes from the BMC over IPMI and from vendor CIM providers.

## Prerequisites
- Vendor add-on installed (Dell, HPE, Lenovo) so CIM providers report RAID controllers and disks. Use the vendor custom ISO or vLCM vendor add-on.
- The WBEM/CIM service running:
```bash
esxcli system wbem get
esxcli system wbem set --enable true
/etc/init.d/sfcbd-watchdog restart
```

## esxcli
```bash
esxcli hardware ipmi sdr list        # sensors and current values
esxcli hardware ipmi sel list        # system event log entries
esxcli hardware ipmi fru list        # field-replaceable units
esxcli hardware ipmi bmc get         # BMC IP and firmware
```

## Alarms
The default alarm *Host hardware sensor state* (and per-component alarms for fan, power, temperature, memory, storage) triggers on sensor state changes. Add an email or SNMP action. Many teams use the BMC (iDRAC/iLO/XClarity) as the primary alert source and vCenter as a second view.

## Housekeeping
- After a hardware fix, use **Reset Sensors** and clear the SEL in the BMC so the old event stops showing.
- Full SELs stop logging new events; clear them periodically.

## Gotchas
- "Unknown" sensors usually mean missing or outdated CIM providers.
- Disable CIM where not used to reduce attack surface (CIS hardening), but then vCenter shows no storage sensors.

## Verify
Pull a redundant PSU in a lab: the sensor turns red and the alarm fires within a minute or two.
