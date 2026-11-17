---
id: computing-software.systems-network-administration.wireshark.choosing-interfaces-and-loopback-capture
name: choosing-interfaces-and-loopback-capture
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, dumpcap, capture-interfaces, loopback-capture, npcap-loopback, multi-interface-capture, pcapng]
level: practitioner
status: verified
description: "Pick the right capture interface: list interfaces with dumpcap -D, capture localhost traffic on Windows/Linux/macOS, and record several interfaces into one pcapng."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChCapInterfaceSection.html
  - https://www.wireshark.org/docs/man-pages/dumpcap.html
  - https://npcap.com/guide/npcap-users-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing interfaces and capturing loopback

## List what you can capture on
```
dumpcap -D            # numbered list: 1. eth0, 2. any, 3. lo (Loopback) ...
tshark -D
dumpcap -D -M         # machine-readable, includes extcap interfaces
dumpcap -L -i eth0    # link-layer types the interface supports (e.g. EN10MB, IEEE802_11_RADIO)
```
In the GUI the welcome screen sparklines show which interface carries traffic; pick that one rather
than guessing by name. On Windows, names are GUIDs; use the friendly names (`Ethernet 2`, `Wi-Fi`).

## Loopback (traffic to 127.0.0.1 / ::1 or to the host's own IP)
- Linux: interface `lo`. Traffic to the host's own non-loopback address also goes via `lo`.
- macOS and the BSDs can also capture loopback (Wireshark wiki, CaptureSetup/Loopback).
- Windows: Npcap installs `Adapter for loopback traffic capture` (`\Device\NPF_Loopback`).
  Current Npcap provides it without an install option (the `/loopback_support` installer flag is legacy, for Nmap 7.80 and
  older). WinPcap cannot capture loopback. Alternatives: `pktmon` (built into Windows) or the RawCap tool the Wireshark wiki names.
```
tshark -i lo -f "tcp port 8080"
tshark -i "\Device\NPF_Loopback" -f "tcp port 5432"
```
The Npcap loopback adapter's link type is NULL (BSD loopback, DLT_NULL); other platforms differ, so check with
`dumpcap -L -i <interface>`. Display filters on IP/TCP work the same.

## Several interfaces at once
```
dumpcap -i eth0 -i eth1 -w both.pcapng
tshark -i 1 -i 3 -w out.pcapng
```
pcapng records which interface each packet came from (`frame.interface_name`,
`frame.interface_id`); add it as a column. Classic pcap cannot hold multiple link types.

## Linux "any"
`-i any` captures all interfaces with the cooked SLL/SLL2 header (no real Ethernet header). SLL2 includes the interface
index of the interface the packet was seen on (tcpdump.org link-type page). Use it to find where traffic flows,
then capture on the specific interface for L2 detail.

## Gotchas
- Containers and VMs: traffic between containers on a bridge may never touch the physical NIC; capture on the
  bridge or the virtual ethernet pair instead.
- VPN clients: encrypted traffic on the physical NIC, cleartext on the tunnel adapter (the VPN adapter).
- Offloads (TSO/GRO) make host captures show 64 KB "packets" larger than the MTU; that is the
  NIC, not the wire.

## Verify
- [ ] The chosen interface shows the target conversation (Statistics > Conversations) before you
  start a long capture.

## Checked
Run on Wireshark 4.4.1 on Windows 11: `dumpcap -D -M` printed JSON with friendly names, `tshark -D` showed the numbered list with
friendly names in brackets, `dumpcap -L -i` listed NULL for the loopback adapter and EN10MB and DOCSIS for Wi-Fi, a two-interface capture
(`-i 10 -i Wi-Fi`, using the friendly name) wrote one pcapng whose packets carried `frame.interface_id` 0 and 1 with
`frame.interface_name` and description, and `tshark -i` with the loopback device path and with its number ran (no matching traffic).
The Npcap loopback behaviour and DLT_NULL come from the Wireshark loopback wiki and the Npcap Users' Guide, SLL2's interface index from
tcpdump.org, the sparkline traffic column from the User's Guide capture-options chapter, and the segmentation-offload effect from the Wireshark offloading wiki. Linux and macOS behaviour was not run here
and is stated only as far as those pages support it.
