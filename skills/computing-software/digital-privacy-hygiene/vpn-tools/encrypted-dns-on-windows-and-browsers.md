---
id: computing-software.digital-privacy-hygiene.vpn-tools.encrypted-dns-on-windows-and-browsers
name: encrypted-dns-on-windows-and-browsers
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, windows-doh, browser-secure-dns, encrypted-dns, dns-privacy, doh, dns-over-https, quad9, cloudflare-dns, firefox-trr, chrome-secure-dns]
level: practitioner
status: docs-checked
description: "Turn on DNS over HTTPS in the Windows DNS client, choose a resolver after reading its logging policy, and know what encrypted DNS does not hide."
sources:
  - "https://learn.microsoft.com/en-us/windows-server/networking/dns/doh-client-support"
  - "https://www.privacyguides.org/en/dns/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encrypted DNS on Windows and browsers

**Goal:** stop your ISP and local network reading every domain you look up.

## Choose a resolver
Privacy Guides compares resolvers (Cloudflare, Mullvad, Quad9, NextDNS and others) by protocols supported,
logging and filtering. Read each one's privacy policy before choosing. For example, Privacy Guides notes that
Quad9 includes malware blocking by default and that Mullvad's policy says it does not log DNS requests.

## Windows DNS client
Microsoft documents DoH for the Windows DNS client (starting with Windows Server 2022). The client can use DoH only
if the primary or secondary DNS server is on the list of known DoH servers.
1. Settings > Network & Internet > the network interface > DNS settings > Edit.
2. Choose **Manual**, then enter the Preferred and Alternate DNS servers. If they are on the known list, the
   **Preferred DNS encryption** dropdown is enabled.
3. Pick **Encrypted only (DNS over HTTPS)** (no resolution if the server can't do DoH),
   **Encrypted preferred, unencrypted allowed** (falls back to plain text without notifying you) or
   **Unencrypted only**, then Save.

- `Get-DnsClientDohServerAddress` lists the known DoH servers; the default list covers Cloudflare, Google and
  Quad9 addresses.
- `Add-DnsClientDohServerAddress -ServerAddress '<resolver-IP-address>' -DohTemplate '<resolver-DoH-template>'
  -AllowFallbackToUdp $False -AutoUpgrade $True` adds another server.
- Group Policy "Configure DNS over HTTPS (DoH) name resolution policy" (Computer Configuration > Policies >
  Administrative Templates > Network > DNS Client) offers Allow, Prohibit and Require DoH. Microsoft advises
  against Require DoH on domain-joined computers.
That page is written for Windows Server; check the settings screen on your own Windows version.

## Browsers
Browsers can set their own secure DNS provider, which then overrides the system setting. Look in the browser's
privacy or security settings for its DNS over HTTPS option; vendor pages for Firefox could not be read here.

## Gotchas
- Corporate and school networks may require their own resolver.
- DNS over HTTPS protects the query in transit between you and the resolver; the resolver itself still sees the
  queries, which is why its policy matters.

## Checked
2026-11-01. Confirmed in Microsoft Learn "Secure DNS Client over HTTPS (DoH)" and Privacy Guides "DNS": settings
path and the three encryption choices, cmdlets, Group Policy options, known-server list, resolver notes. Removed:
resolver IPs beyond the Microsoft list, Windows 11-specific wording, Firefox/Chrome/Edge/Brave menu paths (Mozilla
support page blocked), the SNI/ECH note, the VPN and verification-site steps, Firefox fallback claim.
Method: documentation only; no commands were run.
