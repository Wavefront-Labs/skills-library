---
id: computing-software.digital-privacy-hygiene.vpn-tools.importing-raw-wireguard-configs
name: importing-raw-wireguard-configs
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, wireguard-config, vpn-protocol-selection, kill-switch]
level: practitioner
status: docs-checked
description: "Use a raw WireGuard config from a VPN provider with wg-quick on Linux, understand each field, add the documented kill switch, and generate keys safely."
sources:
  - "https://www.wireguard.com/quickstart/"
  - "https://man7.org/linux/man-pages/man8/wg-quick.8.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Importing raw WireGuard configs

**Goal:** use a provider's WireGuard config on Linux with `wg-quick`, and know what each line does.

## Anatomy
```
[Interface]
PrivateKey = <your private key>       # keep secret
Address = <tunnel address>/32         # addresses assigned to the interface
DNS = <tunnel DNS server>             # set via resolvconf by wg-quick

[Peer]
PublicKey = <server public key>
Endpoint = <server IP>:<port>
AllowedIPs = 0.0.0.0/0, ::/0          # default route: wg-quick makes the tunnel the default gateway
```
wg-quick adds `Address`, `DNS`, `PreUp`/`PostUp`/`PreDown`/`PostDown` and similar keys on top of the format `wg(8)`
reads. It infers routes from the peers' AllowedIPs; a default route entry makes the interface the default gateway.

## Import on Linux
- `wg-quick up <name>` reads `/etc/wireguard/<name>.conf` (it searches there first), so save the config as
  `/etc/wireguard/wg0.conf` and run `wg-quick up wg0`; `wg-quick down wg0` tears it down.
- `wg show` displays the current interface state.
- `DNS =` runs `resolvconf -a tun.INTERFACE -m 0 -x`; if that is unwanted, use `PostUp`/`PostDown` instead.

## Kill switch (Linux)
The wg-quick manual's example, for a peer with `0.0.0.0/0` in AllowedIPs, adds to `[Interface]`:
```
PostUp = iptables -I OUTPUT ! -o %i -m mark ! --mark $(wg show %i fwmark) -m addrtype ! --dst-type LOCAL -j REJECT
PreDown = iptables -D OUTPUT ! -o %i -m mark ! --mark $(wg show %i fwmark) -m addrtype ! --dst-type LOCAL -j REJECT
```
It drops packets that are neither encrypted tunnel traffic nor going through the tunnel. The manual's note
afterwards covers its limits; read it before relying on this. For IPv6, use the equivalent `ip6tables` rules.

## Key hygiene
- Generate keys with `wg`; set `umask 077` first so the private key file is not world-readable:
  `wg genkey | tee privatekey | wg pubkey > publickey`.
- Give the provider only the public key; never share the private key.

## Checked
2026-11-01. Confirmed in the WireGuard quickstart (key generation, `umask 077`, `wg show`) and the wg-quick(8)
manual (config path, Address and DNS handling, default-route behaviour, kill-switch lines, resolvconf). Removed:
the `chmod 600`, systemd `enable`, PersistentKeepalive, Windows app checkbox, provider portal, key-count and
rotation-linkability claims, and the Mullvad page (login-gated).
Method: documentation only; no commands were run.
