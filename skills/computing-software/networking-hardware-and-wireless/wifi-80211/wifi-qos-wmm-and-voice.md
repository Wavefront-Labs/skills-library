---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-qos-wmm-and-voice
name: wifi-qos-wmm-and-voice
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-wmm-qos, voice-over-wlan, dscp-to-wmm]
level: advanced
status: draft
description: "Map DSCP to WMM access categories and tune voice SSIDs: admission control, rates, roaming and queue behaviour."
sources:
  - https://www.ieee802.org/11/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# WMM and voice

- WMM (802.11e EDCA) has four access categories: voice (AC_VO), video (AC_VI), best effort (AC_BE), background (AC_BK). Higher priorities get shorter waits and smaller contention windows.
- Mark traffic with DSCP at the source; map DSCP to the WMM user priority in the AP/controller (for voice commonly EF -> AC_VO). Keep the wired QoS trust boundary consistent.
- Leave WMM enabled; some features (Wi-Fi 5/6 rates) depend on it.
- For voice: -67 dBm or better coverage, roaming via 802.11r/k/v, and prefer 5 GHz.
- Admission control (WMM-AC / CAC) can reject excess voice calls; use only if the clients support it.

## Verify
- [ ] A capture of voice packets shows the expected DSCP and QoS TID.
