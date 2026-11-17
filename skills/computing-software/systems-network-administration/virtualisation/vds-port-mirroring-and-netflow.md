---
id: computing-software.systems-network-administration.virtualisation.vds-port-mirroring-and-netflow
name: vds-port-mirroring-and-netflow
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [port-mirroring, vds-netflow, ipfix, erspan, vds, vmware, vsphere]
level: advanced
status: draft
description: "Capture VM traffic on a vSphere Distributed Switch with port mirroring sessions (local, RSPAN, ERSPAN) and export flows with NetFlow/IPFIX to a collector."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vDS port mirroring and NetFlow

**Goal:** see traffic of specific VMs (IDS, troubleshooting) or flow records (capacity, security) without touching guests.

## Port mirroring session types
| Type | Source | Destination | Use |
|---|---|---|---|
| Distributed Port Mirroring | vDS ports | vDS ports on the same host | sniffer VM next to the source |
| Remote Mirroring Source (RSPAN) | vDS ports | uplink with RSPAN VLAN | physical analyser via switch |
| Remote Mirroring Destination | RSPAN VLAN | vDS ports | receive RSPAN into a VM |
| Encapsulated Remote Mirroring (L3) ERSPAN | vDS ports | IP address (GRE) | analyser anywhere routed |

Create: vDS -> Configure -> Port mirroring -> New. Set direction (ingress/egress/both), **mirrored packet length** (for example 128 bytes to capture headers only), sampling rate, and *Normal I/O on destination ports* (leave off for sniffers).

## Destination VM
- Put the sniffer vNIC on a dedicated port group, promiscuous not needed for a mirror destination port.
- Same-host constraint for Distributed Port Mirroring: if DRS moves the source, the session stops. Use a DRS VM-VM affinity rule or ERSPAN.

## NetFlow / IPFIX
vDS -> Configure -> NetFlow: collector IP/port, observation domain ID, *switch IP address* (makes the vDS appear as one exporter), active flow timeout (60 s), idle (15 s), sampling rate (0 = every packet), *Process internal flows only* off. Then enable NetFlow per distributed port group (Monitoring -> NetFlow: Enabled).

## Gotchas
- Mirroring at full rate to a VM doubles traffic on that host; set a packet length and sample.
- ERSPAN needs the vmkernel route to the collector; vDS version 6.5+ for ERSPAN type III.
- NetFlow exports IPFIX (v10); old collectors that only speak v5/v9 show nothing.

## Verify
`tcpdump -i eth1` in the sniffer VM shows the source traffic; collector shows flows with the vDS switch IP as exporter.
