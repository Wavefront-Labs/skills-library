---
id: computing-software.cybersecurity-defensive.network-defence.wpa3-enterprise-configuration
name: wpa3-enterprise-configuration
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [wireless-security, wpa3-enterprise, wpa3-192-bit, pmf, 802-11w, radius, ssid-design, wpa2-transition]
level: practitioner
status: draft
description: "Configure WPA3-Enterprise: protected management frames, 192-bit mode when needed, RADIUS server certificate validation, SSID design and WPA2 transition."
sources: ["Wi-Fi Alliance WPA3 Specification v3.x", "CompTIA Security+ SY0-701 objective 4.1 (WPA3, RADIUS, AAA)", "NIST SP 800-153 Guidelines for Securing WLANs"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# WPA3-Enterprise configuration

**Goal:** corporate Wi-Fi where only authenticated users/devices connect and traffic and
management frames cannot be forged or downgraded.

## Modes
- **WPA3-Enterprise (standard)**: 802.1X authentication, AES-CCMP-128, **PMF (802.11w) required**.
- **WPA3-Enterprise 192-bit mode**: Suite B (GCMP-256, ECDHE/ECDSA P-384, EAP-TLS only); for high-security environments; needs client support.
- **Transition**: WPA2/WPA3 mixed on one SSID keeps old clients working but PMF becomes optional; plan to retire.

## Design
- One corporate SSID (EAP-TLS, managed devices), one guest SSID (captive portal or WPA3-Personal SAE/OWE, isolated), IoT SSID if needed (WPA3-Personal with per-device PSKs, isolated VLAN).
- Fewer SSIDs = less airtime overhead (each beacons separately).
- Dynamic VLAN / role assignment from RADIUS.

## Controller / AP settings (vendor-neutral)
- Security: WPA3-Enterprise, PMF required, 802.1X with your RADIUS servers (redundant).
- Disable legacy: TKIP, WEP, WPA (v1), 802.11b rates.
- Enable rogue AP detection and wireless IDS features (see rogue AP skill).
- Fast roaming (802.11r FT) works with WPA3; test clients.

## Client configuration (pushed via MDM/GPO)
- Trusted RADIUS server certificate CA and server name pinned; do not allow users to accept unknown certificates (this is how evil-twin credential theft works with PEAP).
- EAP-TLS with device certificates.

## Gotchas
- Old clients (scanners, older Android, IoT) fail with PMF required: separate SSID rather than weakening corporate.
- 6 GHz band requires WPA3 (or OWE) - no WPA2 there.
- RADIUS certificate expiry breaks all Wi-Fi at once; monitor it.

## Verify
- [ ] Packet capture or controller client details show WPA3/PMF negotiated for corporate clients.
- [ ] A client configured without server validation cannot connect (profile enforced).
