---
id: computing-software.cybersecurity-defensive.network-defence.wireguard-deployment
name: wireguard-deployment
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [vpn, wireguard, wg-quick, curve25519, peer-management, allowedips, key-rotation, preshared-key]
level: practitioner
status: docs-checked
description: "Deploy WireGuard tunnels securely: key generation, AllowedIPs routing, firewalling, preshared keys, key distribution and its operational limits for enterprise use."
sources: ["https://www.wireguard.com/quickstart/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WireGuard

**Goal:** a simple, fast encrypted tunnel (site-to-site, admin access, server mesh) configured
so it does not open more than intended.

## Keys and config
```
umask 077; wg genkey | tee server.key | wg pubkey > server.pub
wg genpsk > peer1.psk         # optional preshared key
```
`/etc/wireguard/wg0.conf` (server):
```
[Interface]
Address = 10.99.0.1/24
ListenPort = 51820
PrivateKey = <server private key>

[Peer]
# alice laptop
PublicKey = <peer public key>
PresharedKey = <psk>
AllowedIPs = 10.99.0.2/32
```
Client:
```
[Interface]
Address = 10.99.0.2/32
PrivateKey = <client private key>
DNS = 10.99.0.1
[Peer]
PublicKey = <server public key>
PresharedKey = <psk>
Endpoint = vpn.example.com:51820
AllowedIPs = 10.20.0.0/16          # split tunnel; 0.0.0.0/0 for full tunnel
PersistentKeepalive = 25
```

## AllowedIPs is routing and access control
On the server, each peer's AllowedIPs must be only that peer's tunnel address (or site subnet).
Overlapping or broad AllowedIPs let a peer spoof other addresses. What a peer can reach is
controlled by the server's firewall (nftables/iptables on the wg0 interface), not by WireGuard.

## Firewall
```
nft add rule inet filter forward iifname "wg0" ip saddr 10.99.0.2 ip daddr 10.20.5.10 tcp dport 22 accept
nft add rule inet filter forward iifname "wg0" drop
```

## Enterprise limits
- No built-in user authentication, MFA, posture, or central revocation; keys are the identity.
- Use a management layer if you need SSO, MFA, ACLs and key rotation for user VPN at scale.
- Removing access means removing the peer from every server config.

## Gotchas
- Private keys in config files: file permissions 600, never commit to Git.
- UDP only; blocked in some networks.

## Verify
- [ ] The `wg` tool lists only expected peers with recent handshakes.
- [ ] From a peer, only the allowed destinations/ports are reachable.

## Checked

2026-10-28. Confirmed against: WireGuard quickstart (wg genkey, wg pubkey, peer sections, AllowedIPs, ListenPort, Endpoint, PersistentKeepalive, wg-quick usage).

Removed as unconfirmed: post-quantum wording, systemd unit name, management-layer product list, logging and roaming remarks, NIST SP 800-77 citation.

Method: documentation only; no commands were run.
