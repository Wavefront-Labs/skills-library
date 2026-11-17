---
id: computing-software.systems-network-administration.home-assistant.remote-access-options
name: remote-access-options
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [remote-access, vpn, port-forwarding]
level: practitioner
status: docs-checked
description: "Choose and configure remote access to Home Assistant: Cloud, VPN, reverse proxy or port forwarding, then set the external Home Assistant URL."
sources:
  - https://www.home-assistant.io/docs/configuration/remote/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reach Home Assistant from outside the local network safely.

Only your local network can reach it by default. Follow the securing checklist before exposing it.

Options on the remote page:

1. Home Assistant Cloud: easiest, no open ports, a unique remote URL is generated and traffic is encrypted automatically.
2. VPN, for example Tailscale or ZeroTier One. The VPN connection must be established before you connect from outside; without it the Companion app's sensors will not update.
3. Reverse proxy: you must configure Home Assistant to trust it (see the reverse-proxy-trust skill).
4. Port forwarding from your router to the port Home Assistant listens on.

Finding the port: Settings > System > Network, then HTTP server, Server port. Defaults:

- New Home Assistant OS installations use port 80.
- Home Assistant OS installations set up before 2026.8 keep the port they already used, usually 8123.
- Other installation types use 8123.

On the router you can forward any free external port to that port. Router steps differ, so check the router manual.

Set the external URL:

1. Go to Settings > System > Network.
2. Under Home Assistant URL, enter the external address in the Internet field. With Cloud, turn on Use Home Assistant Cloud instead.
3. Select Save.

## Checked

2026-11-04. Confirmed against the Remote access page. Replaced 'use Home Assistant as if at home' with the page wording about connecting after the VPN is established.

Method: documentation only; no commands were run.
