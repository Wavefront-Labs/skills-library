---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-packet-capture-80211
name: wifi-packet-capture-80211
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-packet-capture, monitor-mode-capture, 80211-status-codes]
level: advanced
status: draft
description: "Capture 802.11 frames in monitor mode, filter by BSSID and read association/auth status and reason codes."
sources:
  - https://www.wireshark.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# 802.11 packet capture

- Monitor mode on the right channel (see Wireshark WLAN capture setup). A single radio sees one channel at a time.
- Display filters: `wlan.bssid == aa:bb:cc:dd:ee:ff`, `wlan.fc.type_subtype == 0x0b` (authentication), `0x00`/`0x01` (association request/response), `0x0c` (deauthentication).
- Read the status/reason code in association responses and deauth frames. They point at policy failures (e.g. unsupported rates, PMF mismatch, AP full).
- EAPOL frames show 4-way handshake progress: missing message 3 or 4 often means a wrong PSK or wrong key derivation.
- Retries (`wlan.fc.retry == 1`) and per-frame rates show RF quality.

## Verify
- [ ] The handshake is observed end to end for a failing client and the failing message identified.
