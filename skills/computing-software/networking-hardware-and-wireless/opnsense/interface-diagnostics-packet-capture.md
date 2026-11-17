---
id: computing-software.networking-hardware-and-wireless.opnsense.interface-diagnostics-packet-capture
name: interface-diagnostics-packet-capture
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [packet-capture, tcpdump, interface-diagnostics, pcap]
level: practitioner
status: docs-checked
description: "Run tcpdump captures from Interfaces > Diagnostics on OPNsense: filter fields, host expressions, count and length, job controls and downloads."
sources: ["https://docs.opnsense.org/manual/diagnostics_interfaces.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Packet capture

Interfaces > Diagnostics > Packet Capture starts a tcpdump process in the background on every selected interface. Options:

- Interface: one or more; a tcpdump runs on each.
- Promiscuous: capture all traffic on the segment, not only traffic addressed to the firewall.
- Address Family: IPv4, IPv6 or both. Protocol with Invert Protocol (all but the selected one).
- Host Address: source or destination IP, MAC or CIDR subnet, matched in either field. Prefix with "not" to negate and combine with boolean expressions, e.g. not 10.0.0.0/24 not and not 11.0.0.1 or 00:0a:01:02:03:04. Empty captures everything.
- Port with Invert Port: e.g. 443 or 22.
- Packet Length: bytes kept per packet; 0 (default) captures the whole frame.
- Count: packets per interface; default 100, 0 means unlimited.
- Description: label shown on the jobs tab.

The Jobs tab lists running and completed captures with actions: stop, remove (also stops an active one), restart (deletes earlier results), download a zip of pcap files plus a JSON of the options (open it in Wireshark), and three views (standard, medium, high detail). Views work while the capture runs and show what has been collected so far.

Typical uses in other docs: confirm dpinger ICMP leaves toward a gateway monitor address, check CARP source addresses, or look for ICMPv6 RS/RA traffic during IPv6 setup.

## Checked

2026-11-03. Confirmed against the OPNsense Interface Diagnostics, Gateways, Virtual IPs and IPv6 manual pages: every capture field, the defaults (length 0, count 100), job actions, downloads, and the dpinger, CARP and RS/RA uses. Removed: the unsupported advice about keeping count and length low.

Method: documentation only; no commands were run.
