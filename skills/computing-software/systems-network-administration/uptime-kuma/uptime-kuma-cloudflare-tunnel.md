---
id: computing-software.systems-network-administration.uptime-kuma.uptime-kuma-cloudflare-tunnel
name: uptime-kuma-cloudflare-tunnel
category: computing-software
field: systems-network-administration
product: uptime-kuma
tags: [cloudflare-tunnel, cloudflared, tunnel-token, zero-trust, uptime-kuma-cloudflared-token]
level: practitioner
status: docs-checked
description: "Expose Uptime Kuma through a Cloudflare Tunnel by entering a tunnel token in Settings or an environment variable."
sources: ["https://github.com/louislam/uptime-kuma/wiki/Reverse-Proxy-with-Cloudflare-Tunnel", "https://github.com/louislam/uptime-kuma/wiki/Environment-Variables"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Uptime Kuma behind a Cloudflare Tunnel

Needs a domain whose DNS is managed by Cloudflare. For Docker only the Debian-based image works (the Alpine base is unsupported); the feature adds about 30 MB to the image. Non-Docker installs need `cloudflared` installed.

Steps:
1. In Cloudflare Zero Trust create a tunnel (Network, Tunnels, Create a Tunnel, Cloudflared) and name it.
2. Copy the connector install command and extract the token from its end.
3. In Uptime Kuma open Settings, Reverse Proxy, paste into Cloudflare Tunnel Token and click Start cloudflared.
4. Back in Cloudflare, when the connector shows, map your hostname to `http://localhost:3001`. SSL is automatic.

Or set `UPTIME_KUMA_CLOUDFLARED_TOKEN=<your token>`; cloudflared then starts automatically and you do not need to publish the container port to the host.

Stop it by removing the mapping in Cloudflare, or click Stop cloudflared and Remove Token in Uptime Kuma. Pros listed by the author: no exposed real IP, can sit behind a firewall, free SSL. Con: the nameserver must move to Cloudflare.

## Checked

2026-11-04. Confirmed against the Uptime Kuma wiki: Reverse Proxy with Cloudflare Tunnel page (requirements, steps, 30 MB, stop options, UPTIME_KUMA_CLOUDFLARED_TOKEN) and Environment Variables page. Removed: The pointer to the side-note page and the generic verify line.

Method: documentation only; no commands were run.
