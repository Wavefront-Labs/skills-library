---
id: computing-software.networking-hardware-and-wireless.check-point.packet-capture-fw-monitor
name: packet-capture-fw-monitor
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, fw-monitor, packet-capture, inspection-points]
level: practitioner
status: draft
description: "Capture packets at each Check Point inspection point (i, I, o, O) with fw monitor, filters, and SecureXL notes."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_CLI_ReferenceGuide/Default.htm
  - https://support.checkpoint.com/results/sk/sk98348
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# fw monitor packet capture

```
fw monitor -e "accept src=10.1.10.55 or dst=10.1.10.55;" -o /var/tmp/mon.cap
fw monitor -F "10.1.10.55,0,203.0.113.9,443,6" -o /var/tmp/mon.cap
fw monitor -e "accept host(10.1.10.55) and port(443);" -m iIoO
fw monitor -p all -e "accept host(10.1.10.55);"      # pre-inbound positions
fw ctl chain                                          # list inspection chain modules
```
- Positions: **i** pre-inbound (before the firewall), **I** post-inbound (after the policy), **o** pre-outbound, **O** post-outbound. A packet visible at `i` but never at `I` was dropped by the firewall; seen at `I` and `o` but not at `O` means a drop at output (e.g. IPS); translation (NAT) shows as different addresses between `I`/`o`.
- `-o file` saves a pcap readable by Wireshark (fw monitor adds the position in the interface name "i/I/o/O" in the capture, Wireshark can show with the CheckPoint dissector).
- **SecureXL**: accelerated connections are mostly invisible to `fw monitor` after the first packets. For a capture, `fwaccel off` in a maintenance window and `fwaccel on` afterwards (this hurts performance); newer builds can capture accelerated flows with `-F` (confirm on your version).
- Always use a precise filter; unfiltered monitor on a busy gateway may crash the session or stall management.
- tcpdump is also valid for the NIC level (`tcpdump -nni eth1 host x`), but sees only before/after the firewall, not inside.

Verify: open the capture in Wireshark and confirm SYN at `i` and `I` for allowed traffic; a SYN present only at `i` means the policy or anti-spoofing dropped it, so follow with `fw ctl zdebug + drop`.
