---
id: computing-software.cybersecurity-defensive.network-defence.wpa3-sae-personal
name: wpa3-sae-personal
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [wpa3-sae, wpa3-personal, sae, transition-mode, pmf, dragonblood, wireless-security]
level: practitioner
status: docs-checked
description: "Deploy WPA3-Personal (SAE): transition mode trade-offs, PMF requirements, H2E vs hunting-and-pecking, passphrase policy, per-device PSK alternatives and client compatibility."
sources: ["https://www.wi-fi.org/discover-wi-fi/security", "https://w1.fi/cgit/hostap/plain/hostapd/hostapd.conf", "https://papers.mathyvanhoef.com/dragonblood.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WPA3-Personal (SAE)

SAE (Simultaneous Authentication of Equals) replaces the WPA2 4-way-handshake PSK exchange: captured
handshakes cannot be cracked offline, and it provides forward secrecy.

## Configuration (hostapd example)
```
wpa=2
wpa_key_mgmt=SAE            # WPA3-only; "SAE WPA-PSK" = transition mode
rsn_pairwise=CCMP
ieee80211w=2                # PMF required (mandatory for SAE)
sae_pwe=1                   # hash-to-element (H2E) only; 2 = both H2E and hunting-and-pecking
sae_password=<long passphrase>
sae_groups=19 20
```
Enterprise controllers: choose the WPA3-Personal (SAE) setting with PMF required; 6 GHz networks require WPA3 (SAE, or Enhanced Open/OWE for open networks).

## Transition mode
WPA2-PSK and SAE on the same SSID with PMF optional - compatible, but an attacker can lure clients to the
WPA2 side and capture a crackable handshake (downgrade). Prefer a separate WPA3-only SSID once clients
support it; keep transition only for a time-boxed migration.

## Implementation flaws
Dragonblood (2019) side channels and downgrade attacks against early SAE implementations: patch APs and
clients; H2E (sae_pwe=1) removes the timing-leaky hunting-and-pecking loop.

## Passphrases and alternatives
- SAE resists offline cracking, but online guessing still works: long random passphrase, rotate when staff leave.
- Shared passphrase = no per-user revocation: for IoT/headless devices use per-device PSKs, for users use WPA3-Enterprise.

## Gotchas
- Older IoT devices cannot do SAE or PMF; keep them on a separate isolated WPA2 SSID instead of weakening the main one.
- Fast roaming with SAE requires FT-SAE support on both sides.

## Verify
- [ ] Beacon/probe response shows AKM SAE and PMF required (packet capture).
- [ ] Client connections negotiate SAE, not PSK.

## Checked
2026-10-28. Confirmed against official pages: hostapd options wpa_key_mgmt SAE, ieee80211w, sae_pwe, sae_groups, sae_password (hostapd.conf); Dragonblood side-channel and downgrade attacks (Vanhoef and Ronen paper).
Removed or rewritten: the AKM number, the iw command and vendor per-device PSK names.
Method: documentation only; no commands were run.
