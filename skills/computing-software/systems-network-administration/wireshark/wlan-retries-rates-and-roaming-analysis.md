---
id: computing-software.systems-network-administration.wireshark.wlan-retries-rates-and-roaming-analysis
name: wlan-retries-rates-and-roaming-analysis
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, wlan-capture, 802-11, wlan-retries, data-rate, airtime, 802-11-association, wlan-roaming-analysis, radiotap, signal-dbm, deauthentication, reassociation, mcs-index, wlan-statistics]
level: advanced
status: docs-checked
description: "Analyse 802.11 captures for performance and roaming: retry rates, data rates/MCS, signal from radiotap, association sequences and deauth reason codes."
sources:
  - https://www.wireshark.org/docs/dfref/w/wlan.html
  - https://www.wireshark.org/docs/dfref/w/wlan_radio.html
  - https://www.wireshark.org/docs/dfref/r/radiotap.html
  - https://gitlab.com/wireshark/wireshark/-/raw/master/epan/dissectors/packet-ieee80211.c
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# WLAN retries, rates and roaming analysis

Requires a monitor-mode capture with radiotap headers on the client's channel (or channels).

## Useful columns
`wlan_radio.channel`, `wlan_radio.signal_dbm`, `wlan_radio.noise_dbm`, `wlan_radio.snr`,
`wlan_radio.data_rate`, `wlan_radio.11ac.mcs`, `wlan_radio.11ax.mcs`, `wlan_radio.11n.mcs_index`,
`wlan.fc.retry`, `wlan.ta`, `wlan.ra`, `wlan.fc.type_subtype`.

## Retries and rates
- Retry rate for a client: count data frames from the transmitter (`wlan.ta == aa:bb:cc:dd:ee:ff
  && wlan.fc.type == 2`) against the same filter plus `&& wlan.fc.retry == 1`. A sustained high
  share points to an RF problem such as interference, low SNR or hidden nodes; set your own
  threshold from a healthy baseline capture.
- A data rate or MCS that drops over time means the sender is rate-adapting down: poor signal,
  interference or a client far from its AP. Compare `wlan_radio.data_rate` and the MCS fields per
  frame.
- Low-rate frames consume more airtime per byte than high-rate ones, so legacy clients and
  low-rate management frames cost airtime. `wlan_radio.duration` is the per-frame duration field
  to sum for airtime.

## Signal
Signal at the sniffer is not signal at the client, but trends help. Compare
`wlan_radio.signal_dbm` against `wlan_radio.noise_dbm` (or use `wlan_radio.snr`) for client data
frames that also carry retries. Take coverage targets from your vendor's design guide.

## Association and roaming sequence
Filter on the client MAC and management frames: `(wlan.addr == <client> && wlan.fc.type == 0) || eapol`.
| Step | Subtype filter |
|---|---|
| Probe request/response | `wlan.fc.type_subtype == 0x04` / `0x05` |
| Authentication | `0x0b` |
| Association request/response | `0x00` / `0x01` |
| Reassociation request/response | `0x02` / `0x03` |
| 4-way handshake | `eapol` |
| Deauth / disassoc | `0x0c` / `0x0a` |

Measure roam time from frames: the last data frame to the old AP until the first data frame on the
new AP. Compare against a baseline for the same network.

Deauthentication and disassociation **reason codes** (`wlan.fixed.reason_code`), as Wireshark
labels them: 1 unspecified reason, 2 previous authentication no longer valid, 3 sending STA is
leaving the BSS, 4 disassociated due to inactivity, 15 4-way handshake timeout, 34 disassociated
because too many frames are not acknowledged (AP transmissions and/or poor channel conditions).

## Verify
- [ ] Retry percentage and typical MCS per client documented for the problem period.
- [ ] Roam events measured from frames, with the reason for any deauth.

## Checked
2026-11-09. Read: Wireshark wlan, wlan_radio and radiotap field references (every field named
above exists) and packet-ieee80211.c plus packet-ieee80211.h (management subtype numbers 0x00 to
0x0c, frame type values 0, 1, 2, reason code texts 1, 2, 3, 4, 15, 34). Removed: the 10-15 percent
retry threshold, the -75 and -67 dBm figures, the beacon at 1 Mb/s and basic-rate statement, the
roam-time figures for 802.1X and 802.11r/OKC, the "wrong PSK" gloss on reason 15, and the
Statistics menu path. Fixed filter precedence with parentheses.
Method: docs-checked 2026-11-09 against the wlan, wlan_radio and radiotap dfref pages and Wireshark packet-ieee80211.c/.h.
