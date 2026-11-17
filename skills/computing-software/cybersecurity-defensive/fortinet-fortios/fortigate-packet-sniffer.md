---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-packet-sniffer
name: fortigate-packet-sniffer
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [diagnose-sniffer, fortios, packet-capture, tcpdump-filter, sniffer-verbosity, pcap-from-fortigate]
level: practitioner
status: draft
description: "Capture packets on a FortiGate with diagnose sniffer, pick verbosity and filters, and save pcaps for analysis."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: see whether traffic arrives, leaves and in which form.

```
diagnose sniffer packet any 'host 10.1.0.5 and port 443' 4 100 l
diagnose sniffer packet port2 'icmp' 1
diagnose sniffer packet any 'host 203.0.113.80' 6 0 l
```
Arguments: interface (or `any`), filter (tcpdump syntax in single quotes), verbose level, count (0 = until stopped), timestamp (`l` local time, `a` absolute UTC).
Verbose levels: 1 headers, 2 headers and data, 3 headers with Ethernet, 4 headers with interface name, 5 headers, data and interface, 6 headers, data and Ethernet with interface.

Capture to a file for Wireshark: GUI Network > Packet Capture, or output level 6 piped through the Fortinet `fgt2eth.pl` script (confirm the script and instructions for your release).

Gotchas
- Offloaded traffic (NP6/NP7) may not appear after the first packets; disable offload for the policy during tests (`set auto-asic-offload disable`).
- `any` shows each packet on ingress and egress, which helps verify NAT (compare addresses).
- Long captures with data level 6 burden the CPU. Use count limits.

## Verify
A SYN from the client appears on the inbound interface and, after NAT and routing, on the outbound interface with the translated source address.
