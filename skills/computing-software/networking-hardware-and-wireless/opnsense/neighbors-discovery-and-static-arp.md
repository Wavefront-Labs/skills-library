---
id: computing-software.networking-hardware-and-wireless.opnsense.neighbors-discovery-and-static-arp
name: neighbors-discovery-and-static-arp
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [neighbors, hostwatch, arp, ndp, static-arp]
level: practitioner
status: docs-checked
description: "Use Interfaces > Neighbors on OPNsense: hostwatch automatic discovery settings, discovery log for flapping, and static ARP/NDP mappings."
sources: ["https://docs.opnsense.org/manual/neighbors.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Neighbors, host discovery and static mappings

Neighbors are hosts on the same layer-2 broadcast domain; each host has its own neighbor table. A firewall acting as default gateway learns most neighbors automatically.

Automatic Discovery (Interfaces > Neighbors > Automatic Discovery) runs the hostwatch service, which builds a persistent database of hosts from ARP and NDP messages and logs when IP to MAC mappings change. It shows how volatile the network is and when unknown hosts appear, and services that read ARP/NDP tables get faster queries and a better picture of RFC 4941 temporary IPv6 addresses. Settings: Enable, Interfaces (limit discovery), Promiscuous mode (rarely needed because the firewall already sits centrally; useful only where it is a pure observer), Verbose logging and Ignore networks. Only ethernet interfaces are monitored; tunnel and loopback interfaces are skipped.

The Discovered Hosts table shows the database when the service is on, otherwise the kernel ARP and NDP tables. The Last Seen column shows newly joined or long-absent hosts. The Discovery Log records new stations and movements in a simple format an external syslog server can consume, for example to alert on new hosts. Many entries that look like flapping suggest a MAC address duplication or hosts fighting over an IP.

Static Assignments define fixed IP to MAC mappings: Ether Address (xx:xx:xx:xx:xx:xx), IP address, Description. IPv4 entries land in the ARP table and IPv6 entries in the NDP table, useful when ARP/NDP messages are not received or to force a pairing. Entries from other sources such as DHCP appear but cannot be edited.

## Checked

2026-11-03. Read the Neighbors manual page (neighbors.html) on docs.opnsense.org and confirmed the claims above against them. Nothing needed removing.
Method: documentation only; no commands were run.
