---
id: computing-software.systems-network-administration.wireshark.macos-wireless-diagnostics-sniffer
name: macos-wireless-diagnostics-sniffer
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, wlan, macos-wireless-sniffer, monitor-mode, macos]
level: practitioner
status: docs-checked
description: "Capture 802.11 frames on a Mac in monitor mode with Wireshark or tcpdump -I: disassociate first, set the channel, and know the airport command caveats."
sources:
  - https://wiki.wireshark.org/CaptureSetup/WLAN
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# macOS monitor-mode Wi-Fi capture

Macs can capture raw 802.11 frames with the built-in adapter, which is the easiest way to get an
over-the-air capture without extra hardware. Monitor mode is the only mode in which macOS gives
802.11 headers and non-data frames.

## Steps
1. Disassociate from the Wi-Fi network first. Some machines running macOS Mojave or later cannot
   stay associated while in monitor mode: the capture starts but sees no packets. Option-click the
   Wi-Fi item in the menu bar to disassociate, or run the `airport` utility with `-z`.
2. Set the channel to capture on. The `airport` utility is undocumented and not in the standard
   path; it lives in the Apple80211 private framework's Resources folder. `airport -I` shows the
   current channel and `airport -z` disassociates. System Integrity Protection blocks creating a
   link under /usr/sbin, so call it by full path, add its folder to PATH, or alias it.
3. In Wireshark, tick the Monitor mode checkbox in the interface settings (Edit Interface Settings
   in Wireshark 1.8 and later). On the command line the equivalent flag for dumpcap, tshark and
   Wireshark is `-I`.

```
tshark -I -i en0 -w air.pcap
```

## Gotchas
- One channel at a time; the capture covers only the channel the adapter is on.
- Captures are not decrypted. Decryption needs the keys in Wireshark's IEEE 802.11 preferences and
  the 4-way handshake in the capture.

## Verify
- [ ] Beacons and the client's frames appear with radiotap headers on the chosen channel.

## Checked
2026-11-09. Read the Wireshark wiki CaptureSetup/WLAN page, macOS section: monitor mode is the only
mode giving 802.11 headers and non-data frames, the Monitor mode checkbox and `-I` flag, the
Mojave-or-later need to disassociate first, the undocumented airport command with `-I` and `-z`,
and the SIP caveat. Removed: Wireless Diagnostics Sniffer steps, output file locations and
extensions, the tcpdump sudo form, and the claims about Apple Silicon and band support (the
Apple Support page cited earlier does not describe a sniffer). The airport sniff and channel
subcommand syntax was not confirmed and is not shown.
Method: docs-checked 2026-11-09 against the Wireshark wiki CaptureSetup/WLAN page.
