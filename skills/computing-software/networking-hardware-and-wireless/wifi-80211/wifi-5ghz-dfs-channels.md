---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-5ghz-dfs-channels
name: wifi-5ghz-dfs-channels
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-5ghz-dfs, unii-bands, radar-detection]
level: practitioner
status: draft
description: "Plan 5 GHz channels across UNII bands, handle DFS radar events and choose 20/40/80 MHz widths for density."
sources:
  - https://www.ieee802.org/11/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# 5 GHz channels and DFS

- 5 GHz is divided into UNII sub-bands with country-specific rules. Some bands require Dynamic Frequency Selection (DFS) because radar shares them: the AP must listen before use (channel availability check, commonly 60 s) and vacate on radar detection.
- A radar event forces a channel change and can briefly drop clients. Mix DFS and non-DFS channels; clients that honour channel switch announcements recover faster.
- Width trade-off: 80 MHz gives rate but few non-overlapping channels. In dense venues prefer 20 or 40 MHz for reuse; in low-density sites 80 MHz is fine.
- Set the correct regulatory domain/country code. A wrong code can enable illegal channels. Allowed channels are country-specific: check the regulator, do not guess.

## Verify
- [ ] Controller shows the right country code and its allowed channel list.
- [ ] Event log shows no repeated radar events on chosen DFS channels (if it does, move off them).
