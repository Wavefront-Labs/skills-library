---
id: computing-software.networking-hardware-and-wireless.strongswan.high-availability-ha-plugin
name: high-availability-ha-plugin
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, high-availability, ha-plugin, clusterip, load-sharing]
level: advanced
status: docs-checked
description: "Two-node strongSwan high availability and load sharing with ClusterIP and the ha plugin: how segments and SPIs spread SAs, and charon.plugins.ha options."
sources:
  - https://docs.strongswan.org/docs/latest/features/highAvailability.html
  - https://docs.strongswan.org/docs/latest/plugins/ha.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# high availability ha plugin
The page describes experimental pseudo active/active HA and load sharing with a cluster of initially two nodes, aimed at legacy IKEv2 clients (no protocol extension). Goals: failure detection and takeover within 1-3 seconds, state synchronization, transparent migration, load sharing and reintegration of repaired nodes.

**ClusterIP.** All nodes share one virtual IP and answer ARP with a multicast MAC, so the switch delivers packets to every node. A hash of the source address (and, for ESP, the SPI) picks the segment; each segment belongs to exactly one node, and the others drop the packet in netfilter. Non-responsible nodes verify an occasional packet to advance the replay window. Outbound flows stay on one node so sequence numbers are not duplicated. Kernel HA patches for many Linux versions are on the strongSwan download site; the ClusterIP module adds a PREROUTING hook plus XFRM_IN and XFRM_OUT hooks.

**Daemon side.** Build with `--enable-ha`. The ha plugin synchronises IKE and basic SA state and monitors heartbeats. It is currently designed for two nodes.

`charon.plugins.ha` options: `local` (receive address), `remote` (send address), `segment_count` (1), `secret` (PSK-authenticated IPsec tunnel for sync traffic), `monitor` (yes), `heartbeat_delay` (1000), `heartbeat_timeout` (2100), `resync` (yes), `autobalance` (0, off), `fifo_interface` (yes, segment administration), `buflen` (2048), `receive_buffer_size`, and an optional `pools` subsection for HA-enabled virtual IP pools shared by the nodes.

## Checked
2026-11-04. Confirmed against the strongSwan High Availability and ha plugin pages: ClusterIP behaviour, 1-3 second takeover goal, --enable-ha, two-node design, every charon.plugins.ha option and default listed. Nothing removed.

Method: documentation only; no commands were run.
