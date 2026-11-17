---
id: computing-software.systems-network-administration.wireshark.wlan-traffic-statistics
name: wlan-traffic-statistics
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, wlan, wlan-traffic-statistics, bssid, channel-utilisation, statistics]
level: practitioner
status: docs-checked
description: "Use Wireshark's Wireless > WLAN Traffic statistics to summarise wireless networks in a capture, and tshark io,stat for retry counts per interval."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChWirelessWLANTraffic.html
  - https://www.wireshark.org/docs/man-pages/tshark.html
  - https://www.wireshark.org/docs/dfref/w/wlan.html
  - https://www.wireshark.org/docs/dfref/r/radiotap.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wireless LAN traffic statistics

The Wireless menu has a WLAN Traffic window that summarises the wireless network traffic in the
capture. Each row shows the statistics for exactly one wireless network. Probe requests are merged
into an existing network when the SSID matches.

## Using it
- Open it before or during a live capture: the window updates frequently.
- Only show existing networks excludes probe requests whose SSID matches no network in the list.
- Name resolution is applied if selected in the window and active for the MAC layer.
- Copy puts the list on the clipboard as CSV.
- Co-channel contention: look for many networks on the same channel in one location.
- To filter on a network, use its BSSID with the `wlan.bssid` display filter field.

## tshark
Beacon summary of networks heard (field names exist in the Wireshark wlan and radiotap references):
```
tshark -r air.pcapng -Y "wlan.fc.type_subtype==0x0008" -T fields -e wlan.bssid -e wlan.ssid -e wlan.ds.current_channel -e radiotap.dbm_antsignal
```
Pipe the output through `sort -u` to list each network once.

## Retries
```
wlan.fc.retry == 1
tshark -r air.pcapng -q -z io,stat,1,"wlan.fc.retry==1","wlan.fc.type==2"
```
`io,stat,interval,filter...` prints a row per interval with a column per filter. Compare retried
frames with data frames (type 2) over the same intervals, and judge the ratio against a healthy
baseline from the same network.

## Gotchas
- One radio captures one channel at a time, so the statistics describe only the channel captured.
- Monitor-mode captures can miss frames under load; treat counts as samples.

## Verify
- [ ] The target AP's BSSID appears on the expected channel in the list.

## Checked
2026-11-09. Read: Wireshark User's Guide section 10.5 WLAN Traffic (one row per network, probe
request merging, Only show existing networks, name resolution, Copy as CSV, live updating), the
tshark man page (`-z io,stat,interval[,filter]...` form and multiple filters) and the wlan dfref
page (field names). Removed: the column list, expanding a BSSID, right-click filtering, the deauth
interpretation, the `tshark -z wlan,stat` example (the man page does not document it), the 10
percent retry threshold and the per-SSID beacon overhead claim.
Method: docs-checked 2026-11-09 against Wireshark User's Guide 10.5, the tshark man page and the wlan dfref page.
