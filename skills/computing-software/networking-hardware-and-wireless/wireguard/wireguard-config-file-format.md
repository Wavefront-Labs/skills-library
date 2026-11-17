---
id: computing-software.networking-hardware-and-wireless.wireguard.wireguard-config-file-format
name: wireguard-config-file-format
category: computing-software
field: networking-hardware-and-wireless
product: wireguard
tags: [wg-conf, interface-section, peer-section, allowedips, endpoint, listenport, fwmark, ini-format]
level: practitioner
status: docs-checked
description: "Write a valid WireGuard config file: Interface and Peer fields, AllowedIPs semantics, endpoints and comments."
sources: ["https://man7.org/linux/man-pages/man8/wg.8.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WireGuard configuration file format

INI-like: one `[Interface]` section and any number of `[Peer]` sections. `#` starts a comment.

Interface fields: `PrivateKey` (required, from `wg genkey`), `ListenPort` (16-bit, random if omitted), `FwMark` (32-bit mark for outgoing packets; `0` or `off` disables; hex with `0x`).

Peer fields: `PublicKey` (required), `PresharedKey` (optional, from `wg genpsk`), `AllowedIPs`, `Endpoint`, `PersistentKeepalive` (1 to 65535 seconds; `0` or `off` disables; off by default).

```ini
[Interface]
PrivateKey = <base64>
ListenPort = 51820

[Peer]
PublicKey = <base64>
Endpoint = 192.95.5.67:1234
AllowedIPs = 10.192.122.3/32, 10.192.124.1/24

[Peer]
PublicKey = <base64>
Endpoint = [2607:5300:60:6b0::c05f:543]:2468
AllowedIPs = 10.192.122.4/32, 192.168.0.0/16
```

`AllowedIPs` does two jobs: it is the list of source addresses accepted from that peer, and the routing table that decides which peer outgoing packets go to. `0.0.0.0/0` and `::/0` match everything. Can be repeated.

`Endpoint` is an IP or hostname, a colon, then a port (IPv6 in brackets); it is updated automatically to the most recent source IP address and port of correctly authenticated packets from the peer. Optional.

`WG_ENDPOINT_RESOLUTION_RETRIES` sets how many times DNS resolution of each peer's endpoint is retried for non-permanent errors (15 if unset).

Config files with `Address`, `DNS` and similar keys are wg-quick files and need `wg-quick strip` before `wg setconf`.

Verify: after `wg setconf wg0 file`, `wg showconf wg0` prints the configuration in this same format.

## Checked

2026-11-03. Confirmed: Interface and Peer fields, AllowedIPs, Endpoint, FwMark and PersistentKeepalive ranges, comment syntax, WG_ENDPOINT_RESOLUTION_RETRIES default and wg-quick strip against the wg(8) and wg-quick(8) man pages. Removed: the claim that a peer with no endpoint can still send to you, the 'how roaming works' gloss, and the claim that hostnames are resolved when the config is applied.

Method: documentation only; no commands were run.
