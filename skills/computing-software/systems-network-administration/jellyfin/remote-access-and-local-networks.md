---
id: computing-software.systems-network-administration.jellyfin.remote-access-and-local-networks
name: remote-access-and-local-networks
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, remote-access, local-networks, cidr, known-proxies, external-access]
level: practitioner
status: draft
description: "Define Jellyfin's local network ranges and control external access globally and per user."
sources: ["https://jellyfin.org/docs/general/post-install/networking/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Local networks and remote access control

Jellyfin can disable external access entirely or enable it per user, but it must know which IP ranges count as the local network.

Where to set things:
- **Local ranges:** `Networking` > `Local Networks`, as comma-separated CIDR entries.
- **Global external access:** `Networking` > `Remote Access Settings`.
- **Per user:** `Users` > `Edit User` > `Allow remote connections to this server`.

Behind a reverse proxy these settings only work if known proxies are set up correctly (see `computing-software.systems-network-administration.jellyfin.reverse-proxy-requirements`); otherwise Jellyfin sees the proxy's address for every client. Keep the access permissions consistent with the network scope in the local network settings.

**Ways to reach the server from outside**, from the docs:
- forwarding ports directly to the internet (not recommended)
- forwarding through a reverse proxy
- a VPN connection into the network
- a VPS reverse proxying to your home network

An IP address or, for IPv6, the server's own address, is needed; a domain with DNS is the easiest way to store it, including for a dynamic IP, but a domain is not mandatory.

Check by browsing from a phone on mobile data with remote connections allowed and then blocked for the test user.
