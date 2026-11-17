---
id: computing-software.systems-network-administration.wireshark.airmon-ng-monitor-mode-and-channel-hopping
name: airmon-ng-monitor-mode-and-channel-hopping
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, wlan, airmon-ng, channel-hopping, monitor-mode, iw]
level: practitioner
status: docs-checked
description: "Put a Linux WLAN adapter into monitor mode with airmon-ng or iw, fix or hop channels, and capture 802.11 management and control frames in Wireshark."
sources:
  - https://www.aircrack-ng.org/doku.php?id=airmon-ng
  - https://wiki.wireshark.org/CaptureSetup/WLAN
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitor mode and channel selection with airmon-ng

## Why monitor mode
Without it, a WLAN capture usually shows only user data packets with "fake" Ethernet headers and none
of the 802.11 management or control frames. On Linux and macOS you only get 802.11 headers in monitor
mode. It is also what you need for traffic between other machines or for radio-layer information.
Support is very platform, adapter and driver dependent.

## airmon-ng
Usage: `airmon-ng <start|stop> <interface> [channel]` or `airmon-ng <check|check kill>`.
```
sudo airmon-ng check            # list processes that may interfere
sudo airmon-ng check kill       # stop network managers, then kill what is left
sudo airmon-ng start wlan0      # for mac80211 drivers this creates wlan0mon
sudo airmon-ng stop wlan0mon
```
- The aircrack-ng page says it is very important to kill the network managers before putting a card
  in monitor mode. Starting monitor mode also runs the interference check.
- With mac80211 drivers capture on the new monitor interface (named `wlan0mon` on current versions,
  `mon0` in older examples), not the original one, and stop that monitor interface to leave
  monitor mode. With drivers that do not use mac80211, capture on the interface you named.
- Afterwards restart the network manager (for example `service network-manager start`).

## Without airmon-ng (iw)
The Wireshark wiki describes creating a monitor interface with iw
(`iw dev <interface> interface add mon<N> type monitor`), bringing it up, capturing on it, then
deleting it with `iw dev mon<N> interface del`. Its example script also sets a fixed channel with
`iw dev mon0 set channel 11`. Wireshark can also set up a monitor interface itself.

## In Wireshark
Wireshark 1.4 or later with libpcap 1.0 or later shows a "Monitor mode" checkbox in Capture Options
for interfaces that support it; the command-line flag is `-I` for dumpcap, tshark and Wireshark. In
the GUI pick a radio information link-layer header type (for example the 802.11 plus radiotap
variant) if one is offered.

## Channel hopping
- A card in monitor mode captures one channel at a time, so hopping inevitably loses traffic. Hop
  first to find the networks in range, then pick a channel for analysis.
- To troubleshoot one AP or station, capture on a single fixed channel.
- Wireshark has no built-in channel hopping; run a separate process to hop (Kismet is the wiki's
  suggested tool, configured through kismet.conf) while Wireshark captures.

## Verify
- [ ] Beacons or other management frames from the target AP appear in the capture on the expected
  channel.

## Checked
Method: docs-checked 2026-11-09 against the aircrack-ng airmon-ng page (usage, check kill, start and stop examples read) and the Wireshark CaptureSetup/WLAN wiki (monitor mode, Linux and channel hopping sections read). The kernel iw page was dropped as a source (it did not support the quoted commands). Dropped unconfirmed claims: iw set type monitor/set channel width syntax, 6 GHz and regulatory domain advice, chipset recommendations, airodump-ng band option, radiotap signal filters.
