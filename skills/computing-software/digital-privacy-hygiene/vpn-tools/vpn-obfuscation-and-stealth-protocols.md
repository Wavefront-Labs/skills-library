---
id: computing-software.digital-privacy-hygiene.vpn-tools.vpn-obfuscation-and-stealth-protocols
name: vpn-obfuscation-and-stealth-protocols
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, vpn-obfuscation, bridges, vpn-protocol-selection]
level: practitioner
status: draft
description: "Use VPN obfuscation (WireGuard over TCP or QUIC, Shadowsocks, Stealth) when networks or countries block VPNs, and know what it does not hide."
sources:
  - "https://mullvad.net/en/help/obfuscation"
  - "https://protonvpn.com/support/stealth-protocol"
  - "https://ssd.eff.org/module/understanding-and-circumventing-network-censorship"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# VPN obfuscation and stealth protocols

**Goal:** connect when a hotel, school, employer or national firewall blocks normal VPN traffic.

## Symptoms that call for it
- WireGuard connects but no handshake; UDP blocked.
- Connection drops after seconds (deep packet inspection).
- Works on mobile data, fails on a specific Wi-Fi.

## Options
| Provider | Mode | Notes |
|---|---|---|
| Mullvad | WireGuard over TCP (udp2tcp), Shadowsocks, QUIC obfuscation | Settings > VPN settings > WireGuard obfuscation; Automatic tries them |
| Proton VPN | Stealth protocol (WireGuard over TLS) | Protocol selector |
| Generic | OpenVPN TCP 443 | Looks like HTTPS port, still fingerprintable |
| Tor | Bridges with obfs4/Snowflake/WebTunnel | When VPN providers are blocked by IP |

## Process
1. Try a different port (443/53) and protocol first.
2. Turn on obfuscation; set to Automatic or force a mode.
3. If provider IPs are blocklisted, try Tor bridges or a self-hosted server on a cloud VPS.

## Limits
- Obfuscation hides that it's a VPN protocol from simple filters; sophisticated censors may still detect or
  throttle unknown encrypted traffic.
- It adds latency (TCP over TCP).
- In countries where VPN use is illegal, obfuscation reduces detection but doesn't change the legal risk.

## Gotchas
- Download the app before you travel; app stores and provider sites are often blocked locally.
