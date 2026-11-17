---
id: computing-software.networking-hardware-and-wireless.opnsense.interface-diagnostics-ping-traceroute
name: interface-diagnostics-ping-traceroute
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [ping, traceroute, port-probe, arp-table, ndp-table]
level: intro
status: docs-checked
description: "OPNsense connectivity tools: ping with source address and DF, traceroute with ASN column, port probe, ARP and NDP tables, DNS lookup and netstat views."
sources: ["https://docs.opnsense.org/manual/diagnostics_interfaces.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Ping, traceroute and other interface diagnostics

Ping (Interfaces > Diagnostics > Ping): fields are Hostname or IP, Address Family, Source address (any address configured on the firewall), Packet size (payload bytes; IP and ICMP headers are added), Do not fragment (sets the DF bit) and a Description. Use Do not fragment with a given size to find MTU problems. If the default ping fails but one with a specific source address works, you usually need a static route to push traffic via the right source; this is common with IPsec policy-based tunnels, which install a kernel trap on the source network. The jobs tab shows send, received, min, max, avg, loss and last_error per job, with stop, restart and remove.

Trace Route uses traceroute or traceroute6: Hostname or IP, Address Family, Protocol (UDP by default, ICMP if UDP fails) and Source address. The result includes the autonomous system number of hops, handy for building an alias of a provider's networks (BGP ASN type) to use in rules.

Port Probe tests whether a TCP port on a host accepts connections.

ARP Table lists IP, MAC, manufacturer, interface and, for DHCPv4 clients, hostname from the leases file. NDP Table does the same for IPv6. DNS Lookup runs a quick query from the firewall.

Netstat tabs (refresh icon updates data keeping the selection): Interfaces (packets and bytes per address), Protocol (system-wide protocol statistics), Sockets (netstat combined with sockstat, showing which process listens), Netisr (kernel network dispatch), Memory (mbuf pools) and Bpf (packets matched, dropped, received and buffer sizes of bpf peers).

## Checked

2026-11-03. Confirmed against the OPNsense Interface Diagnostics and Aliases manual pages: ping fields and job columns, traceroute defaults, ASN in results and the BGP ASN alias type, ARP and NDP tables, netstat tabs. Nothing removed.

Method: documentation only; no commands were run.
