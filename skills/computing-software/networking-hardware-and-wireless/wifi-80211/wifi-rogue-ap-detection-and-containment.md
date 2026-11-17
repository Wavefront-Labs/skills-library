---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-rogue-ap-detection-and-containment
name: wifi-rogue-ap-detection-and-containment
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-rogue-ap, wips-wids, evil-twin-detection, wifi-wips-rogue]
level: advanced
status: draft
description: "Classify neighbouring, rogue and misconfigured APs and decide on alerting, wired-side tracing and containment under local law."
sources:
  - https://www.cwnp.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rogue AP handling

- Classify: your own, neighbour (visible, not connected to your network), rogue (connected to your wired network), evil twin (spoofs your SSID).
- Detect with controller RF scanning or dedicated sensors; match BSSIDs against your inventory and look for your SSID from unknown BSSIDs.
- Wired-side detection: trace the rogue's MAC through switch tables (MAC adjacency) to find the port and disable it.
- Over-the-air containment (deauthenticating clients of a neighbour's AP) can be unlawful or harm neighbours in some jurisdictions. Prefer wired port shutdown, physical removal and policy.
- Keep PMF on and 802.1X server-certificate validation enforced to blunt evil twins.

## Verify
- [ ] A planted test AP is detected, located to a switch port and removed within the SLA.
