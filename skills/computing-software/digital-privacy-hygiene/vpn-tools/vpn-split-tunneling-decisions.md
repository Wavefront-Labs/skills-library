---
id: computing-software.digital-privacy-hygiene.vpn-tools.vpn-split-tunneling-decisions
name: vpn-split-tunneling-decisions
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, split-tunneling, vpn-configuration, app-exclusion, banking-apps, allowedips, wireguard, kill-switch]
level: practitioner
status: docs-checked
description: "Decide which apps or networks bypass the VPN without leaking the browser or DNS, using Mullvad and Proton VPN's documented split-tunnelling modes and limits."
sources:
  - "https://mullvad.net/en/help/split-tunneling-with-the-mullvad-app"
  - "https://protonvpn.com/support/protonvpn-split-tunneling"
  - "https://www.wireguard.com/netns/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Split tunnelling decisions

**Goal:** exclude only what genuinely breaks on the VPN, and know what each exclusion reveals.

## Modes
- **Exclude (app-based):** chosen apps bypass the VPN and use your regular connection and IP; their traffic is not protected. Mullvad supports this on Windows, Linux, macOS and Android, not iOS/iPadOS. Proton VPN offers exclude on its platforms (macOS exclusion only, marked experimental).
- **Include (inverse):** only chosen apps use the tunnel. Proton VPN offers it on Windows, Linux GUI, Android and the browser extension; Mullvad says reverse split tunnelling is not currently planned.
- **By domain:** Proton's browser extension works on websites, not apps.
- **Address-based:** Proton on Windows can also take IPv4/IPv6 addresses and CIDR ranges.
- Split tunnelling is a paid-plan feature at Proton VPN.

## Platform limits to check before relying on it
- Mullvad macOS: Safari and other WebKit apps cannot be excluded; only outgoing connections, so servers (SSH, Plex) cannot accept incoming ones. Proton on macOS: WebKit apps unreliable; WireGuard and Stealth protocols only.
- Mullvad Windows: Windows Store apps cannot be excluded; conflicts with some other VPN or security software. Android: excluded apps fail if "Block connections without VPN" is on.
- Proton: on most platforms split tunnelling cannot be combined with its kill switch (Windows is the exception). Linux: restart excluded/included apps after each connect.
- Some apps are hard or impossible to exclude (Mullvad lists Java apps, some anti-cheat games, Vivox, Parsec, Proton Drive).

## DNS
Mullvad: excluded apps still use the DNS server of the Mullvad server you are connected to; a custom DNS server in the app affects all apps, and queries still go through the tunnel. Test with a DNS leak check from the excluded app if it matters.

## Linux alternative
WireGuard's netns page describes running selected programs in a "physical" namespace (for example for a captive portal login) while ordinary processes see only the WireGuard interface, avoiding routing-table tricks.

## Sensible habits (judgement, not from the pages)
- Exclude the single app that breaks, not the browser you use for sensitive browsing.
- Excluding a browser exposes all its traffic; use a separate profile or browser for the one site.

## Checked
Method: 2026-11-08 read all three cited pages. Platform and DNS facts follow Mullvad and Proton; the netns note follows WireGuard. Removed: the table of "reasonable exclusions" (banking, games, calls), `AllowedIPs` route-based splitting and "allow LAN" (not on these pages), and the iOS consumer-app claim.
