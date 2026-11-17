---
id: computing-software.systems-network-administration.netbird.architecture-overview
name: architecture-overview
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, architecture, management-service, signal-service, relay-service, wireguard-mesh]
level: intro
status: docs-checked
description: "NetBird architecture: client, Management, Signal and Relay roles, how peers get keys and CGNAT-range IPs, and how connections are established and relayed."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/about-netbird/how-netbird-works.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
NetBird has four components. Once clients are authorised through Management, machines form a mesh of encrypted WireGuard tunnels; groups and access controls restrict the full mesh.

Management: central coordinator with a dashboard. Registers and authenticates peers (IdP or setup key), holds the network map with each peer's WireGuard public key, assigns private IPs from 100.64.0.0/10 (each account gets a random /16 by default; a deleted peer's address is released immediately), syncs changes to peers, and manages access rules, private DNS, activity logs and users.

Client: generates WireGuard keys (the private key never leaves the machine), logs in, receives the peer list, finds the best connection candidate, exchanges it via Signal and builds the tunnel. It applies access rules with the system firewall manager (such as nftables) and DNS through an embedded resolver.

Signal: lightweight service that helps peers exchange connection candidates. Stores nothing, carries no traffic, messages are end-to-end encrypted; it steps out once connected (like WebRTC signalling).

Relay: TURN-style fallback when a direct connection is impossible. Coturn historically; from v0.29.0 a new WebSocket-based relay was introduced with the intent of replacing it. It cannot decrypt WireGuard traffic.

Management, Signal and Relay can each be cloud-managed or self-hosted.

## Checked

2026-11-04. Confirmed against the NetBird how-netbird-works page: four components, 100.64.0.0/10 with a random /16 per account, immediate address release, key handling, Signal behaviour, Coturn and the v0.29.0 WebSocket relay, nftables and embedded DNS resolver. Softened the relay replacement claim to match the page wording.
Method: documentation only; no commands were run.
