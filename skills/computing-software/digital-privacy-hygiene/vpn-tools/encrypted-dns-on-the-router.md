---
id: computing-software.digital-privacy-hygiene.vpn-tools.encrypted-dns-on-the-router
name: encrypted-dns-on-the-router
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, router-dns, encrypted-dns, dns-over-tls, openwrt]
level: practitioner
status: draft
description: "Configure a home router to forward DNS over TLS or HTTPS so every device gets encrypted DNS, and handle devices that bypass the router resolver."
sources:
  - "https://openwrt.org/docs/guide-user/services/dns/doh_dnsmasq_https-dns-proxy"
  - "https://docs.opnsense.org/manual/unbound.html"
  - "https://www.privacyguides.org/en/dns/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Encrypted DNS on the router

**Goal:** encrypt DNS for TVs, consoles and IoT that cannot configure it themselves.

## How it works
Devices keep sending plain DNS to the router on the LAN; the router forwards upstream over DoT (port 853) or DoH
(443). The ISP sees encrypted queries; the LAN hop is plain (acceptable on your own network).

## Firmware options
| Firmware | How |
|---|---|
| OpenWrt | `opkg install https-dns-proxy luci-app-https-dns-proxy`, pick a provider; or Stubby/Unbound for DoT |
| OPNsense / pfSense | Unbound DNS > enable DNS over TLS forwarding, add upstream with TLS hostname (e.g. `dns.quad9.net`) |
| Asuswrt (stock/Merlin) | WAN > DNS > DNS Privacy Protocol = DNS-over-TLS, add server and TLS hostname |
| ISP router | Usually cannot; put your own router or a Pi-hole/AdGuard Home with DoH upstream behind it |

Set the router's DHCP to hand out the router (or Pi-hole) as the only DNS server.

## Bypasses
- Browsers with their own secure DNS (Chrome, Firefox, Edge) and Android Private DNS skip the router. That is still
  encrypted; disable them only if you want router-level filtering to apply.
- Some devices hard-code 8.8.8.8. Optionally redirect outbound port 53 to the router with a NAT rule, and block
  known DoH endpoints if filtering matters.
- A VPN on a device uses the VPN's DNS instead.

## Verify
From a LAN device, run a resolver test (e.g. `https://on.quad9.net` or your provider's check page) and
`nslookup example.com` which should show the router as server. On the router, packet-capture port 53 on the WAN:
there should be none.

## Gotchas
- DoT needs correct time; a router without RTC that boots before NTP can fail to resolve. Allow a bootstrap IP or
  enable NTP by IP.
- Encrypted DNS hides queries from the ISP, not the sites you connect to (SNI and IPs remain visible).
