---
id: computing-software.digital-privacy-hygiene.vpn-tools.vpn-feature-checklist
name: vpn-feature-checklist
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, vpn-feature-checklist, vpn-selection, kill-switch]
level: practitioner
status: draft
description: "Compare VPN providers on the features that matter: kill switch, IPv6 handling, port forwarding, WireGuard, multi-hop, obfuscation, device limits and apps."
sources:
  - "https://www.privacyguides.org/en/vpn/"
  - "https://ssd.eff.org/module/choosing-vpn-thats-right-you"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# VPN feature checklist

**Goal:** a short, testable list to compare providers once you've settled on trust (audits, jurisdiction).

## Must-have
| Feature | Why | How to test |
|---|---|---|
| System kill switch / block without VPN | No leaks on reconnect | Disconnect Wi-Fi mid-download; nothing should flow |
| WireGuard | Fast, modern, small codebase | Present in apps and as raw configs |
| IPv6 handled (tunnelled or blocked) | Prevents IPv6 leaks | ipleak/test-ipv6 while connected |
| Own DNS inside tunnel | No ISP DNS leak | DNS leak test |
| Apps for all your OSes, open-source clients | Auditability | Check GitHub |

## Situational
| Feature | Who needs it |
|---|---|
| Port forwarding | Torrent seeding, hosting; few providers still offer it |
| Multi-hop | Separate entry and exit jurisdictions |
| Obfuscation (WireGuard over TCP/QUIC, Shadowsocks, Stealth) | Hotels/schools/countries that block VPNs |
| Split tunnelling | Banking apps, local services |
| Local network sharing | Printers/Chromecast while connected |
| Raw WireGuard/OpenVPN configs | Routers, Linux without app |
| Simultaneous devices | Families |
| Anonymous payment | Threat model includes provider subpoena by name |
| Ad/tracker DNS blocking | Convenience |

## Process
Shortlist 2-3 trusted providers, then score this table during a 7-30 day refund window.

## Gotchas
- Feature lists on comparison sites are often affiliate marketing; verify in the provider's docs and apps.
- "Unlimited devices" doesn't fix trust problems.
