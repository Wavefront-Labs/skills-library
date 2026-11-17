---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-guest-captive-portal-and-owe
name: wifi-guest-captive-portal-and-owe
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-guest-network, captive-portal, owe-enhanced-open]
level: practitioner
status: draft
description: "Set up a guest SSID with client isolation, rate limits, captive portal and OWE where supported, kept off the corporate VLAN."
sources:
  - https://www.wi-fi.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Guest WLAN

- Separate VLAN and firewall zone with internet-only policy; no route to internal subnets. Block RFC 1918 destinations except DNS/DHCP.
- Enable client (peer-to-peer) isolation on the SSID.
- Captive portal with terms acceptance; HTTPS-intercept is unreliable, so use the OS captive-portal detection (RFC 8910/DHCP option 114 is supported by some OSes) where available.
- Rate-limit per client and cap session time/DHCP lease.
- Enhanced Open (OWE) gives encryption without a password; open guest SSIDs without it are plaintext. Use transition mode for older clients.
- Log guest sessions as local law requires; keep retention aligned with policy.

## Verify
- [ ] From a guest client, pings to internal hosts fail and the portal appears on a clean device.
