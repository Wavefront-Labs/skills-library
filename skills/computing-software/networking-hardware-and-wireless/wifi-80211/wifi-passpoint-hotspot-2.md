---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-passpoint-hotspot-2
name: wifi-passpoint-hotspot-2
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-passpoint, hotspot-2-0, 80211u-anqp, wifi-passpoint-openroaming]
level: advanced
status: draft
description: "Understand Passpoint profiles, 802.11u ANQP discovery, realm/roaming consortium and how a client auto-connects securely."
sources:
  - https://www.wi-fi.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Passpoint

- Based on IEEE 802.11u: the AP advertises network capabilities via ANQP (Access Network Query Protocol) before association, including realms (NAI), roaming consortium OIs and venue info.
- Client holds a Passpoint profile (credentials: certificate, SIM/EAP-SIM/AKA, or username/password) and auto-selects a matching network, authenticating with WPA2/WPA3-Enterprise, so no captive portal is needed.
- Server certificate validation is part of the profile; a profile without it would be exploitable by rogue APs.
- Deployment items: RADIUS with the correct realm, HS2.0 settings on the SSID (usually a separate hidden or visible Passpoint SSID/profile), and OSU if onboarding is used.
- OpenRoaming builds a federation on Passpoint so users can roam across participating providers; join through a federation provider.

## Verify
- [ ] A provisioned client connects automatically in range, and the capture shows ANQP queries and an 802.1X exchange.
