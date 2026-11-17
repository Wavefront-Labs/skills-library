---
id: computing-software.systems-network-administration.network-design.wireless-deauthentication-attacks
name: wireless-deauthentication-attacks
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, network-attacks, deauth-attack, 802-11w, pmf, wireless-ids, wpa3]
level: practitioner
status: gated
description: "Recognise and mitigate Wi-Fi deauthentication and disassociation attacks: how forged management frames work, 802.11w PMF, WPA3, WIDS detection and physical response."
sources:
  - https://standards.ieee.org/ieee/802.11w/3725/
  - https://www.wi-fi.org/discover-wi-fi/security
  - https://www.cisco.com/c/en/us/td/docs/wireless/controller/9800/config-guide/b_wl_17_9_cg/m_pmf.html
  - https://www.aircrack-ng.org/doku.php?id=deauthentication
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wireless deauthentication attacks

## How it works
802.11 management frames (deauthentication, disassociation) were unauthenticated before 802.11w.
An attacker spoofs the AP's BSSID and sends deauth frames to a client (or broadcast), knocking it
off. Used to: deny service, force reconnection to capture WPA2 4-way handshakes for offline PSK
cracking, or push clients onto an evil twin. Tools like aireplay-ng do it trivially.

## Mitigations
- **802.11w Protected Management Frames (PMF)**: robust management frames are integrity-protected
  after association; spoofed deauth/disassoc ignored. PMF is reported as required for WPA3 and Wi-Fi 6E/6 GHz (gated: unconfirmed, source is paywalled or blocked); set "PMF required" on WPA3 SSIDs, "optional" on WPA2/WPA3 transition SSIDs
  for legacy clients.
- WPA3-SAE: even captured handshakes do not enable offline dictionary attacks (gated: unconfirmed, source is paywalled or blocked).
- 802.1X/EAP-TLS for corporate SSIDs (no PSK to crack).
- Note: PMF does not stop RF jamming or attacks before association.

## Detection
- WIDS/WIPS on controllers alert on deauth floods
  and spoofed BSSIDs.
- Symptoms: clients repeatedly disconnecting, spikes in deauth counters, evil twin SSIDs nearby.
- Locate the source with RSSI triangulation in the WLC/location services, then physical response.
- Do not use WIPS "containment" (sending your own deauths) against neighbours' networks: unlawful in
  many jurisdictions; take legal advice.

## Verify
- [ ] Corporate SSIDs show PMF required (WPA3) or optional (transition); a lab deauth test against a PMF client fails to disconnect it; WIDS alerts on the test.

## Checked

- Date: 2026-10-28
- Confirmed: Aircrack-ng deauthentication page: the attack sends disassociate packets to associated clients, used to capture WPA/WPA2 handshakes or recover hidden ESSIDs, run with aireplay-ng.
- Removed: SA Query wording, WIDS product names, FCC fine claim.
- Gated: PMF being required for WPA3 and 6 GHz, and WPA3-SAE resisting offline dictionary attacks (IEEE and Wi-Fi Alliance pages gave no matching text, Cisco PMF page returned 404).
Method: documentation only; no commands were run.
