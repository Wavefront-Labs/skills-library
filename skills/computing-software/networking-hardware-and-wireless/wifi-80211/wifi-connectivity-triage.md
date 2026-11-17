---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-connectivity-triage
name: wifi-connectivity-triage
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-troubleshooting, wlan-triage, association-failure, wifi-troubleshooting]
level: practitioner
status: draft
description: "Walk the OSI-stack triage for WLAN complaints: RF, association, authentication, DHCP/DNS and application, with the logs to read."
sources:
  - https://www.cwnp.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# WLAN triage order

1. Scope: one client, one AP, one SSID, or everyone? When did it start? What changed?
2. RF: RSSI/SNR, retry rate, channel utilisation, interference. Tools: client diagnostics, controller RF dashboard, spectrum analyser.
3. Association/auth: controller client-event log; reason/status codes (e.g. deauth reason codes); RADIUS logs.
4. IP: DHCP success, scope exhaustion, DNS.
5. Application: backend, VPN, proxy.

## Common patterns
- Works near the AP only: cell too small or client uplink weak.
- Slow for all: channel utilisation high, low basic rates, a client at cell edge hogging airtime.
- Intermittent drops: DFS radar events, roaming failures, power issues, firmware bugs. Correlate with logs.

## Verify
- [ ] Root cause is confirmed by a measurement, not only an inference, before changing multiple settings.
