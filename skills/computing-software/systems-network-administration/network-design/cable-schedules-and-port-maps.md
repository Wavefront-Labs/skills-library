---
id: computing-software.systems-network-administration.network-design.cable-schedules-and-port-maps
name: cable-schedules-and-port-maps
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, documentation, cable-schedule, port-map, patching-records, structured-cabling]
level: practitioner
status: docs-checked
description: "Maintain cable schedules and switch port maps: what fields to record, generating maps from LLDP/CDP and MAC tables, keeping them current through moves/adds/changes."
sources:
  - https://tiaonline.org/products-and-services/standards/
  - https://docs.netbox.dev/en/stable/models/dcim/cable/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cable schedules and port maps

## Cable schedule fields
Cable ID (the label), A-end (site/room/rack/U/device/port), B-end, media and grade (Cat6A,
OS2), length, colour, installer, test result reference, date, circuit/service carried.

## Port map fields (per switch)
Port, description, mode (access/trunk), VLAN(s), connected device/hostname, outlet/patch panel
port, PoE draw, speed/duplex, status, notes.

## Generating and reconciling
- **LLDP/CDP neighbours** give switch-to-switch and switch-to-AP/phone mappings: use the platform's
  neighbour detail output.
- **MAC + ARP tables** map hosts: the switch MAC table for the port, joined with the router's ARP table
  and DNS.
- Tools: NetBox (its cable model records terminations and a status such as Active, Planned or
  Decommissioning), port-discovery tools, or scripts that write CSV.
- Sync port descriptions from the source of truth (NetBox) to devices via automation so the device
  CLI reflects the map: `description AP-2F-14 | PP-2F-A:14`.

## Keep it current
- Every move/add/change ticket updates the schedule/map (definition of done).
- Scheduled reconciliation report: ports where LLDP/MAC data disagrees with the record.
- Unused ports: shut down and mark; reclaim after a set period unused.

## Verify
- [ ] Spot-check a sample of ports: record, device description and live LLDP/MAC data agree.

## Checked

2026-10-28: Confirmed in the NetBox cable model page: cables connect terminations (console ports, circuit terminations, power ports and so on) and carry a status (Active, Planned, Decommissioning). The TIA page and the Cisco LLDP page (404) gave nothing, so the TIA-606 label reference, the Cisco show commands, Netdisco/LibreNMS/Observium/Netmiko/NAPALM names, the 90-day reclaim figure and the 10-port sample size were removed.
Method: documentation only; no commands were run.
