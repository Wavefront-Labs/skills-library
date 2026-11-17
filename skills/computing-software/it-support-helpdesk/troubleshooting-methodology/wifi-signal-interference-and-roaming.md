---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.wifi-signal-interference-and-roaming
name: wifi-signal-interference-and-roaming
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, networking, network-troubleshooting, wifi-troubleshooting, rssi, snr, channel-interference, roaming-aggressiveness, band-steering, 2-4ghz-vs-5ghz, comptia-a-plus]
level: practitioner
status: draft
description: "Troubleshoot slow or dropping Wi-Fi on clients: signal and SNR readings, 2.4 vs 5/6 GHz, interference and channel overlap, roaming behaviour, adapter drivers and power saving."
sources:
  - "https://learn.microsoft.com/en-us/windows-server/networking/technologies/netsh/netsh-wlan"
  - "https://www.comptia.org/certifications/a"
  - "https://www.cisco.com/c/en/us/support/index.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# wifi-signal-interference-and-roaming

Goal: separate weak signal, interference, roaming and client-driver
problems when a user says "Wi-Fi keeps dropping" (A+ 220-1201 5.7:
intermittent wireless, slow speeds, limited connectivity).

## Measure on the client
```cmd
netsh wlan show interfaces     :: Signal %, BSSID (which AP), Channel, Radio type, Rx/Tx rate
netsh wlan show wlanreport     :: disconnect reasons over 3 days
```
macOS: Option-click Wi-Fi icon (RSSI, noise, channel, PHY mode); Wireless
Diagnostics app.
Rules of thumb: RSSI better than −67 dBm (signal ~70 %+) for voice/video;
SNR > 25 dB. BSSID changing frequently while stationary = roaming
flip-flop.

## Causes and fixes
| Symptom | Likely cause | Action |
|---|---|---|
| Fine near AP, bad in one room | coverage gap / walls | move, report to network team for AP placement |
| Slow at busy times | too many clients/AP, 2.4 GHz congestion | prefer 5/6 GHz SSID/band steering |
| Drops every few minutes | interference (microwaves, Bluetooth, neighbouring APs on overlapping 2.4 GHz channels), driver | update Wi-Fi driver, check channel plan |
| Drops when walking (calls) | roaming: sticky client | adjust adapter **Roaming Aggressiveness** (Intel: Medium-High), 802.11r/k/v support on network |
| Drops after sleep | adapter power saving | Device Manager → Power Management → untick "Allow the computer to turn off this device"; power plan wireless setting Max Performance |
| Connected, no internet | captive portal, DHCP/DNS | see APIPA/DNS skills |
2.4 GHz non-overlapping channels are 1, 6, 11 only.

## Isolation steps
1. Other devices in same spot fine? → this client (driver, adapter, profile).
2. Same device fine elsewhere? → location/AP.
3. Wired dock fixes it? → wireless path confirmed.
4. Phone Wi-Fi analyser apps show channel crowding and signal.

## Gotchas
- Old Wi-Fi drivers (especially Intel/Realtek from OEM image) cause most
  client-side drops — update from OEM/Windows Update driver channel.
- USB 3 ports/cables near 2.4 GHz antennas cause interference.
- Home users: ISP router in a cupboard; mesh/extenders with poor backhaul.

## Verify
Signal and BSSID stable over a working session, wlanreport shows no new
disconnect events, and a Teams call through the problem area holds.
