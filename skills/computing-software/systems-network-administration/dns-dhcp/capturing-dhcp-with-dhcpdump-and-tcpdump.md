---
id: computing-software.systems-network-administration.dns-dhcp.capturing-dhcp-with-dhcpdump-and-tcpdump
name: capturing-dhcp-with-dhcpdump-and-tcpdump
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, dhcpdump, tcpdump, packet-capture, dhcp-options, troubleshooting]
level: practitioner
status: docs-checked
description: "Capture and read DHCP exchanges with tcpdump, tshark and dhcpdump, using the bbonev dhcpdump fork to see options and sessions."
sources:
  - https://github.com/bbonev/dhcpdump
  - https://www.tcpdump.org/manpages/tcpdump.1.html
  - https://www.wireshark.org/docs/man-pages/tshark.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Capturing DHCP with dhcpdump/tcpdump

DHCP uses UDP ports 67 (server) and 68 (client).

## tcpdump
```
tcpdump -ni eth0 -e 'udp port 67 or udp port 68'
tcpdump -ni eth0 -w dhcp.pcap 'udp port 67 or udp port 68'
```
- `-n` skips name resolution, `-e` prints the link-level header (MAC addresses on Ethernet), `-w` writes a capture file for later analysis.
- `-i any` captures on the pseudo-interface covering all interfaces, useful when the packet may arrive on a bonded or VLAN interface. Captures on `any` are not done in promiscuous mode.

## dhcpdump
`dhcpdump -i eth0` parses DHCP packets from an interface. The bbonev fork (based on dhcpdump 1.8) adds, among other things: reading traffic from a pcap file (`-r`), VLAN-tagged traffic, a hex dump of packet content, readable output for option 82, parsing of classless static routes (options 121 and 249), PXE options 93 and 94, and option 116. The unreleased 2.00 line adds an interactive session-tracking view (`-t`) that groups traffic by client and by transaction ID (XID) and shows the message flow (DISCOVER, OFFER, REQUEST, ACK) and a derived state such as offered, bound, NAK or timed out; it works live and on a capture.

## tshark
```
tshark -i eth0 -f "udp port 67 or udp port 68" -O dhcp
tshark -r dhcp.pcap -Y "dhcp.id == 0x3903f326" -T fields -e frame.time_relative -e dhcp.ip.your
```
`-f` is a capture filter, `-Y` a display filter, `-r` reads a file, `-O` shows full detail for the named protocol, and `-T fields -e <field>` prints chosen fields. Run tshark with `-z dhcp,stat` for DHCP statistics.

## Where to capture
- Client side: proves what the client sent and whether replies arrived.
- Server side: proves what the server received and answered. Compare both to locate where packets are dropped.

## Verify
- [ ] The capture shows the full DISCOVER, OFFER, REQUEST, ACK exchange for the test client with the options you expected.

## Checked
Method: docs-checked 2026-11-09 against the bbonev/dhcpdump README, the tcpdump man page (options -e, -n, -w, -i any) and the TShark man page (options -i, -f, -r, -Y, -O, -T fields, -e, -z dhcp,stat), all read. Dropped the tcpdump byte-offset filter, the claim that -vvv decodes DHCP options, the dhcpdump MAC regex flag and the Windows pktmon advice, which those pages do not confirm.
