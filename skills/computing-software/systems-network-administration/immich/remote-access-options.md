---
id: computing-software.systems-network-administration.immich.remote-access-options
name: remote-access-options
category: computing-software
field: systems-network-administration
product: immich
tags: [vpn, tailscale, wireguard, reverse-proxy, cloudflare]
level: practitioner
status: docs-checked
description: "Compare ways to reach Immich from outside your LAN: VPN, Tailscale and a reverse proxy, with their security trade-offs and the port 2283 warning."
sources:
  - https://docs.immich.app/guides/remote-access
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: choose how to expose Immich beyond your home network.

Warning from the docs: never forward port 2283 directly to the internet without additional configuration. That serves the web interface over plain HTTP, leaving you open to man-in-the-middle attacks.

Option 1, VPN to your home network (OpenVPN or WireGuard):

- Simple and very secure. The VPN is the single exposed component, so an Immich vulnerability does not put you at risk. Both are independently security-audited.
- Needs a static IP or Dynamic DNS (DuckDNS is a free provider), VPN software on server and clients, and an open router port to the server.

Option 2, Tailscale:

- Mediates a peer-to-peer WireGuard tunnel, so no router port is needed. Minimal configuration, and protects against Immich zero-days.
- The client usually runs as root on devices, which slightly enlarges attack surface. It is a paid service with a free tier for personal use. It must run on both server and client.

Option 3, reverse proxy:

- Clients connect over HTTPS and the proxy relays to Immich. No client software needed. For your own proxy, Nginx is a good option. You need a certificate for HTTPS; Let's Encrypt is the recommended option for a public domain, while a self-signed certificate encrypts but raises a browser warning.
- A remote proxy such as Cloudflare hides the server IP and helps against DDoS. Access controls such as Cloudflare Access can shield the web interface from Immich vulnerabilities.
- Cons: complex configuration, and depending on configuration the web UI and API may both be exposed.

## Checked

2026-11-09: read https://docs.immich.app/guides/remote-access in full; the warning, all three options and their pros and cons match. Tightened the nginx and certificate wording to what the page says.

Method: documentation only; no commands were run.
