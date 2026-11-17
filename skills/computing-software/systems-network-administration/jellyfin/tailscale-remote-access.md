---
id: computing-software.systems-network-administration.jellyfin.tailscale-remote-access
name: tailscale-remote-access
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, tailscale, vpn, wireguard, cgnat, known-proxies, reverse-proxy]
level: practitioner
status: draft
description: "Reach Jellyfin remotely over Tailscale when ports cannot be opened, directly or through a reverse proxy."
sources: ["https://jellyfin.org/docs/general/post-install/networking/2_tailscale/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Tailscale for remote access

Tailscale is a WireGuard-based VPN. It helps when opening ports is undesirable or impossible, such as behind carrier-grade NAT or when the ISP blocks incoming traffic. A Tailscale account is required.

**Directly**
Pros: no router changes, no public IP or extra server. Cons: every client needs Tailscale installed, blocking clients from each other needs extra complex configuration, and you rely on a third-party account.

Server: install the Tailscale app, log in and connect to the tailnet (on Linux `sudo tailscale up`), then note the server's Tailscale IP, which starts with 100, for example 100.12.34.56. Clients: install Tailscale, connect, then enter `100.12.34.56:8096` in a browser or Jellyfin client.

**With a reverse proxy.** Tailscale can link a remote reverse proxy and the Jellyfin server, which is otherwise tricky with a traditional VPN.
1. Set up Tailscale on the Jellyfin host.
2. Set up Tailscale on the proxy host and make the proxy's upstream the server's Tailscale IP. Caddy example:

```txt
example.com
redir /jellyfin /jellyfin/
reverse_proxy /jellyfin/* 100.12.34.56:8096
```

3. In Jellyfin's Dashboard, Networking, add the proxy's Tailscale IP (such as 100.65.43.21) to `known proxies`.

Check: from a device on the tailnet, open the Jellyfin address and sign in.
