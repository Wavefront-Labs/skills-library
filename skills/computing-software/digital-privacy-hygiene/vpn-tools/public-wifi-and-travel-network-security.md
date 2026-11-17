---
id: computing-software.digital-privacy-hygiene.vpn-tools.public-wifi-and-travel-network-security
name: public-wifi-and-travel-network-security
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, public-wifi, evil-twin, captive-portal, mac-randomization, hotel-wifi, airport-wifi, travel-security, rogue-access-point, wifi-sniffing, firewall-public-network, bluetooth-travel]
level: intro
status: draft
description: "Secure a laptop and phone on hotel, airport and cafe Wi-Fi: evil-twin access points, captive portals, MAC randomization, and a realistic travel threat model."
sources:
  - "https://www.ncsc.gov.uk/guidance/wifi-public-safety"
  - "https://support.apple.com/guide/security/wi-fi-privacy-sec1a6946cea/web"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Public Wi-Fi and travel network security

**Goal:** use hotel, airport, cafe and conference Wi-Fi without the specific
risks those networks carry — a fake network impersonating the real one, local
network snooping, a captive portal that requires a VPN workaround — matched to
what actually matters for most travelers rather than worst-case paranoia.

## 1. The realistic threat model
Modern HTTPS adoption has made simple "cafe Wi-Fi password sniffing" far less
of a risk than it was a decade ago — most sites and apps encrypt traffic
end-to-end regardless of the network. The risks that remain are real but more
specific:
- **Evil-twin access points**: a rogue hotspot named identically to ("Airport
  Free WiFi," "Hotel Guest") or very similar to the legitimate one, run by an
  attacker nearby, that you join by mistake. Once joined, the operator can see
  unencrypted traffic and can serve a convincing fake captive portal to harvest
  credentials.
- **Local network visibility**: other devices on the same Wi-Fi can sometimes
  see each other depending on the network's isolation settings — a device with
  file sharing or network-discovery features left on is exposed to anyone else
  on that same network, not to the wider internet.
- **A VPN hides *which sites* you visit from the local network/ISP**, but
  doesn't change whether the destination site itself is secure — see
  `computing-software.digital-privacy-hygiene.vpn-tools.vpn-dns-and-tracker-blocking-setup`
  section 1 for what a VPN actually buys you here.

## 2. Confirming you joined the real network
- Ask staff directly for the exact network name and (if any) password rather
  than picking the most plausible-looking SSID from a list — evil-twin names
  are specifically designed to be indistinguishable by eye.
- If two networks with very similar names are both present and nobody can
  confirm which is official, treat both as untrusted until confirmed.
- A network requiring no password at all, specifically at a business that
  normally would provide one, is itself slightly suspicious compared to the
  venue's expected setup.

## 3. Captive portals and VPN interaction
- A **captive portal** (the login/terms page many public networks show before
  granting internet access) requires unencrypted, VPN-off access to load
  initially — this is normal and not itself a security compromise; connect,
  complete the portal, **then** turn the VPN on before doing anything else.
- Some VPN apps have a "captive portal detection" that temporarily and
  automatically allows this bypass — convenient, but confirm the VPN
  re-engages afterward rather than assuming; check the app's connection
  status indicator.
- Never enter real account credentials (email login, social login) into a
  captive portal page itself unless it's clearly the venue's own simple
  terms-acceptance form — a portal asking for a full account login is an
  unusual and avoidable request to trust with your actual password.

## 4. Device-level settings for travel
- **MAC address randomization**: modern iOS, Android and recent Windows/macOS
  versions randomize the Wi-Fi MAC address per network by default or as an
  option (iOS: Settings → Wi-Fi → network's ⓘ → Private Wi-Fi Address; similar
  on Android 12+) — this stops a venue (or anyone logging nearby Wi-Fi probe
  requests) from tracking your device's movement across visits/locations by
  its fixed hardware address. Confirm it's actually on rather than assuming
  the default, since some corporate/guest networks require a fixed MAC and
  will prompt you to disable it for that network specifically.
- **Firewall profile**: Windows and macOS let you mark a network "Public," which
  tightens file-sharing and discovery defaults automatically — confirm new
  networks default to this rather than silently inheriting a "Private/Home"
  profile from a previous network with a similar name.
- Turn off **AirDrop/Nearby Share/file-sharing discovery** when not actively
  using it in public — it broadcasts your presence and device name to anyone
  nearby, and has been used for unsolicited file-spam ("AirDrop harassment")
  in crowded public spaces.
- **Bluetooth**: leave it on only if actively using a paired device; an
  always-on, always-discoverable Bluetooth radio is a minor additional
  tracking/attack surface in dense public spaces, though practical risk is
  low for most travelers compared to the Wi-Fi-specific items above.

## 5. Sensitive tasks on the road
- Save banking, tax filing and anything requiring full attention to a trusted
  network (home, a cellular hotspot you control) where practical, rather than
  the hotel lobby — not because HTTPS fails on public Wi-Fi, but because the
  attack surface (evil twins, a worse-attended device, shoulder-surfing in a
  crowded space) is simply larger there.
- A personal/phone-tethered **mobile hotspot** removes the shared-network risk
  entirely for the cost of data usage — worth it for a single sensitive task
  rather than trusting an unfamiliar public network for it.

## Gotchas
- Confirming a network name with staff is cheap insurance that most travelers
  skip entirely — it's the single highest-value step on this list.
- A captive portal is not inherently malicious; the credential-harvesting
  variant specifically asks for a real account login rather than simple terms
  acceptance — that's the distinguishing red flag, not the portal's existence.
- Uncertain: exact default firewall/MAC-randomization behaviour differs by OS
  version and whether a network is "known" vs. new — verify current settings
  on your specific device rather than assuming parity across platforms.

## Verify
- [ ] You confirm the exact network name/password with venue staff rather than
      guessing from a list of similarly-named SSIDs.
- [ ] VPN re-engages after completing any captive portal, confirmed via the
      app's status, not assumed.
- [ ] MAC randomization confirmed on for networks where it's supported.
- [ ] New public networks default to a "Public" firewall profile; file/AirDrop
      sharing is off unless actively in use.
- [ ] Sensitive tasks (banking, tax filing) are deferred to a trusted network
      or a personal hotspot while traveling.
