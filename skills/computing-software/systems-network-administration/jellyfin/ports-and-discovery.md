---
id: computing-software.systems-network-administration.jellyfin.ports-and-discovery
name: ports-and-discovery
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, ports, 8096, 8920, 7359, client-discovery, networking]
level: intro
status: docs-checked
description: "Know which ports Jellyfin binds (8096, 8920, 7359) and which are configurable."
sources: ["https://jellyfin.org/docs/general/post-install/networking/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Jellyfin ports and discovery

Jellyfin streams content and serves its web client over HTTP(S) only. In local networks it also offers auto-discovery, which does not work outside your local subnet. It runs independently of the Internet; an internet connection is needed only for metadata providers.

| Port | Protocol | Configurable | Purpose |
| --- | --- | --- | --- |
| 8096 | TCP | yes | default HTTP, the web frontend |
| 8920 | TCP | yes | default HTTPS, unused unless HTTPS is enabled |
| 7359 | UDP | no | client discovery |

Change the HTTP and HTTPS ports on the **Networking** page of the admin settings.

Client discovery answers a broadcast to 7359/UDP with the server name, IP address and ID, so local clients can find the server. Do not expose discovery externally.

Locally the server is reached at the host IP and port, for example `http://10.0.0.2:8096`, or through a local DNS entry such as `http://jellyfin.internal:8096`. Devices like Google Chromecast or Google TV Streamer may ignore the local DNS server; a workaround is a public IPv6 DNS record pointing at a globally routable IPv6 address of the server, while still blocking inbound access in the firewall.

Check: browse to `http://<server-ip>:8096` from another device on the LAN.

## Checked

2026-11-08. Confirmed against the Jellyfin Networking page: ports table with protocol and configurable column, the Networking admin page for changing ports, discovery broadcast replies, local access examples, Chromecast and Google TV Streamer DNS note with the IPv6 workaround, internet independence. Removed: the Docker and DLNA host-networking paragraph, which is not on this page. Page read in full.

Method: documentation only; no commands were run.
