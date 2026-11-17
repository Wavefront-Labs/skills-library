---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-wpa3-sae-transition
name: wifi-wpa3-sae-transition
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-wpa3-sae, wpa3-transition-mode, sae-hash-to-element, wifi-security]
level: practitioner
status: draft
description: "Roll out WPA3-Personal SAE alongside WPA2-PSK using transition mode and check client compatibility and PMF."
sources:
  - https://www.wi-fi.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# WPA3-Personal (SAE)

- SAE replaces the PSK 4-way handshake input with a password-authenticated key exchange; captured handshakes cannot be brute-forced offline the way WPA2-PSK handshakes can.
- Transition mode advertises both WPA2-PSK and WPA3-SAE on one SSID so older clients keep working. It keeps the WPA2 downgrade surface; plan to move to SAE-only when clients allow.
- WPA3 requires Protected Management Frames (PMF/802.11w): required for SAE, optional (capable) in WPA2 transition.
- Some older clients fail on SAE-only SSIDs or on transition SSIDs with PMF required; test device classes (IoT, printers, scanners) before cutover.
- Hash-to-element (H2E) is the newer SAE password-element derivation that resists side-channel issues; 6 GHz requires it. Enable it where the platform offers the option.

## Verify
- [ ] Client OS shows WPA3 as the negotiated security, not WPA2.
- [ ] Legacy device inventory has a documented fallback SSID or VLAN.
