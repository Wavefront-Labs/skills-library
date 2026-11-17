---
id: computing-software.systems-network-administration.headscale.server-requirements
name: server-requirements
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, requirements, ports, tcp-443, stun, dedicated-user]
level: intro
status: docs-checked
description: "What a Headscale server needs before install: public IP, HTTPS on tcp/443, the ports in use, a dedicated user, and the defaults the docs assume."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/setup/requirements.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Headscale server requirements

Headscale should just work as long as these requirements are met:

- A server with a public IP (dual-stack IPv4 and IPv6 recommended).
- A reasonably modern Linux or BSD system.
- Headscale served via HTTPS on port 443, which may use additional ports (see below).
- A dedicated local user account to run headscale.
- A little bit of command line knowledge to configure and operate it.

## Ports

| Port | Public | Use |
|---|---|---|
| tcp/80 | yes | HTTP-01 Let's Encrypt validation, only if the built-in ACME client is used |
| tcp/443 | yes | HTTPS for Tailscale clients, and the embedded DERP server if enabled |
| udp/3478 | yes | STUN for the embedded DERP server |
| tcp/9090 | no | metrics and debug endpoint |

The ports in use vary with the scenario and enabled features. Some may be changed via the configuration file, but the docs recommend sticking with the defaults. The embedded DERP server needs tcp/443 and udp/3478.

## Defaults the docs assume

- Runs as a system service under user `headscale`.
- Config at `/etc/headscale/config.yaml`.
- SQLite database.
- Data (keys, policy, database) in `/var/lib/headscale`.
- Placeholders like `<VALUE_TO_CHANGE>` and `headscale.example.com` must be replaced.

## Gotcha

The Tailscale client assumes HTTPS on port 443 in certain situations. Serving headscale via HTTP or via HTTPS on another port is possible, but HTTPS on 443 is strongly recommended for production setups (headscale issue 2164).

## Checked

2026-11-04. Confirmed against the Headscale requirements page (requirements, ports in use, assumptions, footnote on port 443). Removed the sentence introducing Headscale as a control server, which the page does not contain.

Method: documentation only; no commands were run.
