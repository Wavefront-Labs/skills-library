---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-pmf-and-deauth-protection
name: wifi-pmf-and-deauth-protection
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-pmf-80211w, deauthentication-attack, management-frame-protection]
level: practitioner
status: draft
description: "Enable 802.11w PMF to stop spoofed deauthentication and disassociation frames, and detect attempts with a WIPS."
sources:
  - https://www.ieee802.org/11/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Protected Management Frames

- Unprotected deauthentication/disassociation frames can be spoofed to disconnect clients (a common nuisance and a prerequisite for evil-twin tricks).
- 802.11w PMF protects unicast management frames with the session keys and broadcast ones with BIP. Set PMF to capable first; required once all clients support it. WPA3 requires it.
- Beacon protection (newer, 802.11 additions) hardens beacon integrity; support varies, confirm per platform.
- Keep a WIPS/WIDS function on (controller rogue detection or a dedicated sensor) to alert on deauth floods.

## Verify
- [ ] Beacons/association responses show MFPC (capable) or MFPR (required) bits in a capture.
- [ ] Spoofed deauth injected on a lab network is ignored by a PMF-required client.
