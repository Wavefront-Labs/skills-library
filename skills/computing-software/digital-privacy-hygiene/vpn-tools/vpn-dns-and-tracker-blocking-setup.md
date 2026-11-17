---
id: computing-software.digital-privacy-hygiene.vpn-tools.vpn-dns-and-tracker-blocking-setup
name: vpn-dns-and-tracker-blocking-setup
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, vpn, wireguard, openvpn, kill-switch, no-logs-audit, free-vpn, dns-leak, encrypted-dns, doh, dot, dns-over-https, dns-over-tls, android-private-dns, ios-dns-profile, secure-dns, tracker-blocking, ublock-origin, ublock-origin-lite, manifest-v3, firefox, enhanced-tracking-protection, brave, mullvad-browser, tor-browser, fingerprinting, webrtc-leak, threat-model]
level: practitioner
status: draft
description: "Decide if you need a VPN, pick one on audited no-logs/WireGuard/kill-switch criteria, test for DNS leaks, enable encrypted DNS, and block trackers without adding fingerprint."
sources:
  - "https://ssd.eff.org/module/choosing-vpn-thats-right-you"
  - "https://support.mozilla.org/kb/enhanced-tracking-protection-firefox-desktop"
  - "https://support.mozilla.org/kb/firefox-dns-over-https"
  - "https://github.com/gorhill/uBlock"
  - "https://www.torproject.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VPN, encrypted DNS and tracker blocking — know what each layer actually buys you

**Goal:** match tools to a real threat, set them up so they don't leak, and stop
cross-site tracking in the browser without making yourself more unique.

## 1. Threat model first
A VPN encrypts traffic between your device and the VPN server and swaps your IP
address for the server's. That **helps** on untrusted Wi-Fi, hides browsing from your
ISP/local network, and gets around IP-based blocks. It does **not**:
- make you anonymous to sites you log into, or stop cookies and fingerprinting;
- protect against phishing, malware or a weak password;
- remove trust — you move it from your ISP to the VPN provider.
HTTPS already protects page contents on public Wi-Fi; the VPN mainly hides *which*
sites and your IP. If your need is "privacy from trackers", sections 4–5 matter more.

## 2. Choosing a VPN (criteria, not brands)
- **Independently audited no-logs policy**, with the report published and recent.
- **WireGuard** (or modern OpenVPN/IKEv2) — avoid PPTP and providers using proprietary
  protocols you can't inspect.
- **Kill switch** / "block connections without VPN" plus IPv6 and DNS leak protection.
- Clear ownership and jurisdiction, open-source apps, anonymous payment if it matters.
- **Avoid free VPNs**: many monetise by logging or injecting ads, and some apps are
  outright malware. Treat "lifetime" deals sceptically.
- Turn on the OS-level kill switch too: Android Settings › Network & internet › VPN ›
  gear › **Always-on VPN** + **Block connections without VPN** (menu names vary by
  version); on desktop use the app's kill switch.

## 3. Leak testing
With the VPN on, visit an independent leak-test site (e.g. dnsleaktest.com extended
test, browserleaks.com, ipleak.net):
- Shown IP and location should be the VPN server's, never your ISP's.
- DNS servers listed should belong to the VPN or your chosen encrypted resolver.
- **WebRTC** should not expose your real IP; if it does, enable the VPN's WebRTC
  protection or the browser's setting (uBlock Origin has "Prevent WebRTC from leaking
  local IP addresses").
Re-test after app updates and when switching networks.

## 4. Encrypted DNS (useful with or without a VPN)
DNS over HTTPS (DoH) or over TLS (DoT) hides lookups from the local network and can
block malware/tracker domains. Pick a resolver whose privacy policy you accept
(e.g. Quad9 `dns.quad9.net`, Cloudflare `one.one.one.one`, or a filtering one).
- **Android 9+**: Settings › Network & internet › **Private DNS** › "Private DNS
  provider hostname" › enter the hostname (no `https://`).
- **iOS/iPadOS 14+**: install the resolver's signed configuration profile, then
  Settings › General › VPN & Device Management (or the resolver's app).
- **Windows 11**: Settings › Network & internet › your adapter › DNS server assignment
  › Edit › set DNS and choose DNS over HTTPS.
- **Browsers**: Firefox Settings › Privacy & Security › DNS over HTTPS › Increased or
  Max Protection; Chrome/Edge › Privacy and security › Security › **Use secure DNS**.
- Many VPNs override DNS while connected — that is expected; check it in the leak test.

## 5. Browser and tracker blocking
- **Firefox**: Settings › Privacy & Security › Enhanced Tracking Protection › **Strict**
  (if a site breaks, lower it for that site via the shield icon). Add uBlock Origin.
- **Brave**: Shields on, trackers & ads "Aggressive" if you tolerate some breakage.
- **Mullvad Browser** (free, built with the Tor Project): Tor Browser's anti-
  fingerprinting without the Tor network — pair with a VPN.
- **Tor Browser**: strongest anonymity, slower; don't log into personal accounts
  through it or install add-ons.
- **uBlock Origin** is the reference blocker on Firefox. On Chrome, Manifest V2
  extensions have been switched off (2024–2025 rollout), so the full uBlock Origin
  no longer runs there; **uBlock Origin Lite** (MV3) is the replacement with fewer
  capabilities. I'm unsure of Edge's exact current status — check.
- Enable **Global Privacy Control** where offered (Firefox, Brave; has legal weight in
  some US states).

## Gotchas
- **Don't stack extensions**: each one changes your browser's fingerprint and is a
  trust grant (see `computing-software.general-digital-literacy.web-browsers.browser-essentials`).
  One content blocker is enough; several "privacy" add-ons often make you *more* unique.
- Banking and streaming sites may block VPN IPs; use split tunnelling for those apps
  rather than switching the VPN off globally.
- **Legality**: VPNs are legal in most countries but restricted or banned in some
  (e.g. China, Russia, Iran, parts of the Gulf); rules change — check before you travel.
  Using a VPN never makes an otherwise illegal act legal.

## Verify
- [ ] You can state what the VPN is protecting against in one sentence.
- [ ] Leak test shows VPN IP, expected DNS servers, no WebRTC leak.
- [ ] Kill switch tested: drop the VPN and traffic stops.
- [ ] Encrypted DNS active on phone and browser.
- [ ] One content blocker (uBlock Origin or Lite) installed; ETP Strict or Shields on.
