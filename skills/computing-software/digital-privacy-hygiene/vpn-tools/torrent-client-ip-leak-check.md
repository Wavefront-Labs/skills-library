---
id: computing-software.digital-privacy-hygiene.vpn-tools.torrent-client-ip-leak-check
name: torrent-client-ip-leak-check
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, torrent-ip-check, vpn-leak-testing, qbittorrent, kill-switch]
level: practitioner
status: draft
description: "Check what IP your torrent client announces using a tracker test magnet, bind the client to the VPN interface, and stop leaks when the VPN drops."
sources:
  - "https://ipleak.net/"
  - "https://github.com/qbittorrent/qBittorrent/wiki/Frequently-Asked-Questions"
  - "https://protonvpn.com/support/port-forwarding/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Torrent client IP leak check

**Goal:** confirm the torrent client uses only the VPN, because a browser leak test does not test the client.

## Test what peers see
1. Connect the VPN and open ipleak.net; under **Torrent Address detection**, click "Activate" and copy the magnet link.
2. Add the magnet to your client. The page lists the IPs the tracker saw from the client.
3. Every IP shown must be the VPN exit IP. Any ISP IP (including IPv6) is a leak.

## Bind the client to the VPN interface
- **qBittorrent:** Tools > Options > Advanced > **Network interface** = your VPN adapter (e.g. `wg0`, `tun0`, or the
  provider's adapter name); also set "Optional IP address to bind to". If the VPN drops, the client stops instead
  of falling back to the normal connection.
- **Transmission:** set `bind-address-ipv4` (and `bind-address-ipv6`) in `settings.json` to the VPN address.
- Also enable the VPN app's kill switch and disable IPv6 if the VPN does not tunnel it.

## Port forwarding
Seeding works better with an inbound port. Some providers offer it (Proton VPN via NAT-PMP on P2P servers); Mullvad
removed port forwarding in 2023. Set the forwarded port in the client; a port forwarded on your home router while on
VPN does nothing and exposes your home IP.

## Retest after changes
After VPN reconnects, client updates, or system sleep, rerun the magnet test. Disconnect the VPN deliberately: the
client should show no connections, not resume on the ISP IP.

## Gotchas
- DHT, PEX and local peer discovery also announce your IP; they respect the bound interface but not a broken bind.
- Downloading copyrighted material is illegal in many places regardless of VPN; ISPs receive notices tied to the
  IP the swarm saw.
