---
id: computing-software.systems-network-administration.network-design.remote-access-vpn-and-ztna
name: remote-access-vpn-and-ztna
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, remote-management, remote-access-vpn, wireguard, ssl-vpn, ipsec-ikev2, split-tunnel, full-tunnel, ztna, clientless-vpn, mfa, posture-check, always-on-vpn, sase]
level: practitioner
status: docs-checked
description: "Design remote access: client VPN (IKEv2, TLS, WireGuard), split vs full tunnel, MFA and posture, clientless portals and per-app ZTNA, with a WireGuard example."
sources:
  - https://www.wireguard.com/quickstart/
  - https://csrc.nist.gov/pubs/sp/800/207/final
  - https://raw.githubusercontent.com/WireGuard/wireguard-tools/master/src/man/wg-quick.8
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remote access VPN and ZTNA

## Options
| Model | What the user gets | Fits |
|---|---|---|
| Client VPN, full tunnel | all traffic via HQ | strict inspection, legacy |
| Client VPN, split tunnel | only corporate prefixes via VPN | most orgs; SaaS direct |
| Clientless (SSL portal) | browser access to web apps, RDP/SSH via HTML5 | contractors, unmanaged devices |
| ZTNA (zero trust network access) | per-application access brokered after identity + device posture, no network-level access | NIST SP 800-207 model; replaces "VPN puts you on the LAN" |

## Design points
- **Authentication**: SAML/OIDC to the IdP with MFA; certificates for device identity;
  never PSK-only for users.
- **Posture**: managed device, disk encryption, EDR running, OS patch level; deny or restrict
  otherwise.
- **Split tunnel**: route internal prefixes + internal DNS suffixes via VPN; send SaaS (Teams,
  Zoom) direct for performance. Use DNS split (`*.corp.example` to internal resolvers).
- **Address pools** sized for peak concurrency, non-overlapping with the private ranges common
  on home routers (overlaps break split-tunnel routing).
- **Capacity**: licence and throughput of the head-end; two head-ends in different sites behind
  a DNS name or anycast.
- **Logging**: user, device, assigned IP, start/stop for incident response.

## WireGuard example (small org / admin access)
Server `/etc/wireguard/wg0.conf`:
```
[Interface]
Address = 10.99.0.1/24
ListenPort = 51820
PrivateKey = <SERVER_PRIVATE_KEY>
[Peer]
PublicKey = <ALICE_PUBLIC_KEY>
AllowedIPs = 10.99.0.10/32
```
Client:
```
[Interface]
Address = 10.99.0.10/32
PrivateKey = <ALICE_PRIVATE_KEY>
DNS = 10.0.0.53
[Peer]
PublicKey = <SERVER_PUBLIC_KEY>
Endpoint = vpn.example.org:51820
AllowedIPs = 10.0.0.0/8          # split tunnel; 0.0.0.0/0 = full tunnel
PersistentKeepalive = 25
```
Keys: `umask 077; wg genkey | tee privatekey | wg pubkey > publickey` (base64 keys, per the WireGuard quickstart). Enable IP forwarding and firewall rules on the
server. WireGuard has no built-in MFA or user directory: put it behind an access broker or use it
for admin/site links.

## Verify
- [ ] Login requires MFA; non-compliant device is denied or restricted.
- [ ] Split-tunnel client reaches internal apps and resolves internal names; SaaS goes direct.
- [ ] Failover to the second head-end tested.

## Checked
2026-10-28. Confirmed against the WireGuard quickstart and wg-quick man page: `/etc/wireguard/<interface>.conf`, `[Interface]`/`[Peer]` fields (`Address`, `ListenPort`, `PrivateKey`, `DNS`, `PublicKey`, `AllowedIPs`, `Endpoint`), key generation with `wg genkey`/`wg pubkey`, and `PersistentKeepalive` with 25 seconds as the quickstart's suggested interval for NAT. Confirmed from the NIST SP 800-207 page: zero trust moves defences from static network perimeters to users, assets and resources. Removed: the exam-objective source and the specific home-router subnet figures.
Method: documentation only; no commands were run.
