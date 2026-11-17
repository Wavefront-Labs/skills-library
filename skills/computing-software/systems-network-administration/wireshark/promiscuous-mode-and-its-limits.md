---
id: computing-software.systems-network-administration.wireshark.promiscuous-mode-and-its-limits
name: promiscuous-mode-and-its-limits
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, promiscuous-mode, switched-network, capture-point, monitor-mode, packet-capture]
level: practitioner
status: verified
description: "Know what promiscuous mode does and does not give you: switched networks deliver only your traffic, when to disable it, Wi-Fi limitations, and how to see other hosts' traffic."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChCapCaptureOptions.html
  - https://wiki.wireshark.org/CaptureSetup/Ethernet
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Promiscuous mode and its limits

Promiscuous mode tells the NIC to pass every frame it receives up the stack, not just frames
addressed to its MAC, broadcast and subscribed multicast. Wireshark enables it by default (`capture.prom_mode: TRUE`
in `tshark -G currentprefs`; the Capture Options dialog also has "Enable promiscuous mode on all interfaces", which
overrides the per-interface setting; `dumpcap -p` turns it off).

## What you actually see on a switched network
A switch only forwards to your port:
- unicast frames to and from your host,
- broadcasts (ARP, DHCP discover) and flooded multicast,
- unknown-unicast flooding (when the switch does not know a destination MAC).

So promiscuous mode on a laptop plugged into a normal access port does not show other users'
traffic. To see it you need a SPAN/mirror port, a TAP, or to capture on one of the endpoints.

## When to turn it off
- Some NICs, virtual switches and corporate endpoint agents refuse or log promiscuous requests;
  the capture fails with `failed to set hardware filter to promiscuous mode` (that text is in Npcap's `wpcap.dll`). Uncheck
  "Enable promiscuous mode on all interfaces" or use `dumpcap -p`.
- On a busy SPAN port where you only want your host's traffic, non-promiscuous capture plus a
  capture filter reduces load.

## Wi-Fi
On Wi-Fi, seeing 802.11 frames of other stations needs monitor mode (`dumpcap -I`, "capture in monitor mode, if available"), a
supported adapter, and the right channel, plus decryption keys for protected networks. On Windows, Npcap offers this
only if installed with "Support raw 802.11 traffic (and monitor mode) for wireless adapters" (`/dot11_support`),
which adds a second filter driver that gives frames a Radiotap header.

## Detecting promiscuous hosts
Security tools can detect promiscuous NICs: the nmap `sniffer-detect` script "checks if a target on a local Ethernet
has its network card in promiscuous mode" (techniques are in the paper it cites). Expect your capture laptop to be
noticed on monitored networks; get authorisation.

## Verify
```
dumpcap -i eth0 -p -w own-only.pcapng # non-promiscuous capture
```
- [ ] You know whether your capture point can see the target hosts (a ping from the target appears
  in the capture) before relying on an empty result.

## Checked
Checked with Wireshark 4.4.1 and Npcap on Windows: `capture.prom_mode` default TRUE from `tshark -G currentprefs`;
`dumpcap -h` lists `-p, --no-promiscuous-mode` and `-I, --monitor-mode`; the string "Enable promiscuous mode on all
interfaces" is in `Wireshark.exe` and the User's Guide says it overrides the individual settings; the error string is in
the Npcap folder's `wpcap.dll`; Npcap users guide read for the `/dot11_support` option; nmap NSE docs read for
`sniffer-detect`. Hypervisor settings and OS-specific Wi-Fi behaviour were removed.
