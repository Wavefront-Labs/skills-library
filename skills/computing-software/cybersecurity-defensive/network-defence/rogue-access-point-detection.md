---
id: computing-software.cybersecurity-defensive.network-defence.rogue-access-point-detection
name: rogue-access-point-detection
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [wireless-security, rogue-ap-detection, wireless-ids, wips, evil-twin, ssid-spoofing, rogue-containment, wireless-survey]
level: practitioner
status: draft
description: "Detect and handle rogue and evil-twin access points with WIDS/WIPS, wired-side correlation and physical location, with care around containment legality."
sources: ["CompTIA Security+ SY0-701 objective 2.4 (rogue access points, evil twin)", "NIST SP 800-153 Guidelines for Securing Wireless LANs (WIDS/WIPS)", "Vendor WIPS documentation (Cisco, Aruba, Juniper Mist)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rogue access point detection

**Goal:** find unauthorised access points connected to your network and fake APs imitating your
SSIDs, and remove them quickly.

## Categories
- **Rogue on wire**: unauthorised AP plugged into your LAN (often an employee's home router) - bypasses network controls. Highest priority.
- **Evil twin / honeypot**: attacker AP broadcasting your corporate SSID to capture credentials or traffic.
- **Neighbour**: someone else's AP nearby - ignore, but classify.

## Detection
1. **WIDS/WIPS** on your managed APs (dedicated scanning radios or off-channel scanning): lists
   unknown BSSIDs, flags those advertising your SSIDs, and correlates.
2. **Wired correlation**: APs' wireless MAC is often close to their wired MAC; WIPS checks
   whether a rogue's clients' MACs appear on your switch CAM tables or the AP answers on your wired network.
3. Switch-side: NAC/802.1X stops unknown devices from getting network access in the first place;
   alert on new MACs with vendor OUIs of consumer AP makers.
4. Periodic walk-through surveys with a wireless analyser (Ekahau, inSSIDer) for sites without WIPS.

## Response
- Rogue on wire: locate by signal strength (controller location maps) and switch port (CAM table), shut the port, remove the device, talk to the owner.
- Evil twin: confirm it advertises your SSID; find the location; ensure clients use EAP-TLS with
  pinned server certificates (then the evil twin cannot steal credentials); involve physical security / law enforcement if malicious.

## Containment caution
WIPS "containment" sends deauthentication frames to clients of the rogue. Using it against APs
that are not on your network (neighbours, public hotspots) can be illegal (US FCC has fined
operators for this). Contain only rogues confirmed on your wired network, under policy.

## Gotchas
- PMF-protected (WPA3) clients ignore forged deauth, so containment does not work against them; physical removal is the fix.
- Phone hotspots appear and vanish constantly; classify rather than alert on each.

## Verify
- [ ] Test: an unapproved AP plugged into a lab port is detected as rogue-on-wire within the agreed time.
- [ ] Rogue classification rules reviewed so neighbours do not flood alerts.
